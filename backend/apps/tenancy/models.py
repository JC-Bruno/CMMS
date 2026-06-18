import uuid

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


class TenantStatus(models.TextChoices):
    PROVISIONING = "provisioning", "Provisioning"
    ACTIVE = "active", "Active"
    SUSPENDED = "suspended", "Suspended"
    INACTIVE = "inactive", "Inactive"


class Tenant(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    code = models.SlugField(
        max_length=60,
        unique=True,
        help_text="Short unique code used internally to identify the tenant.",
    )
    name = models.CharField(
        max_length=150,
        help_text="Commercial name of the tenant.",
    )
    legal_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Legal name or registered company name.",
    )
    tax_id = models.CharField(
        max_length=50,
        blank=True,
        help_text="Optional tax identification number.",
    )
    status = models.CharField(
        max_length=20,
        choices=TenantStatus.choices,
        default=TenantStatus.PROVISIONING,
    )
    database_name = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[a-z][a-z0-9_]*$",
                message=(
                    "Database name must start with a lowercase letter and "
                    "contain only lowercase letters, numbers, and underscores."
                ),
            )
        ],
        help_text="Dedicated operational database assigned to this tenant.",
    )
    database_host = models.CharField(
        max_length=255,
        default="localhost",
    )
    database_port = models.PositiveIntegerField(
        default=5433,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(65535),
        ],
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
        ordering = ["name"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["status"]),
            models.Index(fields=["database_name"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"

    @property
    def is_active(self):
        return self.status == TenantStatus.ACTIVE and self.deleted_at is None