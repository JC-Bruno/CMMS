from django.db import transaction

from apps.maintenance_requests.models import MaintenanceRequestPriority

from .choices import (
    WorkOrderPriority,
    WorkOrderSource,
    WorkOrderStatus,
    WorkOrderType,
)
from .models import WorkOrder
from .numbering import generate_work_order_number


PRIORITY_MAP_FROM_REQUEST = {
    MaintenanceRequestPriority.LOW: WorkOrderPriority.LOW,
    MaintenanceRequestPriority.MEDIUM: WorkOrderPriority.MEDIUM,
    MaintenanceRequestPriority.HIGH: WorkOrderPriority.HIGH,
    MaintenanceRequestPriority.URGENT: WorkOrderPriority.URGENT,
    MaintenanceRequestPriority.SAFETY: WorkOrderPriority.SAFETY,
}


@transaction.atomic
def work_order_create_manual(
    *,
    asset,
    title,
    description,
    work_order_type=WorkOrderType.CORRECTIVE,
    priority=WorkOrderPriority.MEDIUM,
    requester_user_id=None,
    requester_name="",
    requester_email="",
    created_by_user_id=None,
    created_by_name="",
    planned_start_at=None,
    planned_end_at=None,
    due_at=None,
    extra_data=None,
):
    work_order = WorkOrder(
        work_order_number=generate_work_order_number(),
        source=WorkOrderSource.MANUAL,
        asset=asset,
        title=title,
        description=description,
        work_order_type=work_order_type,
        priority=priority,
        status=WorkOrderStatus.CREATED,
        requester_user_id=requester_user_id,
        requester_name=requester_name,
        requester_email=requester_email,
        created_by_user_id=created_by_user_id,
        created_by_name=created_by_name,
        planned_start_at=planned_start_at,
        planned_end_at=planned_end_at,
        due_at=due_at,
        extra_data=extra_data or {},
    )
    work_order.full_clean()
    work_order.save()

    return work_order


@transaction.atomic
def work_order_create_from_request(
    *,
    maintenance_request,
    created_by_user_id=None,
    created_by_name="",
):
    priority = PRIORITY_MAP_FROM_REQUEST[maintenance_request.perceived_priority]

    work_order = WorkOrder(
        work_order_number=generate_work_order_number(),
        source=WorkOrderSource.MAINTENANCE_REQUEST,
        source_request=maintenance_request,
        asset=maintenance_request.asset,
        title=maintenance_request.title,
        description=maintenance_request.description,
        work_order_type=WorkOrderType.CORRECTIVE,
        priority=priority,
        status=WorkOrderStatus.CREATED,
        requester_user_id=maintenance_request.requester_user_id,
        requester_name=maintenance_request.requester_name,
        requester_email=maintenance_request.requester_email,
        created_by_user_id=created_by_user_id,
        created_by_name=created_by_name,
        extra_data={
            "source_request_number": maintenance_request.request_number,
        },
    )
    work_order.full_clean()
    work_order.save()

    from apps.maintenance_requests.services import maintenance_request_mark_converted

    maintenance_request_mark_converted(request=maintenance_request)

    return work_order