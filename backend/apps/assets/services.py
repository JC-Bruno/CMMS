from django.db import transaction
from django.utils import timezone

from .models import Asset, AssetDocument, AssetLocationNode


@transaction.atomic
def location_node_create(
    *,
    code,
    name,
    node_type,
    parent=None,
    description="",
    is_active=True,
):
    location_node = AssetLocationNode(
        code=code,
        name=name,
        node_type=node_type,
        parent=parent,
        description=description,
        is_active=is_active,
    )
    location_node.full_clean()
    location_node.save()

    return location_node


@transaction.atomic
def asset_create(
    *,
    code,
    name,
    location,
    asset_type,
    status,
    criticality,
    parent_asset=None,
    manufacturer="",
    model="",
    serial_number="",
    technical_specs=None,
    acquisition_date=None,
    installation_date=None,
    notes="",
    is_maintainable=True,
):
    asset = Asset(
        code=code,
        name=name,
        location=location,
        asset_type=asset_type,
        status=status,
        criticality=criticality,
        parent_asset=parent_asset,
        manufacturer=manufacturer,
        model=model,
        serial_number=serial_number,
        technical_specs=technical_specs or {},
        acquisition_date=acquisition_date,
        installation_date=installation_date,
        notes=notes,
        is_maintainable=is_maintainable,
    )
    asset.full_clean()
    asset.save()

    return asset


@transaction.atomic
def asset_document_create(
    *,
    asset,
    document_type,
    title,
    document_uri="",
    description="",
    issued_at=None,
):
    document = AssetDocument(
        asset=asset,
        document_type=document_type,
        title=title,
        document_uri=document_uri,
        description=description,
        issued_at=issued_at,
    )
    document.full_clean()
    document.save()

    return document


@transaction.atomic
def asset_soft_delete(*, asset):
    asset.deleted_at = timezone.now()
    asset.save(update_fields=["deleted_at", "updated_at"])

    return asset