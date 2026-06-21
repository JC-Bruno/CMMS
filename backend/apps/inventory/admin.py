from django.contrib import admin

from .models import (
    InventoryLocation,
    SparePart,
    SparePartCategory,
    SparePartStock,
    StockMovement,
)


@admin.register(SparePartCategory)
class SparePartCategoryAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "name",
        "parent",
        "is_active",
        "deleted_at",
    ]
    search_fields = ["code", "name"]
    list_filter = ["is_active", "deleted_at"]


@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "name",
        "category",
        "status",
        "unit_of_measure",
        "minimum_stock",
        "reorder_point",
        "estimated_unit_cost",
    ]
    search_fields = [
        "code",
        "name",
        "manufacturer",
        "manufacturer_part_number",
    ]
    list_filter = ["status", "category", "deleted_at"]


@admin.register(InventoryLocation)
class InventoryLocationAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "name",
        "location_type",
        "parent",
        "is_active",
        "deleted_at",
    ]
    search_fields = ["code", "name"]
    list_filter = ["location_type", "is_active", "deleted_at"]


@admin.register(SparePartStock)
class SparePartStockAdmin(admin.ModelAdmin):
    list_display = [
        "spare_part",
        "location",
        "quantity_on_hand",
        "reserved_quantity",
        "available_quantity",
        "average_unit_cost",
        "last_movement_at",
    ]
    search_fields = [
        "spare_part__code",
        "spare_part__name",
        "location__code",
        "location__name",
    ]
    list_filter = ["location", "deleted_at"]


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = [
        "stock_item",
        "movement_type",
        "reason",
        "quantity",
        "quantity_before",
        "quantity_after",
        "movement_at",
        "created_by_name",
    ]
    search_fields = [
        "stock_item__spare_part__code",
        "stock_item__spare_part__name",
        "reference",
        "created_by_name",
    ]
    list_filter = ["movement_type", "reason", "movement_at"]