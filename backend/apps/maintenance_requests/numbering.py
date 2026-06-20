from django.utils import timezone

from .models import MaintenanceRequest


def generate_request_number():
    today = timezone.localdate()
    prefix = f"MR-{today:%Y%m%d}"

    today_count = MaintenanceRequest.objects.filter(
        created_at__date=today,
    ).count()

    sequence = today_count + 1

    return f"{prefix}-{sequence:04d}"