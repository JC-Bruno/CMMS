from django.db import transaction
from django.utils import timezone

from .models import (
    MaintenanceRequest,
    MaintenanceRequestPriority,
    MaintenanceRequestSource,
    MaintenanceRequestStatus,
)
from ..work_orders.numbering import generate_request_number


@transaction.atomic
def maintenance_request_create(
    *,
    asset,
    title,
    description,
    requester_name,
    requester_user_id=None,
    requester_email="",
    perceived_priority=MaintenanceRequestPriority.MEDIUM,
    source=MaintenanceRequestSource.WEB,
    asset_was_stopped=False,
    safety_risk=False,
    production_impact=False,
    extra_data=None,
):
    now = timezone.now()

    request = MaintenanceRequest(
        request_number=generate_request_number(),
        asset=asset,
        title=title,
        description=description,
        requester_user_id=requester_user_id,
        requester_name=requester_name,
        requester_email=requester_email,
        perceived_priority=perceived_priority,
        source=source,
        is_confirmed_by_requester=True,
        confirmed_at=now,
        asset_was_stopped=asset_was_stopped,
        safety_risk=safety_risk,
        production_impact=production_impact,
        extra_data=extra_data or {},
    )
    request.full_clean()
    request.save()

    return request


@transaction.atomic
def maintenance_request_mark_received(*, request):
    request.status = MaintenanceRequestStatus.RECEIVED
    request.received_at = timezone.now()
    request.full_clean()
    request.save(update_fields=["status", "received_at", "updated_at"])

    return request


@transaction.atomic
def maintenance_request_reject(*, request, reason):
    request.status = MaintenanceRequestStatus.REJECTED
    request.rejected_at = timezone.now()
    request.status_reason = reason
    request.full_clean()
    request.save(
        update_fields=[
            "status",
            "rejected_at",
            "status_reason",
            "updated_at",
        ]
    )

    return request


@transaction.atomic
def maintenance_request_cancel(*, request, reason):
    request.status = MaintenanceRequestStatus.CANCELLED
    request.cancelled_at = timezone.now()
    request.status_reason = reason
    request.full_clean()
    request.save(
        update_fields=[
            "status",
            "cancelled_at",
            "status_reason",
            "updated_at",
        ]
    )

    return request


@transaction.atomic
def maintenance_request_mark_converted(*, request):
    request.status = MaintenanceRequestStatus.CONVERTED_TO_WORK_ORDER
    request.converted_at = timezone.now()
    request.full_clean()
    request.save(update_fields=["status", "converted_at", "updated_at"])

    return request