from django.db import transaction

from .models import Tenant, TenantStatus


@transaction.atomic
def tenant_create(
    *,
    code,
    name,
    database_name,
    legal_name="",
    tax_id="",
    database_host="localhost",
    database_port=5433,
    status=TenantStatus.PROVISIONING,
):
    tenant = Tenant(
        code=code,
        name=name,
        legal_name=legal_name,
        tax_id=tax_id,
        status=status,
        database_name=database_name,
        database_host=database_host,
        database_port=database_port,
    )
    tenant.full_clean()
    tenant.save()

    return tenant


@transaction.atomic
def tenant_activate(*, tenant):
    tenant.status = TenantStatus.ACTIVE
    tenant.full_clean()
    tenant.save(update_fields=["status", "updated_at"])

    return tenant