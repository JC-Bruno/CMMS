from .choices import WorkOrderStatus
from .models import WorkOrder


def work_order_list(*, include_deleted=False):
    queryset = WorkOrder.objects.select_related(
        "asset",
        "source_request",
    )

    if not include_deleted:
        queryset = queryset.filter(deleted_at__isnull=True)

    return queryset.order_by("-created_at")


def work_order_get_by_number(*, work_order_number):
    return (
        WorkOrder.objects.select_related(
            "asset",
            "source_request",
        )
        .filter(
            work_order_number=work_order_number,
            deleted_at__isnull=True,
        )
        .first()
    )


def work_order_list_by_asset(*, asset, include_deleted=False):
    queryset = WorkOrder.objects.filter(asset=asset)

    if not include_deleted:
        queryset = queryset.filter(deleted_at__isnull=True)

    return queryset.order_by("-created_at")


def work_order_list_open(*, include_deleted=False):
    queryset = WorkOrder.objects.select_related("asset").exclude(
        status__in=[
            WorkOrderStatus.CLOSED,
            WorkOrderStatus.CANCELLED,
        ]
    )

    if not include_deleted:
        queryset = queryset.filter(deleted_at__isnull=True)

    return queryset.order_by("-created_at")