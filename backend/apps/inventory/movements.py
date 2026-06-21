from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from .choices import StockMovementReason, StockMovementType
from .models import SparePartStock, StockMovement


INCREASE_MOVEMENT_TYPES = {
    StockMovementType.INITIAL_BALANCE,
    StockMovementType.RECEIPT,
    StockMovementType.RETURN,
    StockMovementType.ADJUSTMENT_IN,
}

DECREASE_MOVEMENT_TYPES = {
    StockMovementType.ISSUE,
    StockMovementType.ADJUSTMENT_OUT,
}


@transaction.atomic(using="client_template")
def stock_movement_create(
    *,
    stock_item,
    movement_type,
    quantity,
    reason=StockMovementReason.OTHER,
    reference="",
    notes="",
    created_by_user_id=None,
    created_by_name="",
    movement_at=None,
):
    quantity = Decimal(str(quantity))

    if quantity <= 0:
        raise ValidationError({"quantity": "Movement quantity must be greater than zero."})

    stock_item = SparePartStock.objects.select_for_update().get(id=stock_item.id)

    quantity_before = stock_item.quantity_on_hand

    if movement_type in INCREASE_MOVEMENT_TYPES:
        quantity_after = quantity_before + quantity
    elif movement_type in DECREASE_MOVEMENT_TYPES:
        quantity_after = quantity_before - quantity
    else:
        raise ValidationError({"movement_type": "Unsupported movement type."})

    if quantity_after < 0:
        raise ValidationError(
            {"quantity": "Movement would make stock quantity negative."}
        )

    movement_time = movement_at or timezone.now()

    movement = StockMovement(
        stock_item=stock_item,
        movement_type=movement_type,
        reason=reason,
        quantity=quantity,
        quantity_before=quantity_before,
        quantity_after=quantity_after,
        reference=reference,
        notes=notes,
        created_by_user_id=created_by_user_id,
        created_by_name=created_by_name,
        movement_at=movement_time,
    )
    movement.full_clean()
    movement.save()

    stock_item.quantity_on_hand = quantity_after
    stock_item.last_movement_at = movement_time
    stock_item.full_clean()
    stock_item.save(
        update_fields=[
            "quantity_on_hand",
            "last_movement_at",
            "updated_at",
        ]
    )

    return movement