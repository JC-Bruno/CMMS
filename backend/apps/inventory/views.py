from rest_framework import mixins, viewsets

from apps.accounts.permissions import HasOperationalPermission

from .models import (
    InventoryLocation,
    SparePart,
    SparePartCategory,
    SparePartStock,
    StockMovement,
)
from .serializers import (
    InventoryLocationSerializer,
    SparePartCategorySerializer,
    SparePartSerializer,
    SparePartStockSerializer,
    StockMovementSerializer,
)


class SparePartCategoryViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = SparePartCategorySerializer
    permission_classes = [HasOperationalPermission]
    permission_required_by_action = {
        "list": "inventory.view_spare_part",
        "retrieve": "inventory.view_spare_part",
        "create": "inventory.create_spare_part",
    }

    def get_queryset(self):
        return (
            SparePartCategory.objects.select_related("parent")
            .filter(deleted_at__isnull=True)
            .order_by("code")
        )


class SparePartViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = SparePartSerializer
    permission_classes = [HasOperationalPermission]
    permission_required_by_action = {
        "list": "inventory.view_spare_part",
        "retrieve": "inventory.view_spare_part",
        "create": "inventory.create_spare_part",
    }

    def get_queryset(self):
        return (
            SparePart.objects.select_related("category")
            .filter(deleted_at__isnull=True)
            .order_by("code")
        )


class InventoryLocationViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = InventoryLocationSerializer
    permission_classes = [HasOperationalPermission]
    permission_required_by_action = {
        "list": "inventory.view_inventory_location",
        "retrieve": "inventory.view_inventory_location",
        "create": "inventory.create_inventory_location",
    }

    def get_queryset(self):
        return (
            InventoryLocation.objects.select_related("parent")
            .filter(deleted_at__isnull=True)
            .order_by("code")
        )


class SparePartStockViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = SparePartStockSerializer
    permission_classes = [HasOperationalPermission]
    permission_required_by_action = {
        "list": "inventory.view_stock",
        "retrieve": "inventory.view_stock",
        "create": "inventory.create_stock",
    }

    def get_queryset(self):
        return (
            SparePartStock.objects.select_related("spare_part", "location")
            .filter(deleted_at__isnull=True)
            .order_by("spare_part__code", "location__code")
        )


class StockMovementViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = StockMovementSerializer
    permission_classes = [HasOperationalPermission]
    permission_required_by_action = {
        "list": "inventory.view_stock_movement",
        "retrieve": "inventory.view_stock_movement",
        "create": "inventory.create_stock_movement",
    }

    def get_queryset(self):
        return (
            StockMovement.objects.select_related(
                "stock_item",
                "stock_item__spare_part",
                "stock_item__location",
            )
            .all()
            .order_by("-movement_at", "-created_at")
        )