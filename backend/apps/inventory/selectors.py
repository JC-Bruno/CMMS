from django.db import models
from .models import (
    InventoryLocation,
    SparePart,
    SparePartCategory,
    SparePartStock,
    StockMovement,
)


def spare_part_category_list(*, include_deleted=False):
    queryset = SparePartCategory.objects.all()

    if not include_deleted:
        queryset = queryset.filter(deleted_at__isnull=True)

    return queryset.order_by("code")


def spare_part_list(*, include_deleted=False):
    queryset = SparePart.objects.select_related("category")

    if not include_deleted:
        queryset = queryset.filter(deleted_at__isnull=True)

    return queryset.order_by("code")


def spare_part_get_by_code(*, code):
    return (
        SparePart.objects.select_related("category")
        .filter(code=code, deleted_at__isnull=True)
        .first()
    )


def inventory_location_list(*, include_deleted=False):
    queryset = InventoryLocation.objects.select_related("parent")

    if not include_deleted:
        queryset = queryset.filter(deleted_at__isnull=True)

    return queryset.order_by("code")


def inventory_location_get_by_code(*, code):
    return (
        InventoryLocation.objects.select_related("parent")
        .filter(code=code, deleted_at__isnull=True)
        .first()
    )


def stock_list(*, include_deleted=False):
    queryset = SparePartStock.objects.select_related("spare_part", "location")

    if not include_deleted:
        queryset = queryset.filter(deleted_at__isnull=True)

    return queryset.order_by("spare_part__code", "location__code")


def stock_get(*, spare_part, location):
    return (
        SparePartStock.objects.select_related("spare_part", "location")
        .filter(
            spare_part=spare_part,
            location=location,
            deleted_at__isnull=True,
        )
        .first()
    )


def stock_movement_list_by_stock_item(*, stock_item):
    return StockMovement.objects.filter(stock_item=stock_item).order_by(
        "-movement_at",
        "-created_at",
    )


def spare_part_list_below_reorder_point():
    return (
        SparePartStock.objects.select_related("spare_part", "location")
        .filter(
            deleted_at__isnull=True,
            spare_part__deleted_at__isnull=True,
            spare_part__status="active",
            quantity_on_hand__lte=models.F("spare_part__reorder_point"),
        )
        .order_by("spare_part__code", "location__code")
    )