from django.db import models


class WorkOrderStatus(models.TextChoices):
    CREATED = "created", "Created"
    ASSIGNED = "assigned", "Assigned"
    IN_PROGRESS = "in_progress", "In progress"
    ON_HOLD = "on_hold", "On hold"
    TECHNICALLY_CLOSED = "technically_closed", "Technically closed"
    CLOSED = "closed", "Closed"
    CANCELLED = "cancelled", "Cancelled"


class WorkOrderType(models.TextChoices):
    CORRECTIVE = "corrective", "Corrective"
    PREVENTIVE = "preventive", "Preventive"
    INSPECTION = "inspection", "Inspection"
    IMPROVEMENT = "improvement", "Improvement"
    OTHER = "other", "Other"


class WorkOrderPriority(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"
    URGENT = "urgent", "Urgent"
    SAFETY = "safety", "Safety"


class WorkOrderSource(models.TextChoices):
    MANUAL = "manual", "Manual"
    MAINTENANCE_REQUEST = "maintenance_request", "Maintenance request"
    PREVENTIVE_PLAN = "preventive_plan", "Preventive plan"
    OTHER = "other", "Other"