import uuid

from django.core.exceptions import ValidationError
from django.db import models

from apps.assets.models import Asset
from apps.maintenance_requests.models import MaintenanceRequest

from .choices import (
    WorkOrderPriority,
    WorkOrderSource,
    WorkOrderStatus,
    WorkOrderType,
)


class WorkOrder(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    work_order_number = models.CharField(
        max_length=40,
        unique=True,
        help_text="Human-readable work order number.",
    )
    source = models.CharField(
        max_length=30,
        choices=WorkOrderSource.choices,
        default=WorkOrderSource.MANUAL,
    )
    source_request = models.OneToOneField(
        MaintenanceRequest,
        on_delete=models.PROTECT,
        related_name="work_order",
        null=True,
        blank=True,
        help_text="Maintenance request that originated this work order, if applicable.",
    )
    asset = models.ForeignKey(
        Asset,
        on_delete=models.PROTECT,
        related_name="work_orders",
    )
    title = models.CharField(
        max_length=180,
    )
    description = models.TextField()
    work_order_type = models.CharField(
        max_length=30,
        choices=WorkOrderType.choices,
        default=WorkOrderType.CORRECTIVE,
    )
    priority = models.CharField(
        max_length=20,
        choices=WorkOrderPriority.choices,
        default=WorkOrderPriority.MEDIUM,
    )
    status = models.CharField(
        max_length=30,
        choices=WorkOrderStatus.choices,
        default=WorkOrderStatus.CREATED,
    )

    requester_user_id = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        help_text="Requester user ID from control database snapshot.",
    )
    requester_name = models.CharField(
        max_length=150,
        blank=True,
    )
    requester_email = models.EmailField(
        blank=True,
    )

    created_by_user_id = models.PositiveBigIntegerField(
        null=True,
        blank=True,
    )
    created_by_name = models.CharField(
        max_length=150,
        blank=True,
    )

    planned_start_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    planned_end_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    due_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    assigned_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    started_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    on_hold_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    technically_closed_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    closed_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    cancelled_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    status_reason = models.TextField(
        blank=True,
    )
    extra_data = models.JSONField(
        default=dict,
        blank=True,
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
            models.Index(fields=["work_order_number"]),
            models.Index(fields=["asset"]),
            models.Index(fields=["source"]),
            models.Index(fields=["status"]),
            models.Index(fields=["priority"]),
            models.Index(fields=["work_order_type"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["deleted_at"]),
        ]

    def __str__(self):
        return f"{self.work_order_number} - {self.title}"

    def clean(self):
        super().clean()

        if self.asset_id and self.asset.deleted_at is not None:
            raise ValidationError(
                {
                    "asset": "Work orders cannot be linked to a deleted asset."
                }
            )

        if self.source_request_id:
            if self.source_request.deleted_at is not None:
                raise ValidationError(
                    {
                        "source_request": (
                            "Work orders cannot be linked to a deleted request."
                        )
                    }
                )

            if self.asset_id and self.source_request.asset_id != self.asset_id:
                raise ValidationError(
                    {
                        "asset": (
                            "The work order asset must match the source request asset."
                        )
                    }
                )

        if self.status == WorkOrderStatus.ASSIGNED and self.assigned_at is None:
            raise ValidationError(
                {
                    "assigned_at": "Assigned work orders must have an assigned date."
                }
            )

        if self.status == WorkOrderStatus.IN_PROGRESS and self.started_at is None:
            raise ValidationError(
                {
                    "started_at": "In-progress work orders must have a start date."
                }
            )

        if (
            self.status == WorkOrderStatus.TECHNICALLY_CLOSED
            and self.technically_closed_at is None
        ):
            raise ValidationError(
                {
                    "technically_closed_at": (
                        "Technically closed work orders must have a technical close date."
                    )
                }
            )

        if self.status == WorkOrderStatus.CLOSED and self.closed_at is None:
            raise ValidationError(
                {
                    "closed_at": "Closed work orders must have a close date."
                }
            )

        if self.status == WorkOrderStatus.CANCELLED and self.cancelled_at is None:
            raise ValidationError(
                {
                    "cancelled_at": "Cancelled work orders must have a cancellation date."
                }
            )


class WorkOrderAssignee(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    work_order = models.ForeignKey(
        WorkOrder,
        on_delete=models.CASCADE,
        related_name="assignees",
    )
    technician_user_id = models.PositiveBigIntegerField(
        help_text="Technician user ID from control database.",
    )
    technician_name = models.CharField(
        max_length=150,
    )
    technician_email = models.EmailField(
        blank=True,
    )
    is_primary = models.BooleanField(
        default=False,
    )
    is_active = models.BooleanField(
        default=True,
    )
    assigned_at = models.DateTimeField()
    unassigned_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-is_primary", "technician_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["work_order", "technician_user_id"],
                condition=models.Q(unassigned_at__isnull=True),
                name="unique_active_work_order_assignee",
            )
        ]
        indexes = [
            models.Index(fields=["work_order"]),
            models.Index(fields=["technician_user_id"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["unassigned_at"]),
        ]

    def __str__(self):
        return f"{self.work_order.work_order_number} -> {self.technician_name}"


class WorkOrderLaborEntry(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    work_order = models.ForeignKey(
        WorkOrder,
        on_delete=models.CASCADE,
        related_name="labor_entries",
    )
    technician_user_id = models.PositiveBigIntegerField()
    technician_name = models.CharField(
        max_length=150,
    )
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    notes = models.TextField(
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["started_at"]
        indexes = [
            models.Index(fields=["work_order"]),
            models.Index(fields=["technician_user_id"]),
            models.Index(fields=["started_at"]),
        ]

    def __str__(self):
        return f"{self.work_order.work_order_number} - {self.technician_name}"

    def clean(self):
        super().clean()

        if self.ended_at <= self.started_at:
            raise ValidationError(
                {
                    "ended_at": "Labor end time must be after start time."
                }
            )


class WorkOrderTechnicalReport(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    work_order = models.OneToOneField(
        WorkOrder,
        on_delete=models.CASCADE,
        related_name="technical_report",
    )
    diagnosis = models.TextField()
    work_performed = models.TextField()
    probable_cause = models.TextField(
        blank=True,
    )
    observations = models.TextField(
        blank=True,
    )
    evidence_uri = models.CharField(
        max_length=500,
        blank=True,
        help_text="File path, URL, or storage reference for evidence.",
    )
    closed_by_user_id = models.PositiveBigIntegerField(
        null=True,
        blank=True,
    )
    closed_by_name = models.CharField(
        max_length=150,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["work_order"]),
            models.Index(fields=["closed_by_user_id"]),
        ]

    def __str__(self):
        return f"Technical report for {self.work_order.work_order_number}"