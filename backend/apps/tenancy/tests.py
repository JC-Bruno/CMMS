import pytest

from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Tenant, TenantStatus
from .selectors import tenant_get_by_code, tenant_list
from .services import tenant_activate, tenant_create


@pytest.mark.django_db
def test_tenant_create_defaults_to_provisioning_status():
    tenant = tenant_create(
        code="monelca",
        name="Grupo Monelca",
        database_name="cmms_client_monelca",
    )

    assert tenant.code == "monelca"
    assert tenant.name == "Grupo Monelca"
    assert tenant.database_name == "cmms_client_monelca"
    assert tenant.status == TenantStatus.PROVISIONING
    assert tenant.is_active is False
    assert str(tenant) == "Grupo Monelca (monelca)"


@pytest.mark.django_db
def test_tenant_activate_changes_status_to_active():
    tenant = tenant_create(
        code="monelca",
        name="Grupo Monelca",
        database_name="cmms_client_monelca",
    )

    tenant_activate(tenant=tenant)

    tenant.refresh_from_db()

    assert tenant.status == TenantStatus.ACTIVE
    assert tenant.is_active is True


@pytest.mark.django_db
def test_tenant_database_name_rejects_invalid_format():
    tenant = Tenant(
        code="bad-db",
        name="Bad Database",
        database_name="CMMS Bad Name",
    )

    with pytest.raises(ValidationError):
        tenant.full_clean()


@pytest.mark.django_db
def test_tenant_selectors_ignore_soft_deleted_records():
    active_tenant = tenant_create(
        code="active-client",
        name="Active Client",
        database_name="cmms_client_active",
    )
    deleted_tenant = tenant_create(
        code="deleted-client",
        name="Deleted Client",
        database_name="cmms_client_deleted",
    )

    deleted_tenant.deleted_at = timezone.now()
    deleted_tenant.save(update_fields=["deleted_at", "updated_at"])

    assert tenant_get_by_code(code="active-client") == active_tenant
    assert tenant_get_by_code(code="deleted-client") is None
    assert list(tenant_list()) == [active_tenant]