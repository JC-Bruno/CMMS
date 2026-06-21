import uuid
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

from .choices import (
    InventoryLocationType,
    SparePartStatus,
    StockMovementReason,
    StockMovementType,
)


inventory_code_validator = RegexValidator(
    regex=r"^[A-Za-z0-9][A-Za-z0-9._-]*$",
    message=(
        "Code must start with a letter or number and may contain letters, "
        "numbers, dots, underscores, or hyphens."
    ),
)


class SparePartCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(
        max_length=50,
        validators=[inventory_code_validator],
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["code"]
        constraints = [
            models.UniqueConstraint(
                fields=["code"],
                condition=models.Q(deleted_at__isnull=True),
                name="unique_active_spare_part_category_code",
            )
        ]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["name"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["deleted_at"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


class SparePart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(
        max_length=80,
        validators=[inventory_code_validator],
        help_text="Internal spare part code.",
    )
    name = models.CharField(max_length=180)
    category = models.ForeignKey(
        SparePartCategory,
        on_delete=models.PROTECT,
        related_name="spare_parts",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=SparePartStatus.choices,
        default=SparePartStatus.ACTIVE,
    )
    description = models.TextField(blank=True)
    manufacturer = models.CharField(max_length=120, blank=True)
    manufacturer_part_number = models.CharField(max_length=120, blank=True)
    unit_of_measure = models.CharField(max_length=30, default="unit")
    minimum_stock = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    maximum_stock = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    reorder_point = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    estimated_unit_cost = models.DecimalField(
        max_digits=14,
        decimal_places=4,
        null=True,
        blank=True,
    )
    notes = models.TextField(blank=True)
    extra_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["code"]
        constraints = [
            models.UniqueConstraint(
                fields=["code"],
                condition=models.Q(deleted_at__isnull=True),
                name="unique_active_spare_part_code",
            )
        ]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["name"]),
            models.Index(fields=["status"]),
            models.Index(fields=["category"]),
            models.Index(fields=["deleted_at"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"

    def clean(self):
        super().clean()

        if self.minimum_stock < 0:
            raise ValidationError({"minimum_stock": "Minimum stock cannot be negative."})

        if self.reorder_point < 0:
            raise ValidationError({"reorder_point": "Reorder point cannot be negative."})

        if self.maximum_stock is not None and self.maximum_stock < self.minimum_stock:
            raise ValidationError(
                {"maximum_stock": "Maximum stock cannot be lower than minimum stock."}
            )

        if self.estimated_unit_cost is not None and self.estimated_unit_cost < 0:
            raise ValidationError(
                {"estimated_unit_cost": "Estimated unit cost cannot be negative."}
            )


class InventoryLocation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(
        max_length=80,
        validators=[inventory_code_validator],
    )
    name = models.CharField(max_length=180)
    location_type = models.CharField(
        max_length=30,
        choices=InventoryLocationType.choices,
        default=InventoryLocationType.WAREHOUSE,
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        null=True,
        blank=True,
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    extra_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["code"]
        constraints = [
            models.UniqueConstraint(
                fields=["code"],
                condition=models.Q(deleted_at__isnull=True),
                name="unique_active_inventory_location_code",
            )
        ]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["name"]),
            models.Index(fields=["location_type"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["deleted_at"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"

    def clean(self):
        super().clean()

        if self.parent_id == self.id:
            raise ValidationError({"parent": "Location cannot be its own parent."})


class SparePartStock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    spare_part = models.ForeignKey(
        SparePart,
        on_delete=models.PROTECT,
        related_name="stock_items",
    )
    location = models.ForeignKey(
        InventoryLocation,
        on_delete=models.PROTECT,
        related_name="stock_items",
    )
    quantity_on_hand = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    reserved_quantity = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    average_unit_cost = models.DecimalField(
        max_digits=14,
        decimal_places=4,
        null=True,
        blank=True,
    )
    last_movement_at = models.DateTimeField(null=True, blank=True)
    extra_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["spare_part__code", "location__code"]
        constraints = [
            models.UniqueConstraint(
                fields=["spare_part", "location"],
                condition=models.Q(deleted_at__isnull=True),
                name="unique_active_spare_part_stock_location",
            )
        ]
        indexes = [
            models.Index(fields=["spare_part"]),
            models.Index(fields=["location"]),
            models.Index(fields=["quantity_on_hand"]),
            models.Index(fields=["deleted_at"]),
        ]

    def __str__(self):
        return f"{self.spare_part.code} @ {self.location.code}: {self.quantity_on_hand}"

    @property
    def available_quantity(self):
        return self.quantity_on_hand - self.reserved_quantity

    def clean(self):
        super().clean()

        if self.spare_part_id and self.spare_part.deleted_at is not None:
            raise ValidationError(
                {"spare_part": "Stock cannot be linked to a deleted spare part."}
            )

        if self.location_id and self.location.deleted_at is not None:
            raise ValidationError(
                {"location": "Stock cannot be linked to a deleted inventory location."}
            )

        if self.quantity_on_hand < 0:
            raise ValidationError(
                {"quantity_on_hand": "Quantity on hand cannot be negative."}
            )

        if self.reserved_quantity < 0:
            raise ValidationError(
                {"reserved_quantity": "Reserved quantity cannot be negative."}
            )

        if self.reserved_quantity > self.quantity_on_hand:
            raise ValidationError(
                {"reserved_quantity": "Reserved quantity cannot exceed quantity on hand."}
            )

        if self.average_unit_cost is not None and self.average_unit_cost < 0:
            raise ValidationError(
                {"average_unit_cost": "Average unit cost cannot be negative."}
            )


class StockMovement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stock_item = models.ForeignKey(
        SparePartStock,
        on_delete=models.PROTECT,
        related_name="movements",
    )
    movement_type = models.CharField(
        max_length=30,
        choices=StockMovementType.choices,
    )
    reason = models.CharField(
        max_length=40,
        choices=StockMovementReason.choices,
        default=StockMovementReason.OTHER,
    )
    quantity = models.DecimalField(max_digits=14, decimal_places=2)
    quantity_before = models.DecimalField(max_digits=14, decimal_places=2)
    quantity_after = models.DecimalField(max_digits=14, decimal_places=2)
    reference = models.CharField(
        max_length=120,
        blank=True,
        help_text="Purchase order, adjustment reference, or external document.",
    )
    notes = models.TextField(blank=True)
    created_by_user_id = models.PositiveBigIntegerField(null=True, blank=True)
    created_by_name = models.CharField(max_length=150, blank=True)
    movement_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-movement_at", "-created_at"]
        indexes = [
            models.Index(fields=["stock_item"]),
            models.Index(fields=["movement_type"]),
            models.Index(fields=["reason"]),
            models.Index(fields=["movement_at"]),
            models.Index(fields=["created_by_user_id"]),
        ]

    def __str__(self):
        return f"{self.stock_item} - {self.movement_type} - {self.quantity}"

    def clean(self):
        super().clean()

        if self.quantity <= 0:
            raise ValidationError({"quantity": "Movement quantity must be greater than zero."})

        if self.quantity_before < 0:
            raise ValidationError(
                {"quantity_before": "Quantity before cannot be negative."}
            )

        if self.quantity_after < 0:
            raise ValidationError(
                {"quantity_after": "Quantity after cannot be negative."}
            )