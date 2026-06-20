from django.db import transaction

from .models import (
    OperationalPermission,
    Role,
    RolePermission,
    TenantUser,
    TenantUserRole,
)


@transaction.atomic
def operational_permission_create(
    *,
    code,
    name,
    module,
    description="",
    is_active=True,
):
    permission = OperationalPermission(
        code=code,
        name=name,
        module=module,
        description=description,
        is_active=is_active,
    )
    permission.full_clean()
    permission.save()

    return permission


@transaction.atomic
def role_create(
    *,
    code,
    name,
    description="",
    is_system=False,
    is_active=True,
):
    role = Role(
        code=code,
        name=name,
        description=description,
        is_system=is_system,
        is_active=is_active,
    )
    role.full_clean()
    role.save()

    return role


@transaction.atomic
def role_assign_permission(*, role, permission):
    role_permission, _created = RolePermission.objects.get_or_create(
        role=role,
        permission=permission,
    )

    return role_permission


@transaction.atomic
def tenant_user_create(
    *,
    tenant,
    user,
    display_name="",
    is_active=True,
):
    tenant_user = TenantUser(
        tenant=tenant,
        user=user,
        display_name=display_name,
        is_active=is_active,
    )
    tenant_user.full_clean()
    tenant_user.save()

    return tenant_user


@transaction.atomic
def tenant_user_assign_role(*, tenant_user, role):
    tenant_user_role, _created = TenantUserRole.objects.get_or_create(
        tenant_user=tenant_user,
        role=role,
    )

    return tenant_user_role