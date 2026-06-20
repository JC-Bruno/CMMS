from django.contrib import admin

from .models import (
    OperationalPermission,
    Role,
    RolePermission,
    TenantUser,
    TenantUserRole,
    UserProfile,
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "job_title",
        "phone",
        "is_global_support",
        "created_at",
    )
    search_fields = (
        "user__username",
        "user__email",
        "job_title",
        "phone",
    )
    list_filter = (
        "is_global_support",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )


class RolePermissionInline(admin.TabularInline):
    model = RolePermission
    extra = 0


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "is_system",
        "is_active",
        "created_at",
    )
    list_filter = (
        "is_system",
        "is_active",
    )
    search_fields = (
        "code",
        "name",
        "description",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    inlines = [
        RolePermissionInline,
    ]


@admin.register(OperationalPermission)
class OperationalPermissionAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "module",
        "is_active",
    )
    list_filter = (
        "module",
        "is_active",
    )
    search_fields = (
        "code",
        "name",
        "description",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )


class TenantUserRoleInline(admin.TabularInline):
    model = TenantUserRole
    extra = 0


@admin.register(TenantUser)
class TenantUserAdmin(admin.ModelAdmin):
    list_display = (
        "tenant",
        "user",
        "display_name",
        "is_active",
        "created_at",
    )
    list_filter = (
        "tenant",
        "is_active",
    )
    search_fields = (
        "tenant__code",
        "tenant__name",
        "user__username",
        "user__email",
        "display_name",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    inlines = [
        TenantUserRoleInline,
    ]