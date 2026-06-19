from .models import Tenant


def tenant_list(*, include_deleted=False):
    queryset = Tenant.objects.all()

    if not include_deleted:
        queryset = queryset.filter(deleted_at__isnull=True)

    return queryset.order_by("name")


def tenant_get_by_code(*, code):
    return Tenant.objects.filter(
        code=code,
        deleted_at__isnull=True,
    ).first()