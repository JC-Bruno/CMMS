from rest_framework import serializers

from .models import Asset, AssetDocument, AssetLocationNode
from .services import asset_create, asset_document_create, location_node_create

from apps.assets.models import Asset, AssetStructureNode
from apps.assets.services import (
    asset_structure_node_create,
    asset_structure_node_update,
)

class AssetLocationNodeSerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(
        source="parent",
        queryset=AssetLocationNode.objects.filter(deleted_at__isnull=True),
        allow_null=True,
        required=False,
    )
    parent_code = serializers.CharField(source="parent.code", read_only=True)

    class Meta:
        model = AssetLocationNode
        fields = [
            "id",
            "code",
            "name",
            "node_type",
            "parent_id",
            "parent_code",
            "description",
            "is_active",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = [
            "id",
            "parent_code",
            "is_active",
            "created_at",
            "updated_at",
            "deleted_at",
        ]

    def create(self, validated_data):
        return location_node_create(
            code=validated_data["code"],
            name=validated_data["name"],
            node_type=validated_data["node_type"],
            parent=validated_data.get("parent"),
            description=validated_data.get("description", ""),
        )


class AssetSerializer(serializers.ModelSerializer):
    location_id = serializers.PrimaryKeyRelatedField(
        source="location",
        queryset=AssetLocationNode.objects.filter(deleted_at__isnull=True),
    )
    location_code = serializers.CharField(source="location.code", read_only=True)
    parent_asset_id = serializers.PrimaryKeyRelatedField(
        source="parent_asset",
        queryset=Asset.objects.filter(deleted_at__isnull=True),
        allow_null=True,
        required=False,
    )
    parent_asset_code = serializers.CharField(source="parent_asset.code", read_only=True)

    class Meta:
        model = Asset
        fields = [
            "id",
            "code",
            "name",
            "asset_type",
            "status",
            "criticality",
            "location_id",
            "location_code",
            "parent_asset_id",
            "parent_asset_code",
            "manufacturer",
            "model",
            "serial_number",
            "technical_specs",
            "acquisition_date",
            "installation_date",
            "notes",
            "is_maintainable",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = [
            "id",
            "location_code",
            "parent_asset_code",
            "created_at",
            "updated_at",
            "deleted_at",
        ]

    def create(self, validated_data):
        return asset_create(
            code=validated_data["code"],
            name=validated_data["name"],
            location=validated_data["location"],
            asset_type=validated_data.get("asset_type"),
            status=validated_data.get("status"),
            criticality=validated_data.get("criticality"),
            parent_asset=validated_data.get("parent_asset"),
            manufacturer=validated_data.get("manufacturer", ""),
            model=validated_data.get("model", ""),
            serial_number=validated_data.get("serial_number", ""),
            technical_specs=validated_data.get("technical_specs") or {},
            acquisition_date=validated_data.get("acquisition_date"),
            installation_date=validated_data.get("installation_date"),
            notes=validated_data.get("notes", ""),
            is_maintainable=validated_data.get("is_maintainable", True),
        )


class AssetDocumentSerializer(serializers.ModelSerializer):
    asset_id = serializers.PrimaryKeyRelatedField(
        source="asset",
        queryset=Asset.objects.filter(deleted_at__isnull=True),
    )
    asset_code = serializers.CharField(source="asset.code", read_only=True)

    class Meta:
        model = AssetDocument
        fields = [
            "id",
            "asset_id",
            "asset_code",
            "document_type",
            "title",
            "document_uri",
            "description",
            "issued_at",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = [
            "id",
            "asset_code",
            "created_at",
            "updated_at",
            "deleted_at",
        ]

    def create(self, validated_data):
        return asset_document_create(
            asset=validated_data["asset"],
            document_type=validated_data["document_type"],
            title=validated_data["title"],
            document_uri=validated_data["document_uri"],
            description=validated_data.get("description", ""),
            issued_at=validated_data.get("issued_at"),
        )
    
class AssetStructureNodeSerializer(serializers.ModelSerializer):
    asset_code = serializers.CharField(source="asset.code", read_only=True)
    asset_name = serializers.CharField(source="asset.name", read_only=True)
    parent_code = serializers.CharField(source="parent.code", read_only=True)
    parent_name = serializers.CharField(source="parent.name", read_only=True)

    class Meta:
        model = AssetStructureNode
        fields = (
            "id",
            "asset",
            "asset_code",
            "asset_name",
            "parent",
            "parent_code",
            "parent_name",
            "node_type",
            "code",
            "name",
            "description",
            "is_maintainable",
            "sort_order",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "asset_code",
            "asset_name",
            "parent_code",
            "parent_name",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        return asset_structure_node_create(**validated_data)

    def update(self, instance, validated_data):
        return asset_structure_node_update(
            node=instance,
            parent=validated_data.get("parent"),
            node_type=validated_data["node_type"],
            code=validated_data["code"],
            name=validated_data["name"],
            description=validated_data.get("description", ""),
            is_maintainable=validated_data.get("is_maintainable", False),
            sort_order=validated_data.get("sort_order", 0),
        )