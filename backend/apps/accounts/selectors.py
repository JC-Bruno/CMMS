from .models import TenantUser


def tenant_user_get(*, tenant, user):
    return TenantUser.objects.filter(
        tenant=tenant,
        user=user,
        is_active=True,
        deleted_at__isnull=True,
    ).first()


def tenant_user_permission_codes(*, tenant, user):
    tenant_user = tenant_user_get(
        tenant=tenant,
        user=user,
    )

    if tenant_user is None:
        return set()

    permissions = (
        tenant_user.tenant_user_roles.filter(
            role__is_active=True,
            role__permissions__is_active=True,
        )
        .values_list(
            "role__permissions__code",
            flat=True,
        )
        .distinct()
    )

    return set(permissions)