from decimal import Decimal
from uuid import uuid4

import pytest
from django.core.exceptions import ValidationError
from django.db import router

from .choices import (
    InventoryLocationType,
    SparePartStatus,
    StockMovementReason,
    StockMovementType,
)
from .models import SparePart, SparePartStock
from .movements import stock_movement_create
from .selectors import (
    inventory_location_get_by_code,
    spare_part_get_by_code,
    spare_part_list_below_reorder_point,
    stock_get,
)
from .services import (
    inventory_location_create,
    spare_part_category_create,
    spare_part_create,
    stock_create,
)


def _suffix():
    return uuid4().hex[:8]


def _create_stock_item(*, initial_quantity=Decimal("0.00"), reorder_point=Decimal("2.00")):
    suffix = _suffix()

    category = spare_part_category_create(
        code=f"bearings_{suffix}",
        name="Rodamientos",
    )
    spare_part = spare_part_create(
        code=f"BRG-6205-{suffix}",
        name="Rodamiento 6205",
        category=category,
        status=SparePartStatus.ACTIVE,
        unit_of_measure="unit",
        minimum_stock=Decimal("1.00"),
        reorder_point=reorder_point,
    )
    location = inventory_location_create(
        code=f"main_wh_{suffix}",
        name="Almacén principal",
        location_type=InventoryLocationType.WAREHOUSE,
    )

    return stock_create(
        spare_part=spare_part,
        location=location,
        quantity_on_hand=initial_quantity,
    )


@pytest.mark.django_db(databases=["client_template"])
def test_inventory_models_are_routed_to_client_template():
    assert router.allow_migrate_model("default", SparePart) is False
    assert router.allow_migrate_model("client_template", SparePart) is True
    assert router.allow_migrate_model("default", SparePartStock) is False
    assert router.allow_migrate_model("client_template", SparePartStock) is True


@pytest.mark.django_db(databases=["client_template"])
def test_spare_part_can_be_created_and_selected_by_code():
    suffix = _suffix()

    category = spare_part_category_create(
        code=f"electrical_{suffix}",
        name="Eléctricos",
    )
    spare_part = spare_part_create(
        code=f"FUSE-10A-{suffix}",
        name="Fusible 10A",
        category=category,
        manufacturer="Generic",
        manufacturer_part_number="F10A",
        reorder_point=Decimal("5.00"),
    )

    found = spare_part_get_by_code(code=spare_part.code)

    assert found == spare_part
    assert found.category == category


@pytest.mark.django_db(databases=["client_template"])
def test_inventory_location_can_be_created_and_selected_by_code():
    suffix = _suffix()

    location = inventory_location_create(
        code=f"rack_a1_{suffix}",
        name="Rack A1",
        location_type=InventoryLocationType.WAREHOUSE,
    )

    found = inventory_location_get_by_code(code=location.code)

    assert found == location


@pytest.mark.django_db(databases=["client_template"])
def test_stock_can_be_created_for_spare_part_and_location():
    stock_item = _create_stock_item(initial_quantity=Decimal("4.00"))

    found = stock_get(
        spare_part=stock_item.spare_part,
        location=stock_item.location,
    )

    assert found == stock_item
    assert found.quantity_on_hand == Decimal("4.00")


@pytest.mark.django_db(databases=["client_template"])
def test_receipt_movement_increases_stock():
    stock_item = _create_stock_item(initial_quantity=Decimal("2.00"))

    movement = stock_movement_create(
        stock_item=stock_item,
        movement_type=StockMovementType.RECEIPT,
        quantity=Decimal("3.00"),
        reason=StockMovementReason.PURCHASE,
        reference="PO-001",
        created_by_name="Almacén",
    )

    stock_item.refresh_from_db()

    assert movement.quantity_before == Decimal("2.00")
    assert movement.quantity_after == Decimal("5.00")
    assert stock_item.quantity_on_hand == Decimal("5.00")


@pytest.mark.django_db(databases=["client_template"])
def test_issue_movement_decreases_stock():
    stock_item = _create_stock_item(initial_quantity=Decimal("5.00"))

    movement = stock_movement_create(
        stock_item=stock_item,
        movement_type=StockMovementType.ISSUE,
        quantity=Decimal("2.00"),
        reason=StockMovementReason.MAINTENANCE_USE,
        reference="WO-TEST-001",
    )

    stock_item.refresh_from_db()

    assert movement.quantity_before == Decimal("5.00")
    assert movement.quantity_after == Decimal("3.00")
    assert stock_item.quantity_on_hand == Decimal("3.00")


@pytest.mark.django_db(databases=["client_template"])
def test_issue_movement_cannot_make_stock_negative():
    stock_item = _create_stock_item(initial_quantity=Decimal("1.00"))

    with pytest.raises(ValidationError):
        stock_movement_create(
            stock_item=stock_item,
            movement_type=StockMovementType.ISSUE,
            quantity=Decimal("2.00"),
            reason=StockMovementReason.MAINTENANCE_USE,
        )


@pytest.mark.django_db(databases=["client_template"])
def test_spare_part_below_reorder_point_selector():
    stock_item = _create_stock_item(
        initial_quantity=Decimal("1.00"),
        reorder_point=Decimal("2.00"),
    )

    queryset = spare_part_list_below_reorder_point()

    assert stock_item in list(queryset)


@pytest.mark.django_db(databases=["client_template"])
def test_negative_minimum_stock_is_invalid():
    suffix = _suffix()

    with pytest.raises(ValidationError):
        spare_part_create(
            code=f"INVALID-{suffix}",
            name="Invalid spare part",
            minimum_stock=Decimal("-1.00"),
        )