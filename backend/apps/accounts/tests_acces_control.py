from django.contrib.auth import get_user_model
from django.core.management import call_command

import pytest
from rest_framework.test import APIClient

from apps.accounts.models import OperationalPermission
from apps.accounts.permissions import user_has_operational_permission
from apps.accounts.services import (
    role_assign_permission,
    role_create,
    tenant_user_assign_role,
    tenant_user_create,
)
from apps.tenancy.models import Tenant, TenantStatus


def _create_user_and_tenant():
    user_model = get_user_model()

    user = user_model.objects.create_user(
        username="permission_user",
        email="permission_user@example.com",
        password="test-password",
    )

    tenant = Tenant.objects.create(
        code="permission_tenant",
        name="Permission Tenant",
        status=TenantStatus.ACTIVE,
        database_name="cmms_client_template",
    )

    return user, tenant


@pytest.mark.django_db(databases=["default"])
def test_seed_access_control_creates_permissions_and_roles():
    call_command("seed_access_control")

    assert OperationalPermission.objects.filter(
        code="work_orders.start_work_order",
    ).exists()


@pytest.mark.django_db(databases=["default"])
def test_user_has_operational_permission_when_role_grants_it():
    user, tenant = _create_user_and_tenant()

    permission = OperationalPermission.objects.create(
        code="assets.view_asset",
        name="View assets",
        module="assets",
        description="Can view assets.",
    )
    role = role_create(
        code="asset_viewer_test",
        name="Asset Viewer Test",
        description="Test role.",
    )
    role_assign_permission(role=role, permission=permission)

    tenant_user = tenant_user_create(
        tenant=tenant,
        user=user,
        display_name="Permission User",
    )
    tenant_user_assign_role(tenant_user=tenant_user, role=role)

    assert (
        user_has_operational_permission(
            user=user,
            tenant_code=tenant.code,
            permission_code="assets.view_asset",
        )
        is True
    )


@pytest.mark.django_db(databases=["default"])
def test_current_user_endpoint_returns_permissions():
    user, tenant = _create_user_and_tenant()

    permission = OperationalPermission.objects.create(
        code="maintenance_requests.create_request",
        name="Create request",
        module="maintenance_requests",
        description="Can create request.",
    )
    role = role_create(
        code="requester_test",
        name="Requester Test",
        description="Test requester role.",
    )
    role_assign_permission(role=role, permission=permission)

    tenant_user = tenant_user_create(
        tenant=tenant,
        user=user,
        display_name="Permission User",
    )
    tenant_user_assign_role(tenant_user=tenant_user, role=role)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get(
        "/api/auth/me/",
        HTTP_X_CMMS_TENANT_CODE=tenant.code,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == user.username
    assert data["tenant"]["code"] == tenant.code
    assert "maintenance_requests.create_request" in data["permissions"]