from django.contrib import admin

from .models import (
    WorkOrder,
    WorkOrderAssignee,
    WorkOrderLaborEntry,
    WorkOrderTechnicalReport,
)


class WorkOrderAssigneeInline(admin.TabularInline):
    model = WorkOrderAssignee
    extra = 0


class WorkOrderLaborEntryInline(admin.TabularInline):
    model = WorkOrderLaborEntry
    extra = 0


class WorkOrderTechnicalReportInline(admin.StackedInline):
    model = WorkOrderTechnicalReport
    extra = 0
    max_num = 1


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = (
        "work_order_number",
        "asset",
        "title",
        "work_order_type",
        "priority",
        "status",
        "source",
        "created_at",
    )
    list_filter = (
        "status",
        "priority",
        "work_order_type",
        "source",
    )
    search_fields = (
        "work_order_number",
        "asset__code",
        "asset__name",
        "title",
        "description",
        "requester_name",
    )
    readonly_fields = (
        "id",
        "work_order_number",
        "created_at",
        "updated_at",
    )
    inlines = [
        WorkOrderAssigneeInline,
        WorkOrderLaborEntryInline,
        WorkOrderTechnicalReportInline,
    ]


@admin.register(WorkOrderAssignee)
class WorkOrderAssigneeAdmin(admin.ModelAdmin):
    list_display = (
        "work_order",
        "technician_user_id",
        "technician_name",
        "is_primary",
        "is_active",
        "assigned_at",
    )
    list_filter = (
        "is_primary",
        "is_active",
    )
    search_fields = (
        "work_order__work_order_number",
        "technician_name",
        "technician_email",
    )


@admin.register(WorkOrderLaborEntry)
class WorkOrderLaborEntryAdmin(admin.ModelAdmin):
    list_display = (
        "work_order",
        "technician_name",
        "started_at",
        "ended_at",
        "duration_minutes",
    )
    search_fields = (
        "work_order__work_order_number",
        "technician_name",
    )


@admin.register(WorkOrderTechnicalReport)
class WorkOrderTechnicalReportAdmin(admin.ModelAdmin):
    list_display = (
        "work_order",
        "closed_by_name",
        "created_at",
    )
    search_fields = (
        "work_order__work_order_number",
        "diagnosis",
        "work_performed",
        "probable_cause",
        "closed_by_name",
    )