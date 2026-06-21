from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import MaintenanceRequest
from .serializers import (
    MaintenanceRequestReasonSerializer,
    MaintenanceRequestSerializer,
)
from .services import (
    maintenance_request_cancel,
    maintenance_request_mark_received,
    maintenance_request_reject,
)


class MaintenanceRequestViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = MaintenanceRequestSerializer

    def get_queryset(self):
        return (
            MaintenanceRequest.objects.select_related("asset")
            .filter(deleted_at__isnull=True)
            .order_by("-created_at")
        )

    @action(detail=True, methods=["post"])
    def receive(self, request, pk=None):
        maintenance_request = self.get_object()
        maintenance_request = maintenance_request_mark_received(
            request=maintenance_request,
        )

        serializer = self.get_serializer(maintenance_request)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        maintenance_request = self.get_object()
        input_serializer = MaintenanceRequestReasonSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        maintenance_request = maintenance_request_reject(
            request=maintenance_request,
            reason=input_serializer.validated_data.get("reason", ""),
        )

        serializer = self.get_serializer(maintenance_request)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        maintenance_request = self.get_object()
        input_serializer = MaintenanceRequestReasonSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        maintenance_request = maintenance_request_cancel(
            request=maintenance_request,
            reason=input_serializer.validated_data.get("reason", ""),
        )

        serializer = self.get_serializer(maintenance_request)
        return Response(serializer.data, status=status.HTTP_200_OK)