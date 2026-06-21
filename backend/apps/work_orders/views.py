from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.accounts.permissions import HasOperationalPermission

from .assignments import work_order_assign_technician
from .labor import work_order_labor_entry_create
from .models import WorkOrder
from .serializers import (
    WorkOrderAssignTechnicianSerializer,
    WorkOrderCreateManualSerializer,
    WorkOrderFromRequestSerializer,
    WorkOrderLaborCreateSerializer,
    WorkOrderReasonSerializer,
    WorkOrderSerializer,
    WorkOrderTechnicalCloseSerializer,
)
from .transitions import (
    work_order_cancel,
    work_order_close_final,
    work_order_put_on_hold,
    work_order_start,
    work_order_technical_close,
)


class WorkOrderViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = WorkOrderSerializer
    permission_classes = [HasOperationalPermission]
    permission_required_by_action = {
        "list": "work_orders.view_work_order",
        "retrieve": "work_orders.view_work_order",
        "create": "work_orders.create_work_order",
        "from_request": "maintenance_requests.convert_to_work_order",
        "assign_technician": "work_orders.assign_technician",
        "start": "work_orders.start_work_order",
        "put_on_hold": "work_orders.put_on_hold",
        "technical_close": "work_orders.technical_close",
        "close_final": "work_orders.final_close",
        "cancel": "work_orders.cancel_work_order",
        "labor_entries": "work_orders.add_labor_entry",
    }

    def get_queryset(self):
        return (
            WorkOrder.objects.select_related("asset", "source_request")
            .prefetch_related("assignees", "labor_entries")
            .filter(deleted_at__isnull=True)
            .order_by("-created_at")
        )

    def get_serializer_class(self):
        if self.action == "create":
            return WorkOrderCreateManualSerializer

        return WorkOrderSerializer

    def create(self, request, *args, **kwargs):
        input_serializer = self.get_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        work_order = input_serializer.save()

        output_serializer = WorkOrderSerializer(work_order)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path="from-request")
    def from_request(self, request):
        input_serializer = WorkOrderFromRequestSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        work_order = input_serializer.save()

        output_serializer = WorkOrderSerializer(work_order)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="assign-technician")
    def assign_technician(self, request, pk=None):
        work_order = self.get_object()

        input_serializer = WorkOrderAssignTechnicianSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        work_order_assign_technician(
            work_order=work_order,
            technician_user_id=input_serializer.validated_data["technician_user_id"],
            technician_name=input_serializer.validated_data["technician_name"],
            technician_email=input_serializer.validated_data.get("technician_email", ""),
            is_primary=input_serializer.validated_data.get("is_primary", False),
        )

        work_order.refresh_from_db()

        output_serializer = WorkOrderSerializer(work_order)
        return Response(output_serializer.data)

    @action(detail=True, methods=["post"])
    def start(self, request, pk=None):
        work_order = self.get_object()
        work_order = work_order_start(work_order=work_order)

        output_serializer = WorkOrderSerializer(work_order)
        return Response(output_serializer.data)

    @action(detail=True, methods=["post"], url_path="put-on-hold")
    def put_on_hold(self, request, pk=None):
        work_order = self.get_object()

        input_serializer = WorkOrderReasonSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        work_order = work_order_put_on_hold(
            work_order=work_order,
            reason=input_serializer.validated_data.get("reason", ""),
        )

        output_serializer = WorkOrderSerializer(work_order)
        return Response(output_serializer.data)

    @action(detail=True, methods=["post"], url_path="technical-close")
    def technical_close(self, request, pk=None):
        work_order = self.get_object()

        input_serializer = WorkOrderTechnicalCloseSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        work_order = work_order_technical_close(
            work_order=work_order,
            diagnosis=input_serializer.validated_data["diagnosis"],
            work_performed=input_serializer.validated_data["work_performed"],
            probable_cause=input_serializer.validated_data.get("probable_cause", ""),
            observations=input_serializer.validated_data.get("observations", ""),
            evidence_uri=input_serializer.validated_data.get("evidence_uri", ""),
            closed_by_user_id=input_serializer.validated_data.get("closed_by_user_id"),
            closed_by_name=input_serializer.validated_data.get("closed_by_name", ""),
        )

        output_serializer = WorkOrderSerializer(work_order)
        return Response(output_serializer.data)

    @action(detail=True, methods=["post"], url_path="close-final")
    def close_final(self, request, pk=None):
        work_order = self.get_object()
        work_order = work_order_close_final(work_order=work_order)

        output_serializer = WorkOrderSerializer(work_order)
        return Response(output_serializer.data)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        work_order = self.get_object()

        input_serializer = WorkOrderReasonSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        work_order = work_order_cancel(
            work_order=work_order,
            reason=input_serializer.validated_data.get("reason", ""),
        )

        output_serializer = WorkOrderSerializer(work_order)
        return Response(output_serializer.data)

    @action(detail=True, methods=["post"], url_path="labor-entries")
    def labor_entries(self, request, pk=None):
        work_order = self.get_object()

        input_serializer = WorkOrderLaborCreateSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        work_order_labor_entry_create(
            work_order=work_order,
            technician_user_id=input_serializer.validated_data["technician_user_id"],
            technician_name=input_serializer.validated_data["technician_name"],
            started_at=input_serializer.validated_data["started_at"],
            ended_at=input_serializer.validated_data["ended_at"],
            notes=input_serializer.validated_data.get("notes", ""),
        )

        work_order.refresh_from_db()

        output_serializer = WorkOrderSerializer(work_order)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)