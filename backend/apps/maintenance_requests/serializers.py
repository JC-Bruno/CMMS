from rest_framework import serializers

from apps.assets.models import Asset

from .models import MaintenanceRequest
from .services import (
    maintenance_request_cancel,
    maintenance_request_create,
    maintenance_request_mark_received,
    maintenance_request_reject,
)


class MaintenanceRequestSerializer(serializers.ModelSerializer):
    asset_id = serializers.PrimaryKeyRelatedField(
        source="asset",
        queryset=Asset.objects.filter(deleted_at__isnull=True),
    )
    asset_code = serializers.CharField(source="asset.code", read_only=True)
    asset_name = serializers.CharField(source="asset.name", read_only=True)

    class Meta:
        model = MaintenanceRequest
        fields = [
            "id",
            "request_number",
            "asset_id",
            "asset_code",
            "asset_name",
            "title",
            "description",
            "perceived_priority",
            "status",
            "source",
            "requester_user_id",
            "requester_name",
            "requester_email",
            "is_confirmed_by_requester",
            "confirmed_at",
            "asset_was_stopped",
            "safety_risk",
            "production_impact",
            "status_reason",
            "extra_data",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = [
            "id",
            "request_number",
            "asset_code",
            "asset_name",
            "status",
            "confirmed_at",
            "status_reason",
            "created_at",
            "updated_at",
            "deleted_at",
        ]

    def create(self, validated_data):
        return maintenance_request_create(
            asset=validated_data["asset"],
            title=validated_data["title"],
            description=validated_data["description"],
            perceived_priority=validated_data.get("perceived_priority"),
            source=validated_data.get("source"),
            requester_user_id=validated_data.get("requester_user_id"),
            requester_name=validated_data.get("requester_name", ""),
            requester_email=validated_data.get("requester_email", ""),
            is_confirmed_by_requester=validated_data.get(
                "is_confirmed_by_requester",
                True,
            ),
            asset_was_stopped=validated_data.get("asset_was_stopped", False),
            safety_risk=validated_data.get("safety_risk", False),
            production_impact=validated_data.get("production_impact", False),
            extra_data=validated_data.get("extra_data") or {},
        )


class MaintenanceRequestReasonSerializer(serializers.Serializer):
    reason = serializers.CharField(required=False, allow_blank=True)