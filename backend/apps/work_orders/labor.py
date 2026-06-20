from django.db import transaction

from .models import WorkOrderLaborEntry


@transaction.atomic(using="client_template")
def work_order_labor_entry_create(
    *,
    work_order,
    technician_user_id,
    technician_name,
    started_at,
    ended_at,
    notes="",
):
    duration_minutes = int((ended_at - started_at).total_seconds() // 60)

    labor_entry = WorkOrderLaborEntry(
        work_order=work_order,
        technician_user_id=technician_user_id,
        technician_name=technician_name,
        started_at=started_at,
        ended_at=ended_at,
        duration_minutes=duration_minutes,
        notes=notes,
    )
    labor_entry.full_clean()
    labor_entry.save()

    return labor_entry