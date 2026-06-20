from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

from apps.tenancy.models import Tenant


permission_code_validator = RegexValidator(
    regex=r"^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+$",
    message=(
        "Permission code must use lowercase segments separated by dots, "
        "for example: work_orders.create."
    ),
)


class OperationalPermissionModule(models.TextChoices):
    CORE = "core", "Core"
    TENANCY = "tenancy", "Tenancy"
    ACCOUNTS = "accounts", "Accounts"
    ASSETS = "assets", "Assets"
    MAINTENANCE_REQUESTS = "maintenance_requests", "Maintenance requests"
    WORK_ORDERS = "work_orders", "Work orders"
    INVENTORY = "inventory", "Inventory"
    REPORTING = "reporting", "Reporting"
    ADMINISTRATION = "administration", "Administration"


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cmms_profile",
    )
    job_title = models.CharField(
        max_length=120,
        blank=True,
    )
    phone = models.CharField(
        max_length=40,
        blank=True,
    )
    is_global_support = models.BooleanField(
        default=False,
        help_text="Allows the user to be marked as internal platform support.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["user__username"]

    def __str__(self):
        return f"Profile for {self.user}"


class OperationalPermission(models.Model):
    code = models.CharField(
        max_length=120,
        unique=True,
        validators=[permission_code_validator],
        help_text="Internal permission code, for example: work_orders.create.",
    )
    name = models.CharField(
        max_length=150,
    )
    module = models.CharField(
        max_length=40,
        choices=OperationalPermissionModule.choices,
    )
    description = models.TextField(
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["module", "code"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["module"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.code


class Role(models.Model):
    code = models.SlugField(
        max_length=80,
        unique=True,
        help_text="Short unique role code, for example: maintenance_supervisor.",
    )
    name = models.CharField(
        max_length=150,
    )
    description = models.TextField(
        blank=True,
    )
    is_system = models.BooleanField(
        default=False,
        help_text="Marks roles created by the platform and not by a tenant admin.",
    )
    is_active = models.BooleanField(
        default=True,
    )
    permissions = models.ManyToManyField(
        OperationalPermission,
        through="RolePermission",
        related_name="roles",
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name


class RolePermission(models.Model):
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="role_permissions",
    )
    permission = models.ForeignKey(
        OperationalPermission,
        on_delete=models.CASCADE,
        related_name="permission_roles",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = ("role", "permission")
        ordering = ["role__name", "permission__code"]

    def __str__(self):
        return f"{self.role} -> {self.permission}"


class TenantUser(models.Model):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="tenant_users",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tenant_memberships",
    )
    display_name = models.CharField(
        max_length=150,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
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
        ordering = ["tenant__name", "user__username"]
        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "user"],
                condition=models.Q(deleted_at__isnull=True),
                name="unique_active_tenant_user",
            )
        ]
        indexes = [
            models.Index(fields=["tenant", "user"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["deleted_at"]),
        ]

    def __str__(self):
        return f"{self.user} @ {self.tenant}"


class TenantUserRole(models.Model):
    tenant_user = models.ForeignKey(
        TenantUser,
        on_delete=models.CASCADE,
        related_name="tenant_user_roles",
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="tenant_user_roles",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = ("tenant_user", "role")
        ordering = ["tenant_user__tenant__name", "role__name"]

    def __str__(self):
        return f"{self.tenant_user} -> {self.role}"