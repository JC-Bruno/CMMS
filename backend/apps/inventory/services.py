from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from .choices import SparePartStatus
from .models import (
    InventoryLocation,
    SparePart,
    SparePartCategory,
    SparePartStock,
)


@transaction.atomic(using="client_template")
def spare_part_category_create(
    *,
    code,
    name,
    description="",
    parent=None,
):
    category = SparePartCategory(
        code=code,
        name=name,
        description=description,
        parent=parent,
    )
    category.full_clean()
    category.save()

    return category


@transaction.atomic(using="client_template")
def spare_part_create(
    *,
    code,
    name,
    category=None,
    status=SparePartStatus.ACTIVE,
    description="",
    manufacturer="",
    manufacturer_part_number="",
    unit_of_measure="unit",
    minimum_stock=Decimal("0.00"),
    maximum_stock=None,
    reorder_point=Decimal("0.00"),
    estimated_unit_cost=None,
    notes="",
    extra_data=None,
):
    spare_part = SparePart(
        code=code,
        name=name,
        category=category,
        status=status,
        description=description,
        manufacturer=manufacturer,
        manufacturer_part_number=manufacturer_part_number,
        unit_of_measure=unit_of_measure,
        minimum_stock=minimum_stock,
        maximum_stock=maximum_stock,
        reorder_point=reorder_point,
        estimated_unit_cost=estimated_unit_cost,
        notes=notes,
        extra_data=extra_data or {},
    )
    spare_part.full_clean()
    spare_part.save()

    return spare_part


@transaction.atomic(using="client_template")
def inventory_location_create(
    *,
    code,
    name,
    location_type,
    parent=None,
    description="",
    extra_data=None,
):
    location = InventoryLocation(
        code=code,
        name=name,
        location_type=location_type,
        parent=parent,
        description=description,
        extra_data=extra_data or {},
    )
    location.full_clean()
    location.save()

    return location


@transaction.atomic(using="client_template")
def stock_create(
    *,
    spare_part,
    location,
    quantity_on_hand=Decimal("0.00"),
    reserved_quantity=Decimal("0.00"),
    average_unit_cost=None,
    extra_data=None,
):
    stock_item = SparePartStock(
        spare_part=spare_part,
        location=location,
        quantity_on_hand=quantity_on_hand,
        reserved_quantity=reserved_quantity,
        average_unit_cost=average_unit_cost,
        last_movement_at=timezone.now() if quantity_on_hand else None,
        extra_data=extra_data or {},
    )
    stock_item.full_clean()
    stock_item.save()

    return stock_item


@transaction.atomic(using="client_template")
def spare_part_soft_delete(*, spare_part):
    spare_part.deleted_at = timezone.now()
    spare_part.save(update_fields=["deleted_at", "updated_at"])

    return spare_part


@transaction.atomic(using="client_template")
def inventory_location_soft_delete(*, location):
    location.deleted_at = timezone.now()
    location.save(update_fields=["deleted_at", "updated_at"])

    return location