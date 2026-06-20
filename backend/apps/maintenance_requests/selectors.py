from .models import MaintenanceRequest, MaintenanceRequestStatus


def maintenance_request_list(*, include_deleted=False):
    queryset = MaintenanceRequest.objects.select_related("asset")

    if not include_deleted:
        queryset = queryset.filter(deleted_at__isnull=True)

    return queryset.order_by("-created_at")


def maintenance_request_get_by_number(*, request_number):
    return (
        MaintenanceRequest.objects.select_related("asset")
        .filter(
            request_number=request_number,
            deleted_at__isnull=True,
        )
        .first()
    )


def maintenance_request_list_by_asset(*, asset, include_deleted=False):
    queryset = MaintenanceRequest.objects.filter(asset=asset)

    if not include_deleted:
        queryset = queryset.filter(deleted_at__isnull=True)

    return queryset.order_by("-created_at")


def maintenance_request_list_open(*, include_deleted=False):
    queryset = MaintenanceRequest.objects.select_related("asset").exclude(
        status__in=[
            MaintenanceRequestStatus.REJECTED,
            MaintenanceRequestStatus.CANCELLED,
            MaintenanceRequestStatus.CONVERTED_TO_WORK_ORDER,
        ]
    )

    if not include_deleted:
        queryset = queryset.filter(deleted_at__isnull=True)

    return queryset.order_by("-created_at")