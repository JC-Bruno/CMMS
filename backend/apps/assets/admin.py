from django.contrib import admin
from apps.assets.models import AssetStructureNode
from .models import Asset, AssetDocument, AssetLocationNode


@admin.register(AssetLocationNode)
class AssetLocationNodeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "node_type",
        "parent",
        "is_active",
        "created_at",
    )
    list_filter = (
        "node_type",
        "is_active",
    )
    search_fields = (
        "code",
        "name",
        "description",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


class AssetDocumentInline(admin.TabularInline):
    model = AssetDocument
    extra = 0
    fields = (
        "document_type",
        "title",
        "document_uri",
        "issued_at",
        "deleted_at",
    )


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "asset_type",
        "status",
        "criticality",
        "location",
        "is_maintainable",
        "created_at",
    )
    list_filter = (
        "asset_type",
        "status",
        "criticality",
        "is_maintainable",
    )
    search_fields = (
        "code",
        "name",
        "manufacturer",
        "model",
        "serial_number",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    inlines = [
        AssetDocumentInline,
    ]


@admin.register(AssetDocument)
class AssetDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "asset",
        "document_type",
        "title",
        "document_uri",
        "issued_at",
        "created_at",
    )
    list_filter = (
        "document_type",
    )
    search_fields = (
        "asset__code",
        "asset__name",
        "title",
        "document_uri",
        "description",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

@admin.register(AssetStructureNode)
class AssetStructureNodeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "asset",
        "parent",
        "node_type",
        "is_maintainable",
        "sort_order",
    )
    list_filter = ("node_type", "is_maintainable", "asset")
    search_fields = ("code", "name", "asset__code", "asset__name")
    ordering = ("asset__code", "sort_order", "code")