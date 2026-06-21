from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import (
    get_request_tenant,
    get_tenant_code_from_request,
    user_effective_permission_codes,
)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tenant = get_request_tenant(request)
        tenant_code = get_tenant_code_from_request(request)

        permissions = sorted(
            user_effective_permission_codes(
                user=request.user,
                tenant_code=tenant_code,
            )
        )

        tenant_data = None

        if tenant is not None:
            tenant_data = {
                "id": str(tenant.id),
                "code": tenant.code,
                "name": tenant.name,
                "status": tenant.status,
                "is_active": tenant.is_active,
            }

        return Response(
            {
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "is_superuser": request.user.is_superuser,
                "tenant": tenant_data,
                "permissions": permissions,
            }
        )