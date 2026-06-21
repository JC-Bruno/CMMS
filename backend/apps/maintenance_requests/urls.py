from rest_framework.routers import DefaultRouter

from .views import MaintenanceRequestViewSet


app_name = "maintenance_requests"

router = DefaultRouter()
router.register("requests", MaintenanceRequestViewSet, basename="maintenance-request")

urlpatterns = router.urls