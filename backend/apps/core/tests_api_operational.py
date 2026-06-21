from decimal import Decimal
from uuid import uuid4

from django.contrib.auth import get_user_model

import pytest
from rest_framework.test import APIClient

from apps.accounts.models import OperationalPermission
from apps.accounts.services import (
    role_assign_permission,
    role_create,
    tenant_user_assign_role,
    tenant_user_create,
)
from apps.assets.choices import (
    AssetCriticality,
    AssetStatus,
    AssetType,
    LocationNodeType,
)
from apps.assets.services import asset_create, location_node_create
from apps.inventory.choices import (
    InventoryLocationType,
    SparePartStatus,
    StockMovementReason,
    StockMovementType,
)
from apps.inventory.services import (
    inventory_location_create,
    spare_part_category_create,
    spare_part_create,
    stock_create,
)
from apps.maintenance_requests.choices import MaintenanceRequestPriority
from apps.maintenance_requests.services import maintenance_request_create
from apps.tenancy.models import Tenant, TenantStatus


def _suffix():
    return uuid4().hex[:8]


def _response_items(response):
    data = response.json()

    if isinstance(data, dict) and "results" in data:
        return data["results"]

    return data


def _create_authenticated_client_with_permissions(*, permission_codes):
    suffix = _suffix()
    user_model = get_user_model()

    user = user_model.objects.create_user(
        username=f"api_user_{suffix}",
        email=f"api_user_{suffix}@example.com",
        password="test-password",
    )

    tenant = Tenant.objects.create(
        code=f"api_tenant_{suffix}",
        name="API Test Tenant",
        status=TenantStatus.ACTIVE,
        database_name="cmms_client_template",
    )

    role = role_create(
        code=f"api_role_{suffix}",
        name="API Test Role",
        description="Role used for API permission tests.",
    )

    for permission_code in permission_codes:
        permission, _created = OperationalPermission.objects.get_or_create(
            code=permission_code,
            defaults={
                "name": permission_code,
                "module": permission_code.split(".")[0],
                "description": "Test permission.",
                "is_active": True,
            },
        )
        role_assign_permission(role=role, permission=permission)

    tenant_user = tenant_user_create(
        tenant=tenant,
        user=user,
        display_name=user.username,
    )
    tenant_user_assign_role(tenant_user=tenant_user, role=role)

    client = APIClient()
    client.force_authenticate(user=user)

    return client, tenant


def _create_asset():
    suffix = _suffix()

    company = location_node_create(
        code=f"api_company_{suffix}",
        name="Grupo Monelca",
        node_type=LocationNodeType.COMPANY,
    )
    site = location_node_create(
        code=f"api_site_{suffix}",
        name="El Salvador",
        node_type=LocationNodeType.SITE,
        parent=company,
    )
    facility = location_node_create(
        code=f"api_facility_{suffix}",
        name="Planta Opico",
        node_type=LocationNodeType.FACILITY,
        parent=site,
    )
    area = location_node_create(
        code=f"api_area_{suffix}",
        name="Área de corte",
        node_type=LocationNodeType.AREA,
        parent=facility,
    )
    location = location_node_create(
        code=f"api_location_{suffix}",
        name="Ubicación plasma CNC",
        node_type=LocationNodeType.LOCATION,
        parent=area,
    )

    return asset_create(
        code=f"API-PLASMA-{suffix}",
        name="CNC Plasma API",
        location=location,
        asset_type=AssetType.EQUIPMENT,
        status=AssetStatus.ACTIVE,
        criticality=AssetCriticality.HIGH,
    )


def _create_stock_item():
    suffix = _suffix()

    category = spare_part_category_create(
        code=f"api_category_{suffix}",
        name="Rodamientos API",
    )
    spare_part = spare_part_create(
        code=f"API-BRG-6205-{suffix}",
        name="Rodamiento 6205 API",
        category=category,
        status=SparePartStatus.ACTIVE,
        unit_of_measure="unit",
        minimum_stock=Decimal("1.00"),
        reorder_point=Decimal("2.00"),
    )
    location = inventory_location_create(
        code=f"api_wh_{suffix}",
        name="Almacén API",
        location_type=InventoryLocationType.WAREHOUSE,
    )

    return stock_create(
        spare_part=spare_part,
        location=location,
        quantity_on_hand=Decimal("2.00"),
    )


@pytest.mark.django_db(databases=["default", "client_template"])
def test_assets_api_lists_assets():
    asset = _create_asset()
    client, tenant = _create_authenticated_client_with_permissions(
        permission_codes=["assets.view_asset"],
    )

    response = client.get(
        "/api/assets/items/",
        HTTP_X_CMMS_TENANT_CODE=tenant.code,
    )

    assert response.status_code == 200
    items = _response_items(response)
    assert any(item["code"] == asset.code for item in items)


@pytest.mark.django_db(databases=["default", "client_template"])
def test_maintenance_request_api_can_create_request():
    asset = _create_asset()
    client, tenant = _create_authenticated_client_with_permissions(
        permission_codes=["maintenance_requests.create_request"],
    )

    response = client.post(
        "/api/maintenance-requests/requests/",
        {
            "asset_id": str(asset.id),
            "title": "Falla reportada desde API",
            "description": "La máquina presenta ruido anormal.",
            "perceived_priority": MaintenanceRequestPriority.HIGH,
            "requester_name": "Supervisor Producción",
            "is_confirmed_by_requester": True,
        },
        format="json",
        HTTP_X_CMMS_TENANT_CODE=tenant.code,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["request_number"].startswith("MR-")
    assert data["asset_code"] == asset.code


@pytest.mark.django_db(databases=["default", "client_template"])
def test_work_order_api_can_create_from_request():
    asset = _create_asset()
    maintenance_request = maintenance_request_create(
        asset=asset,
        title="No arranca desde API",
        description="El equipo no arranca.",
        requester_name="Supervisor Producción",
        perceived_priority=MaintenanceRequestPriority.URGENT,
    )
    client, tenant = _create_authenticated_client_with_permissions(
        permission_codes=["maintenance_requests.convert_to_work_order"],
    )

    response = client.post(
        "/api/work-orders/items/from-request/",
        {
            "maintenance_request_id": str(maintenance_request.id),
            "created_by_user_id": 1,
            "created_by_name": "Planificador",
        },
        format="json",
        HTTP_X_CMMS_TENANT_CODE=tenant.code,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["work_order_number"].startswith("WO-")
    assert data["asset_code"] == asset.code


@pytest.mark.django_db(databases=["default", "client_template"])
def test_inventory_api_can_create_receipt_movement():
    stock_item = _create_stock_item()
    client, tenant = _create_authenticated_client_with_permissions(
        permission_codes=["inventory.create_stock_movement"],
    )

    response = client.post(
        "/api/inventory/movements/",
        {
            "stock_item_id": str(stock_item.id),
            "movement_type": StockMovementType.RECEIPT,
            "reason": StockMovementReason.PURCHASE,
            "quantity": "3.00",
            "reference": "PO-API-001",
            "created_by_name": "Almacén",
        },
        format="json",
        HTTP_X_CMMS_TENANT_CODE=tenant.code,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["quantity_before"] == "2.00"
    assert data["quantity_after"] == "5.00"