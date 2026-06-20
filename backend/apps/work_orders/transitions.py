from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from .choices import WorkOrderStatus
from .models import WorkOrderTechnicalReport


def _ensure_has_active_assignee(*, work_order):
    has_assignee = work_order.assignees.filter(
        is_active=True,
        unassigned_at__isnull=True,
    ).exists()

    if not has_assignee:
        raise ValidationError(
            "A work order must have at least one active assignee before starting."
        )


@transaction.atomic
def work_order_start(*, work_order):
    _ensure_has_active_assignee(work_order=work_order)

    if work_order.status not in [
        WorkOrderStatus.ASSIGNED,
        WorkOrderStatus.ON_HOLD,
    ]:
        raise ValidationError(
            "Only assigned or on-hold work orders can be started."
        )

    work_order.status = WorkOrderStatus.IN_PROGRESS

    if work_order.started_at is None:
        work_order.started_at = timezone.now()

    work_order.full_clean()
    work_order.save(update_fields=["status", "started_at", "updated_at"])

    return work_order


@transaction.atomic
def work_order_put_on_hold(*, work_order, reason):
    if work_order.status != WorkOrderStatus.IN_PROGRESS:
        raise ValidationError(
            "Only in-progress work orders can be put on hold."
        )

    work_order.status = WorkOrderStatus.ON_HOLD
    work_order.on_hold_at = timezone.now()
    work_order.status_reason = reason
    work_order.save(update_fields=["status", "on_hold_at", "status_reason", "updated_at"])

    return work_order


@transaction.atomic
def work_order_technical_close(
    *,
    work_order,
    diagnosis,
    work_performed,
    probable_cause="",
    observations="",
    evidence_uri="",
    closed_by_user_id=None,
    closed_by_name="",
):
    if work_order.status != WorkOrderStatus.IN_PROGRESS:
        raise ValidationError(
            "Only in-progress work orders can be technically closed."
        )

    if not diagnosis.strip():
        raise ValidationError("Diagnosis is required for technical close.")

    if not work_performed.strip():
        raise ValidationError("Work performed is required for technical close.")

    report = WorkOrderTechnicalReport(
        work_order=work_order,
        diagnosis=diagnosis,
        work_performed=work_performed,
        probable_cause=probable_cause,
        observations=observations,
        evidence_uri=evidence_uri,
        closed_by_user_id=closed_by_user_id,
        closed_by_name=closed_by_name,
    )
    report.full_clean()
    report.save()

    work_order.status = WorkOrderStatus.TECHNICALLY_CLOSED
    work_order.technically_closed_at = timezone.now()
    work_order.full_clean()
    work_order.save(update_fields=["status", "technically_closed_at", "updated_at"])

    return work_order


@transaction.atomic
def work_order_close_final(*, work_order):
    if work_order.status != WorkOrderStatus.TECHNICALLY_CLOSED:
        raise ValidationError(
            "Only technically closed work orders can be finally closed."
        )

    work_order.status = WorkOrderStatus.CLOSED
    work_order.closed_at = timezone.now()
    work_order.full_clean()
    work_order.save(update_fields=["status", "closed_at", "updated_at"])

    return work_order


@transaction.atomic
def work_order_cancel(*, work_order, reason):
    if work_order.status in [
        WorkOrderStatus.CLOSED,
        WorkOrderStatus.CANCELLED,
    ]:
        raise ValidationError(
            "Closed or cancelled work orders cannot be cancelled again."
        )

    work_order.status = WorkOrderStatus.CANCELLED
    work_order.cancelled_at = timezone.now()
    work_order.status_reason = reason
    work_order.full_clean()
    work_order.save(
        update_fields=[
            "status",
            "cancelled_at",
            "status_reason",
            "updated_at",
        ]
    )

    return work_order