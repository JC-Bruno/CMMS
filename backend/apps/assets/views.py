from rest_framework import mixins, viewsets

from .models import Asset, AssetDocument, AssetLocationNode
from .serializers import (
    AssetDocumentSerializer,
    AssetLocationNodeSerializer,
    AssetSerializer,
)


class AssetLocationNodeViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = AssetLocationNodeSerializer

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

    def get_queryset(self):
        return (
            AssetDocument.objects.select_related("asset")
            .filter(deleted_at__isnull=True)
            .order_by("-created_at")
        )