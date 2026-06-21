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
from apps.assets.models import (
    AssetCriticality,
    AssetStatus,
    AssetType,
    LocationNodeType,
)
from apps.assets.services import asset_create, location_node_create
from apps.tenancy.models import Tenant, TenantStatus


def _suffix():
    return uuid4().hex[:8]


def _create_asset():
    suffix = _suffix()

    company = location_node_create(
        code=f"access_company_{suffix}",
        name="Grupo Monelca",
        node_type=LocationNodeType.COMPANY,
    )
    site = location_node_create(
        code=f"access_site_{suffix}",
        name="El Salvador",
        node_type=LocationNodeType.SITE,
        parent=company,
    )
    facility = location_node_create(
        code=f"access_facility_{suffix}",
        name="Planta Opico",
        node_type=LocationNodeType.FACILITY,
        parent=site,
    )
    area = location_node_create(
        code=f"access_area_{suffix}",
        name="Área de corte",
        node_type=LocationNodeType.AREA,
        parent=facility,
    )
    location = location_node_create(
        code=f"access_location_{suffix}",
        name="Ubicación plasma CNC",
        node_type=LocationNodeType.LOCATION,
        parent=area,
    )

    return asset_create(
        code=f"ACCESS-PLASMA-{suffix}",
        name="CNC Plasma Access",
        location=location,
        asset_type=AssetType.EQUIPMENT,
        status=AssetStatus.ACTIVE,
        criticality=AssetCriticality.HIGH,
    )


def _create_user_and_tenant():
    suffix = _suffix()
    user_model = get_user_model()

    user = user_model.objects.create_user(
        username=f"access_user_{suffix}",
        email=f"access_user_{suffix}@example.com",
        password="test-password",
    )

    tenant = Tenant.objects.create(
        code=f"access_tenant_{suffix}",
        name="Access Test Tenant",
        status=TenantStatus.ACTIVE,
        database_name="cmms_client_template",
    )

    return user, tenant


def _grant_permission(*, user, tenant, permission_code):
    suffix = _suffix()

    permission = OperationalPermission.objects.create(
        code=permission_code,
        name=permission_code,
        module=permission_code.split(".")[0],
        description="Test permission.",
    )

    role = role_create(
        code=f"access_role_{suffix}",
        name="Access Test Role",
        description="Test role.",
    )
    role_assign_permission(role=role, permission=permission)

    tenant_user = tenant_user_create(
        tenant=tenant,
        user=user,
        display_name=user.username,
    )
    tenant_user_assign_role(tenant_user=tenant_user, role=role)


@pytest.mark.django_db(databases=["default", "client_template"])
def test_operational_api_rejects_unauthenticated_user():
    _create_asset()
    client = APIClient()

    response = client.get("/api/assets/items/")

    assert response.status_code in [401, 403]


@pytest.mark.django_db(databases=["default", "client_template"])
def test_operational_api_rejects_authenticated_user_without_permission():
    _create_asset()
    user, tenant = _create_user_and_tenant()

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get(
        "/api/assets/items/",
        HTTP_X_CMMS_TENANT_CODE=tenant.code,
    )

    assert response.status_code == 403


@pytest.mark.django_db(databases=["default", "client_template"])
def test_operational_api_allows_user_with_permission():
    asset = _create_asset()
    user, tenant = _create_user_and_tenant()
    _grant_permission(
        user=user,
        tenant=tenant,
        permission_code="assets.view_asset",
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get(
        "/api/assets/items/",
        HTTP_X_CMMS_TENANT_CODE=tenant.code,
    )

    assert response.status_code == 200
    assert any(item["code"] == asset.code for item in response.json())