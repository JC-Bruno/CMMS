from rest_framework.routers import DefaultRouter

from .views import WorkOrderViewSet


app_name = "work_orders"

router = DefaultRouter()
router.register("items", WorkOrderViewSet, basename="work-order")

urlpatterns = router.urls