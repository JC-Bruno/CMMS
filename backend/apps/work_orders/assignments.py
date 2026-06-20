from django.db import transaction
from django.utils import timezone

from .choices import WorkOrderStatus
from .models import WorkOrderAssignee


@transaction.atomic(using="client_template")
def work_order_assign_technician(
    *,
    work_order,
    technician_user_id,
    technician_name,
    technician_email="",
    is_primary=False,
):
    now = timezone.now()

    assignee, _created = WorkOrderAssignee.objects.get_or_create(
        work_order=work_order,
        technician_user_id=technician_user_id,
        unassigned_at=None,
        defaults={
            "technician_name": technician_name,
            "technician_email": technician_email,
            "is_primary": is_primary,
            "assigned_at": now,
        },
    )

    if work_order.status == WorkOrderStatus.CREATED:
        work_order.status = WorkOrderStatus.ASSIGNED
        work_order.assigned_at = now
        work_order.full_clean()
        work_order.save(update_fields=["status", "assigned_at", "updated_at"])

    return assignee