from rest_framework import mixins, viewsets

from apps.accounts.permissions import HasOperationalPermission

from .models import Asset, AssetDocument, AssetLocationNode
from .serializers import (
    AssetDocumentSerializer,
    AssetLocationNodeSerializer,
    AssetSerializer,
)

from apps.assets.models import AssetStructureNode
from apps.assets.selectors import asset_structure_node_list
from apps.assets.serializers import AssetStructureNodeSerializer
from apps.assets.services import asset_structure_node_soft_delete


class AssetLocationNodeViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = AssetLocationNodeSerializer
    permission_classes = [HasOperationalPermission]
    permission_required_by_action = {
        "list": "assets.view_asset_location",
        "retrieve": "assets.view_asset_location",
        "create": "assets.create_asset_location",
    }

    def get_queryset(self):
        return (
            AssetLocationNode.objects.select_related("parent")
            .filter(deleted_at__isnull=True)
            .order_by("code")
        )


class AssetViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = AssetSerializer
    permission_classes = [HasOperationalPermission]
    permission_required_by_action = {
        "list": "assets.view_asset",
        "retrieve": "assets.view_asset",
        "create": "assets.create_asset",
    }

    def get_queryset(self):
        return (
            Asset.objects.select_related("location", "parent_asset")
            .filter(deleted_at__isnull=True)
            .order_by("code")
        )


class AssetDocumentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = AssetDocumentSerializer
    permission_classes = [HasOperationalPermission]
    permission_required_by_action = {
        "list": "assets.view_asset_document",
        "retrieve": "assets.view_asset_document",
        "create": "assets.create_asset_document",
    }

    def get_queryset(self):
        return (
            AssetDocument.objects.select_related("asset")
            .filter(deleted_at__isnull=True)
            .order_by("-created_at")
        )
    
class AssetStructureNodeViewSet(viewsets.ModelViewSet):
    serializer_class = AssetStructureNodeSerializer
    permission_classes = [HasOperationalPermission]

    permission_required_by_action = {
        "list": "assets.view_asset",
        "retrieve": "assets.view_asset",
        "create": "assets.create_asset",
        "update": "assets.change_asset",
        "partial_update": "assets.change_asset",
        "destroy": "assets.delete_asset",
    }

    def get_queryset(self):
        return asset_structure_node_list()

    def perform_destroy(self, instance: AssetStructureNode):
        asset_structure_node_soft_delete(node=instance)