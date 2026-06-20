import uuid

from django.core.exceptions import ValidationError
from django.db import models

from apps.assets.models import Asset


class MaintenanceRequestStatus(models.TextChoices):
    CREATED = "created", "Created"
    RECEIVED = "received", "Received"
    REJECTED = "rejected", "Rejected"
    CANCELLED = "cancelled", "Cancelled"
    CONVERTED_TO_WORK_ORDER = "converted_to_work_order", "Converted to work order"


class MaintenanceRequestPriority(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"
    URGENT = "urgent", "Urgent"
    SAFETY = "safety", "Safety"


class MaintenanceRequestSource(models.TextChoices):
    WEB = "web", "Web"
    MOBILE = "mobile", "Mobile"
    ADMIN = "admin", "Admin"
    IMPORT = "import", "Import"
    OTHER = "other", "Other"


class MaintenanceRequest(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    request_number = models.CharField(
        max_length=40,
        unique=True,
        help_text="Human-readable request number.",
    )
    asset = models.ForeignKey(
        Asset,
        on_delete=models.PROTECT,
        related_name="maintenance_requests",
    )
    title = models.CharField(
        max_length=180,
        help_text="Short description of the reported issue.",
    )
    description = models.TextField(
        help_text="Detailed failure description provided by the requester.",
    )
    perceived_priority = models.CharField(
        max_length=20,
        choices=MaintenanceRequestPriority.choices,
        default=MaintenanceRequestPriority.MEDIUM,
    )
    status = models.CharField(
        max_length=40,
        choices=MaintenanceRequestStatus.choices,
        default=MaintenanceRequestStatus.CREATED,
    )
    source = models.CharField(
        max_length=20,
        choices=MaintenanceRequestSource.choices,
        default=MaintenanceRequestSource.WEB,
    )

    requester_user_id = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        help_text=(
            "ID of the user in the control database. Not a FK because "
            "operational data lives in the client database."
        ),
    )
    requester_name = models.CharField(
        max_length=150,
        help_text="Requester name snapshot at creation time.",
    )
    requester_email = models.EmailField(
        blank=True,
    )

    is_confirmed_by_requester = models.BooleanField(
        default=False,
    )
    confirmed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    asset_was_stopped = models.BooleanField(
        default=False,
        help_text="Indicates whether the asset was stopped when the request was created.",
    )
    safety_risk = models.BooleanField(
        default=False,
    )
    production_impact = models.BooleanField(
        default=False,
    )

    received_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    rejected_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    cancelled_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    converted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    status_reason = models.TextField(
        blank=True,
        help_text="Optional reason for rejection, cancellation, or status change.",
    )
    extra_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="Flexible data captured from form, voice transcription, or import.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["request_number"]),
            models.Index(fields=["asset"]),
            models.Index(fields=["status"]),
            models.Index(fields=["perceived_priority"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["deleted_at"]),
        ]

    def __str__(self):
        return f"{self.request_number} - {self.title}"

    def clean(self):
        super().clean()

        if self.asset_id and self.asset.deleted_at is not None:
            raise ValidationError(
                {
                    "asset": "Maintenance requests cannot be linked to a deleted asset."
                }
            )

        if self.is_confirmed_by_requester and self.confirmed_at is None:
            raise ValidationError(
                {
                    "confirmed_at": (
                        "Confirmed maintenance requests must have a confirmation date."
                    )
                }
            )

        if self.status == MaintenanceRequestStatus.RECEIVED and self.received_at is None:
            raise ValidationError(
                {
                    "received_at": "Received maintenance requests must have a received date."
                }
            )

        if self.status == MaintenanceRequestStatus.REJECTED and self.rejected_at is None:
            raise ValidationError(
                {
                    "rejected_at": "Rejected maintenance requests must have a rejected date."
                }
            )

        if self.status == MaintenanceRequestStatus.CANCELLED and self.cancelled_at is None:
            raise ValidationError(
                {
                    "cancelled_at": "Cancelled maintenance requests must have a cancelled date."
                }
            )

        if (
            self.status == MaintenanceRequestStatus.CONVERTED_TO_WORK_ORDER
            and self.converted_at is None
        ):
            raise ValidationError(
                {
                    "converted_at": (
                        "Converted maintenance requests must have a conversion date."
                    )
                }
            )