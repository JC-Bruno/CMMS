from rest_framework.routers import DefaultRouter
from apps.assets.views import AssetStructureNodeViewSet
from .views import AssetDocumentViewSet, AssetLocationNodeViewSet, AssetViewSet


app_name = "assets"

router = DefaultRouter()
router.register("locations", AssetLocationNodeViewSet, basename="asset-location")
router.register("items", AssetViewSet, basename="asset")
router.register("documents", AssetDocumentViewSet, basename="asset-document")
router.register(
    "structure-nodes",
    AssetStructureNodeViewSet,
    basename="asset-structure-node",
)
urlpatterns = router.urls