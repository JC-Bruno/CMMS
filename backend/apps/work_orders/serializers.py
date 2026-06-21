from rest_framework import serializers

from apps.assets.models import Asset
from apps.maintenance_requests.models import MaintenanceRequest

from .models import (
    WorkOrder,
    WorkOrderAssignee,
    WorkOrderLaborEntry,
    WorkOrderTechnicalReport,
)
from .services import work_order_create_from_request, work_order_create_manual


class WorkOrderAssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderAssignee
        fields = [
            "id",
            "technician_user_id",
            "technician_name",
            "technician_email",
            "is_primary",
            "is_active",
            "assigned_at",
            "unassigned_at",
        ]


class WorkOrderLaborEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderLaborEntry
        fields = [
            "id",
            "technician_user_id",
            "technician_name",
            "started_at",
            "ended_at",
            "duration_minutes",
            "notes",
            "created_at",
        ]


class WorkOrderTechnicalReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderTechnicalReport
        fields = [
            "id",
            "diagnosis",
            "work_performed",
            "probable_cause",
            "observations",
            "evidence_uri",
            "closed_by_user_id",
            "closed_by_name",
            "created_at",
            "updated_at",
        ]


class WorkOrderSerializer(serializers.ModelSerializer):
    asset_id = serializers.UUIDField(source="asset.id", read_only=True)
    asset_code = serializers.CharField(source="asset.code", read_only=True)
    asset_name = serializers.CharField(source="asset.name", read_only=True)
    source_request_id = serializers.UUIDField(source="source_request.id", read_only=True)
    assignees = WorkOrderAssigneeSerializer(many=True, read_only=True)
    labor_entries = WorkOrderLaborEntrySerializer(many=True, read_only=True)
    technical_report = WorkOrderTechnicalReportSerializer(read_only=True)

    class Meta:
        model = WorkOrder
        fields = [
            "id",
            "work_order_number",
            "source",
            "source_request_id",
            "asset_id",
            "asset_code",
            "asset_name",
            "title",
            "description",
            "work_order_type",
            "priority",
            "status",
            "requester_user_id",
            "requester_name",
            "requester_email",
            "created_by_user_id",
            "created_by_name",
            "planned_start_at",
            "planned_end_at",
            "due_at",
            "assigned_at",
            "started_at",
            "on_hold_at",
            "technically_closed_at",
            "closed_at",
            "cancelled_at",
            "status_reason",
            "extra_data",
            "assignees",
            "labor_entries",
            "technical_report",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class WorkOrderCreateManualSerializer(serializers.Serializer):
    asset_id = serializers.PrimaryKeyRelatedField(
        source="asset",
        queryset=Asset.objects.filter(deleted_at__isnull=True),
    )
    title = serializers.CharField(max_length=180)
    description = serializers.CharField()
    work_order_type = serializers.CharField(required=False)
    priority = serializers.CharField(required=False)
    requester_user_id = serializers.IntegerField(required=False, allow_null=True)
    requester_name = serializers.CharField(required=False, allow_blank=True)
    requester_email = serializers.EmailField(required=False, allow_blank=True)
    created_by_user_id = serializers.IntegerField(required=False, allow_null=True)
    created_by_name = serializers.CharField(required=False, allow_blank=True)
    planned_start_at = serializers.DateTimeField(required=False, allow_null=True)
    planned_end_at = serializers.DateTimeField(required=False, allow_null=True)
    due_at = serializers.DateTimeField(required=False, allow_null=True)
    extra_data = serializers.JSONField(required=False)

    def create(self, validated_data):
        return work_order_create_manual(
            asset=validated_data["asset"],
            title=validated_data["title"],
            description=validated_data["description"],
            work_order_type=validated_data.get("work_order_type"),
            priority=validated_data.get("priority"),
            requester_user_id=validated_data.get("requester_user_id"),
            requester_name=validated_data.get("requester_name", ""),
            requester_email=validated_data.get("requester_email", ""),
            created_by_user_id=validated_data.get("created_by_user_id"),
            created_by_name=validated_data.get("created_by_name", ""),
            planned_start_at=validated_data.get("planned_start_at"),
            planned_end_at=validated_data.get("planned_end_at"),
            due_at=validated_data.get("due_at"),
            extra_data=validated_data.get("extra_data") or {},
        )


class WorkOrderFromRequestSerializer(serializers.Serializer):
    maintenance_request_id = serializers.PrimaryKeyRelatedField(
        source="maintenance_request",
        queryset=MaintenanceRequest.objects.filter(deleted_at__isnull=True),
    )
    created_by_user_id = serializers.IntegerField(required=False, allow_null=True)
    created_by_name = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        return work_order_create_from_request(
            maintenance_request=validated_data["maintenance_request"],
            created_by_user_id=validated_data.get("created_by_user_id"),
            created_by_name=validated_data.get("created_by_name", ""),
        )


class WorkOrderAssignTechnicianSerializer(serializers.Serializer):
    technician_user_id = serializers.IntegerField()
    technician_name = serializers.CharField(max_length=150)
    technician_email = serializers.EmailField(required=False, allow_blank=True)
    is_primary = serializers.BooleanField(required=False, default=False)


class WorkOrderLaborCreateSerializer(serializers.Serializer):
    technician_user_id = serializers.IntegerField()
    technician_name = serializers.CharField(max_length=150)
    started_at = serializers.DateTimeField()
    ended_at = serializers.DateTimeField()
    notes = serializers.CharField(required=False, allow_blank=True)


class WorkOrderTechnicalCloseSerializer(serializers.Serializer):
    diagnosis = serializers.CharField()
    work_performed = serializers.CharField()
    probable_cause = serializers.CharField(required=False, allow_blank=True)
    observations = serializers.CharField(required=False, allow_blank=True)
    evidence_uri = serializers.CharField(required=False, allow_blank=True)
    closed_by_user_id = serializers.IntegerField(required=False, allow_null=True)
    closed_by_name = serializers.CharField(required=False, allow_blank=True)


class WorkOrderReasonSerializer(serializers.Serializer):
    reason = serializers.CharField(required=False, allow_blank=True)