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
from apps.tenancy.models import Tenant, TenantStatus


@pytest.mark.django_db(databases=["default"])
def test_token_login_and_current_user_endpoint_returns_permissions():
    user_model = get_user_model()
    user = user_model.objects.create_user(
        username="auth_user",
        email="auth_user@example.com",
        password="test-password",
    )

    tenant = Tenant.objects.create(
        code="auth_tenant",
        name="Auth Tenant",
        status=TenantStatus.ACTIVE,
        database_name="cmms_client_template",
    )

    permission = OperationalPermission.objects.create(
        code="assets.view_asset",
        name="View assets",
        module="assets",
        description="Can view assets.",
    )
    role = role_create(
        code="auth_role",
        name="Auth Role",
        description="Role used for auth API tests.",
    )
    role_assign_permission(role=role, permission=permission)

    tenant_user = tenant_user_create(
        tenant=tenant,
        user=user,
        display_name=user.username,
    )
    tenant_user_assign_role(tenant_user=tenant_user, role=role)

    client = APIClient()

    token_response = client.post(
        "/api/auth/token/",
        {
            "username": "auth_user",
            "password": "test-password",
        },
        format="json",
    )

    assert token_response.status_code == 200
    tokens = token_response.json()
    assert "access" in tokens
    assert "refresh" in tokens

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")

    me_response = client.get(
        "/api/auth/me/",
        HTTP_X_CMMS_TENANT_CODE=tenant.code,
    )

    assert me_response.status_code == 200
    data = me_response.json()
    assert data["username"] == "auth_user"
    assert data["tenant"]["code"] == tenant.code
    assert "assets.view_asset" in data["permissions"]


@pytest.mark.django_db(databases=["default"])
def test_logout_blacklists_refresh_token():
    user_model = get_user_model()
    user_model.objects.create_user(
        username="logout_user",
        email="logout_user@example.com",
        password="test-password",
    )

    client = APIClient()

    token_response = client.post(
        "/api/auth/token/",
        {
            "username": "logout_user",
            "password": "test-password",
        },
        format="json",
    )

    assert token_response.status_code == 200
    tokens = token_response.json()

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")

    logout_response = client.post(
        "/api/auth/logout/",
        {
            "refresh": tokens["refresh"],
        },
        format="json",
    )

    assert logout_response.status_code == 204