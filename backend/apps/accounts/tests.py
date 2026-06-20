import pytest

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from apps.tenancy.services import tenant_create

from .models import OperationalPermissionModule
from .selectors import tenant_user_permission_codes
from .services import (
    operational_permission_create,
    role_assign_permission,
    role_create,
    tenant_user_assign_role,
    tenant_user_create,
)


@pytest.mark.django_db
def test_role_permission_assignment_gives_effective_permission_to_tenant_user():
    user = get_user_model().objects.create_user(
        username="technician",
        password="test-password",
    )
    tenant = tenant_create(
        code="monelca",
        name="Grupo Monelca",
        database_name="cmms_client_monelca",
    )
    permission = operational_permission_create(
        code="work_orders.start",
        name="Start work orders",
        module=OperationalPermissionModule.WORK_ORDERS,
    )
    role = role_create(
        code="maintenance_technician",
        name="Maintenance Technician",
    )
    tenant_user = tenant_user_create(
        tenant=tenant,
        user=user,
        display_name="Technician User",
    )

    role_assign_permission(
        role=role,
        permission=permission,
    )
    tenant_user_assign_role(
        tenant_user=tenant_user,
        role=role,
    )

    assert tenant_user_permission_codes(
        tenant=tenant,
        user=user,
    ) == {"work_orders.start"}


@pytest.mark.django_db
def test_user_without_tenant_membership_has_no_effective_permissions():
    user = get_user_model().objects.create_user(
        username="external",
        password="test-password",
    )
    tenant = tenant_create(
        code="monelca",
        name="Grupo Monelca",
        database_name="cmms_client_monelca",
    )

    assert tenant_user_permission_codes(
        tenant=tenant,
        user=user,
    ) == set()


@pytest.mark.django_db
def test_inactive_role_does_not_grant_permission():
    user = get_user_model().objects.create_user(
        username="planner",
        password="test-password",
    )
    tenant = tenant_create(
        code="monelca",
        name="Grupo Monelca",
        database_name="cmms_client_monelca",
    )
    permission = operational_permission_create(
        code="work_orders.assign",
        name="Assign work orders",
        module=OperationalPermissionModule.WORK_ORDERS,
    )
    role = role_create(
        code="maintenance_planner",
        name="Maintenance Planner",
        is_active=False,
    )
    tenant_user = tenant_user_create(
        tenant=tenant,
        user=user,
    )

    role_assign_permission(
        role=role,
        permission=permission,
    )
    tenant_user_assign_role(
        tenant_user=tenant_user,
        role=role,
    )

    assert tenant_user_permission_codes(
        tenant=tenant,
        user=user,
    ) == set()


@pytest.mark.django_db
def test_permission_code_rejects_invalid_format():
    with pytest.raises(ValidationError):
        operational_permission_create(
            code="Work Orders Start",
            name="Invalid Permission",
            module=OperationalPermissionModule.WORK_ORDERS,
        )