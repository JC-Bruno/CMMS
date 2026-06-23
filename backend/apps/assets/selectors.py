from .models import Asset, AssetDocument, AssetLocationNode
from apps.assets.models import AssetStructureNode

def location_node_list(*, include_deleted=False):
    queryset = AssetLocationNode.objects.all()

    if not include_deleted:
        queryset = queryset.filter(deleted_at__isnull=True)

    return queryset.order_by("node_type", "name")


def location_node_get_by_code(*, code):
    return AssetLocationNode.objects.filter(
        code=code,
        deleted_at__isnull=True,
    ).first()


def location_node_children(*, parent, include_deleted=False):
    queryset = AssetLocationNode.objects.filter(parent=parent)

    if not include_deleted:
        queryset = queryset.filter(deleted_at__isnull=True)

    return queryset.order_by("node_type", "name")


def asset_list(*, include_deleted=False):
    queryset = Asset.objects.select_related(
        "location",
        "parent_asset",
    )

    if not include_deleted:
        queryset = queryset.filter(deleted_at__isnull=True)

    return queryset.order_by("code")


def asset_get_by_code(*, code):
    return (
        Asset.objects.select_related(
            "location",
            "parent_asset",
        )
        .filter(
            code=code,
            deleted_at__isnull=True,
        )
        .first()
    )


def asset_document_list(*, asset, include_deleted=False):
    queryset = AssetDocument.objects.filter(asset=asset)

    if not include_deleted:
        queryset = queryset.filter(deleted_at__isnull=True)

    return queryset.order_by("document_type", "title")

def asset_structure_node_list():
    return (
        AssetStructureNode.objects.select_related(
            "asset",
            "parent",
        )
        .filter(deleted_at__isnull=True)
        .order_by("asset__code", "sort_order", "code")
    )