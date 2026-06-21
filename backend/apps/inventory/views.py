from rest_framework import mixins, viewsets

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