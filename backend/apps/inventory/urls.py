from rest_framework.routers import DefaultRouter

from .views import (
    InventoryLocationViewSet,
    SparePartCategoryViewSet,
    SparePartStockViewSet,
    SparePartViewSet,
    StockMovementViewSet,
)


app_name = "inventory"

router = DefaultRouter()
router.register("categories", SparePartCategoryViewSet, basename="spare-part-category")
router.register("spare-parts", SparePartViewSet, basename="spare-part")
router.register("locations", InventoryLocationViewSet, basename="inventory-location")
router.register("stock", SparePartStockViewSet, basename="spare-part-stock")
router.register("movements", StockMovementViewSet, basename="stock-movement")

urlpatterns = router.urls