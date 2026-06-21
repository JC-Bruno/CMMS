from rest_framework.permissions import BasePermission

from apps.accounts.selectors import tenant_user_permission_codes
from apps.tenancy.selectors import tenant_get_by_code


TENANT_HEADER = "X-CMMS-Tenant-Code"


def get_tenant_code_from_request(request):
    return request.headers.get(TENANT_HEADER)


def get_request_tenant(request):
    tenant_code = get_tenant_code_from_request(request)

    if not tenant_code:
        return None

    return tenant_get_by_code(code=tenant_code)


def user_effective_permission_codes(*, user, tenant_code):
    if not user or not user.is_authenticated:
        return set()

    if user.is_superuser:
        return {"*"}

    if not tenant_code:
        return set()

    tenant = tenant_get_by_code(code=tenant_code)

    if tenant is None or not tenant.is_active:
        return set()

    return tenant_user_permission_codes(tenant=tenant, user=user)


def user_has_operational_permission(*, user, tenant_code, permission_code):
    permission_codes = user_effective_permission_codes(
        user=user,
        tenant_code=tenant_code,
    )

    return "*" in permission_codes or permission_code in permission_codes


class HasOperationalPermission(BasePermission):
    """
    Validates operational permissions for DRF ViewSets.

    Each protected ViewSet must define:

    permission_required_by_action = {
        "list": "assets.view_asset",
        "retrieve": "assets.view_asset",
        "create": "assets.create_asset",
    }
    """

    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        action = getattr(view, "action", None)
        permission_map = getattr(view, "permission_required_by_action", {})
        permission_code = permission_map.get(action)

        if permission_code is None:
            return False

        tenant_code = get_tenant_code_from_request(request)

        return user_has_operational_permission(
            user=request.user,
            tenant_code=tenant_code,
            permission_code=permission_code,
        )