from django.contrib import admin

from .models import MaintenanceRequest


@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = (
        "request_number",
        "asset",
        "title",
        "perceived_priority",
        "status",
        "requester_name",
        "asset_was_stopped",
        "safety_risk",
        "production_impact",
        "created_at",
    )
    list_filter = (
        "status",
        "perceived_priority",
        "asset_was_stopped",
        "safety_risk",
        "production_impact",
        "source",
    )
    search_fields = (
        "request_number",
        "asset__code",
        "asset__name",
        "title",
        "description",
        "requester_name",
        "requester_email",
    )
    readonly_fields = (
        "id",
        "request_number",
        "created_at",
        "updated_at",
    )