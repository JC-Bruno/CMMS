from django.contrib import admin

from .models import Tenant


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "status",
        "database_name",
        "database_host",
        "database_port",
        "created_at",
    )
    list_filter = (
        "status",
    )
    search_fields = (
        "code",
        "name",
        "legal_name",
        "database_name",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )