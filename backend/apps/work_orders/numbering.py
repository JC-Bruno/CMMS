from django.utils import timezone

from .models import WorkOrder


def generate_work_order_number():
    today = timezone.localdate()
    prefix = f"WO-{today:%Y%m%d}"

    today_count = WorkOrder.objects.filter(
        created_at__date=today,
    ).count()

    sequence = today_count + 1

    return f"{prefix}-{sequence:04d}"