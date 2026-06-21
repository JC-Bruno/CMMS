from rest_framework import serializers

from .models import (
    InventoryLocation,
    SparePart,
    SparePartCategory,
    SparePartStock,
    StockMovement,
)
from .movements import stock_movement_create
from .services import (
    inventory_location_create,
    spare_part_category_create,
    spare_part_create,
    stock_create,
)


class SparePartCategorySerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(
        source="parent",
        queryset=SparePartCategory.objects.filter(deleted_at__isnull=True),
        allow_null=True,
        required=False,
    )
    parent_code = serializers.CharField(source="parent.code", read_only=True)

    class Meta:
        model = SparePartCategory
        fields = [
            "id",
            "code",
            "name",
            "description",
            "parent_id",
            "parent_code",
            "is_active",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = [
            "id",
            "parent_code",
            "is_active",
            "created_at",
            "updated_at",
            "deleted_at",
        ]

    def create(self, validated_data):
        return spare_part_category_create(
            code=validated_data["code"],
            name=validated_data["name"],
            description=validated_data.get("description", ""),
            parent=validated_data.get("parent"),
        )


class SparePartSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        source="category",
        queryset=SparePartCategory.objects.filter(deleted_at__isnull=True),
        allow_null=True,
        required=False,
    )
    category_code = serializers.CharField(source="category.code", read_only=True)

    class Meta:
        model = SparePart
        fields = [
            "id",
            "code",
            "name",
            "category_id",
            "category_code",
            "status",
            "description",
            "manufacturer",
            "manufacturer_part_number",
            "unit_of_measure",
            "minimum_stock",
            "maximum_stock",
            "reorder_point",
            "estimated_unit_cost",
            "notes",
            "extra_data",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = [
            "id",
            "category_code",
            "created_at",
            "updated_at",
            "deleted_at",
        ]

    def create(self, validated_data):
        return spare_part_create(
            code=validated_data["code"],
            name=validated_data["name"],
            category=validated_data.get("category"),
            status=validated_data.get("status"),
            description=validated_data.get("description", ""),
            manufacturer=validated_data.get("manufacturer", ""),
            manufacturer_part_number=validated_data.get("manufacturer_part_number", ""),
            unit_of_measure=validated_data.get("unit_of_measure", "unit"),
            minimum_stock=validated_data.get("minimum_stock"),
            maximum_stock=validated_data.get("maximum_stock"),
            reorder_point=validated_data.get("reorder_point"),
            estimated_unit_cost=validated_data.get("estimated_unit_cost"),
            notes=validated_data.get("notes", ""),
            extra_data=validated_data.get("extra_data") or {},
        )


class InventoryLocationSerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(
        source="parent",
        queryset=InventoryLocation.objects.filter(deleted_at__isnull=True),
        allow_null=True,
        required=False,
    )
    parent_code = serializers.CharField(source="parent.code", read_only=True)

    class Meta:
        model = InventoryLocation
        fields = [
            "id",
            "code",
            "name",
            "location_type",
            "parent_id",
            "parent_code",
            "description",
            "is_active",
            "extra_data",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = [
            "id",
            "parent_code",
            "is_active",
            "created_at",
            "updated_at",
            "deleted_at",
        ]

    def create(self, validated_data):
        return inventory_location_create(
            code=validated_data["code"],
            name=validated_data["name"],
            location_type=validated_data["location_type"],
            parent=validated_data.get("parent"),
            description=validated_data.get("description", ""),
            extra_data=validated_data.get("extra_data") or {},
        )


class SparePartStockSerializer(serializers.ModelSerializer):
    spare_part_id = serializers.PrimaryKeyRelatedField(
        source="spare_part",
        queryset=SparePart.objects.filter(deleted_at__isnull=True),
    )
    spare_part_code = serializers.CharField(source="spare_part.code", read_only=True)
    spare_part_name = serializers.CharField(source="spare_part.name", read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(
        source="location",
        queryset=InventoryLocation.objects.filter(deleted_at__isnull=True),
    )
    location_code = serializers.CharField(source="location.code", read_only=True)
    available_quantity = serializers.DecimalField(
        max_digits=14,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = SparePartStock
        fields = [
            "id",
            "spare_part_id",
            "spare_part_code",
            "spare_part_name",
            "location_id",
            "location_code",
            "quantity_on_hand",
            "reserved_quantity",
            "available_quantity",
            "average_unit_cost",
            "last_movement_at",
            "extra_data",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = [
            "id",
            "spare_part_code",
            "spare_part_name",
            "location_code",
            "available_quantity",
            "last_movement_at",
            "created_at",
            "updated_at",
            "deleted_at",
        ]

    def create(self, validated_data):
        return stock_create(
            spare_part=validated_data["spare_part"],
            location=validated_data["location"],
            quantity_on_hand=validated_data.get("quantity_on_hand"),
            reserved_quantity=validated_data.get("reserved_quantity"),
            average_unit_cost=validated_data.get("average_unit_cost"),
            extra_data=validated_data.get("extra_data") or {},
        )


class StockMovementSerializer(serializers.ModelSerializer):
    stock_item_id = serializers.PrimaryKeyRelatedField(
        source="stock_item",
        queryset=SparePartStock.objects.filter(deleted_at__isnull=True),
    )
    spare_part_code = serializers.CharField(
        source="stock_item.spare_part.code",
        read_only=True,
    )
    location_code = serializers.CharField(
        source="stock_item.location.code",
        read_only=True,
    )

    class Meta:
        model = StockMovement
        fields = [
            "id",
            "stock_item_id",
            "spare_part_code",
            "location_code",
            "movement_type",
            "reason",
            "quantity",
            "quantity_before",
            "quantity_after",
            "reference",
            "notes",
            "created_by_user_id",
            "created_by_name",
            "movement_at",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "spare_part_code",
            "location_code",
            "quantity_before",
            "quantity_after",
            "movement_at",
            "created_at",
        ]

    def create(self, validated_data):
        return stock_movement_create(
            stock_item=validated_data["stock_item"],
            movement_type=validated_data["movement_type"],
            quantity=validated_data["quantity"],
            reason=validated_data.get("reason"),
            reference=validated_data.get("reference", ""),
            notes=validated_data.get("notes", ""),
            created_by_user_id=validated_data.get("created_by_user_id"),
            created_by_name=validated_data.get("created_by_name", ""),
        )