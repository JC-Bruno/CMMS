import pytest
from uuid import uuid4
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.assets.models import (
    AssetCriticality,
    AssetStatus,
    AssetType,
    LocationNodeType,
)
from apps.assets.services import asset_create, location_node_create
from apps.maintenance_requests.models import (
    MaintenanceRequestPriority,
    MaintenanceRequestStatus,
)
from apps.maintenance_requests.services import maintenance_request_create

from .assignments import work_order_assign_technician
from .choices import WorkOrderPriority, WorkOrderStatus
from .labor import work_order_labor_entry_create
from .selectors import work_order_get_by_number, work_order_list_open
from .services import work_order_create_from_request, work_order_create_manual
from .transitions import (
    work_order_cancel,
    work_order_close_final,
    work_order_start,
    work_order_technical_close,
)


def _create_asset():
    suffix = uuid4().hex[:8]

    company = location_node_create(
        code=f"company_{suffix}",
        name="Grupo Monelca",
        node_type=LocationNodeType.COMPANY,
    )
    site = location_node_create(
        code=f"site_sv_{suffix}",
        name="El Salvador",
        node_type=LocationNodeType.SITE,
        parent=company,
    )
    facility = location_node_create(
        code=f"plant_opico_{suffix}",
        name="Planta Opico",
        node_type=LocationNodeType.FACILITY,
        parent=site,
    )
    area = location_node_create(
        code=f"area_cutting_{suffix}",
        name="Área de corte",
        node_type=LocationNodeType.AREA,
        parent=facility,
    )
    location = location_node_create(
        code=f"loc_plasma_01_{suffix}",
        name="Ubicación plasma CNC 01",
        node_type=LocationNodeType.LOCATION,
        parent=area,
    )

    return asset_create(
        code=f"PLASMA-{suffix}",
        name="CNC Plasma 01",
        location=location,
        asset_type=AssetType.EQUIPMENT,
        status=AssetStatus.ACTIVE,
        criticality=AssetCriticality.HIGH,
    )

def _create_work_order_with_assignee():
    asset = _create_asset()
    work_order = work_order_create_manual(
        asset=asset,
        title="No enciende fuente plasma",
        description="Fuente no enciende al iniciar turno.",
        priority=WorkOrderPriority.HIGH,
        requester_name="Supervisor Producción",
    )
    work_order_assign_technician(
        work_order=work_order,
        technician_user_id=10,
        technician_name="Técnico Mecatrónico",
        is_primary=True,
    )
    work_order.refresh_from_db()

    return work_order


@pytest.mark.django_db(databases=["client_template"])
def test_manual_work_order_can_be_created():
    asset = _create_asset()

    work_order = work_order_create_manual(
        asset=asset,
        title="Falla en compresor",
        description="Compresor presenta alarma.",
        priority=WorkOrderPriority.HIGH,
        requester_name="Supervisor Producción",
    )

    assert work_order.asset == asset
    assert work_order.status == WorkOrderStatus.CREATED
    assert work_order.work_order_number.startswith("WO-")
    assert work_order_get_by_number(
        work_order_number=work_order.work_order_number
    ) == work_order


@pytest.mark.django_db(databases=["client_template"])
def test_request_can_be_converted_to_work_order():
    asset = _create_asset()
    request = maintenance_request_create(
        asset=asset,
        title="No arranca motor principal",
        description="El motor principal no arranca.",
        requester_name="Supervisor Producción",
        perceived_priority=MaintenanceRequestPriority.URGENT,
    )

    work_order = work_order_create_from_request(
        maintenance_request=request,
        created_by_user_id=1,
        created_by_name="Planificador",
    )

    request.refresh_from_db()

    assert work_order.source_request == request
    assert work_order.asset == asset
    assert work_order.priority == WorkOrderPriority.URGENT
    assert request.status == MaintenanceRequestStatus.CONVERTED_TO_WORK_ORDER


@pytest.mark.django_db(databases=["client_template"])
def test_assigning_technician_changes_status_to_assigned():
    asset = _create_asset()
    work_order = work_order_create_manual(
        asset=asset,
        title="Fuga de aire",
        description="Fuga en línea principal.",
    )

    assignee = work_order_assign_technician(
        work_order=work_order,
        technician_user_id=10,
        technician_name="Técnico Mecatrónico",
        is_primary=True,
    )

    work_order.refresh_from_db()

    assert assignee.work_order == work_order
    assert work_order.status == WorkOrderStatus.ASSIGNED
    assert work_order.assigned_at is not None


@pytest.mark.django_db(databases=["client_template"])
def test_work_order_cannot_start_without_assignee():
    asset = _create_asset()
    work_order = work_order_create_manual(
        asset=asset,
        title="Sin técnico",
        description="OT sin asignación.",
    )

    with pytest.raises(ValidationError):
        work_order_start(work_order=work_order)


@pytest.mark.django_db(databases=["client_template"])
def test_assigned_work_order_can_be_started():
    work_order = _create_work_order_with_assignee()

    work_order_start(work_order=work_order)
    work_order.refresh_from_db()

    assert work_order.status == WorkOrderStatus.IN_PROGRESS
    assert work_order.started_at is not None


@pytest.mark.django_db(databases=["client_template"])
def test_labor_entry_calculates_duration_minutes():
    work_order = _create_work_order_with_assignee()
    started_at = timezone.now()
    ended_at = started_at + timezone.timedelta(hours=2)

    labor_entry = work_order_labor_entry_create(
        work_order=work_order,
        technician_user_id=10,
        technician_name="Técnico Mecatrónico",
        started_at=started_at,
        ended_at=ended_at,
        notes="Diagnóstico y reparación.",
    )

    assert labor_entry.duration_minutes == 120


@pytest.mark.django_db(databases=["client_template"])
def test_work_order_can_be_technically_closed():
    work_order = _create_work_order_with_assignee()
    work_order_start(work_order=work_order)
    work_order.refresh_from_db()

    work_order_technical_close(
        work_order=work_order,
        diagnosis="Contactor principal dañado.",
        work_performed="Se reemplazó contactor y se realizaron pruebas.",
        probable_cause="Desgaste eléctrico.",
        closed_by_user_id=10,
        closed_by_name="Técnico Mecatrónico",
    )
    work_order.refresh_from_db()

    assert work_order.status == WorkOrderStatus.TECHNICALLY_CLOSED
    assert work_order.technically_closed_at is not None
    assert work_order.technical_report.diagnosis == "Contactor principal dañado."


@pytest.mark.django_db(databases=["client_template"])
def test_technically_closed_work_order_can_be_finally_closed():
    work_order = _create_work_order_with_assignee()
    work_order_start(work_order=work_order)
    work_order.refresh_from_db()
    work_order_technical_close(
        work_order=work_order,
        diagnosis="Falla corregida.",
        work_performed="Se ajustó sistema y se verificó operación.",
    )
    work_order.refresh_from_db()

    work_order_close_final(work_order=work_order)
    work_order.refresh_from_db()

    assert work_order.status == WorkOrderStatus.CLOSED
    assert work_order.closed_at is not None


@pytest.mark.django_db(databases=["client_template"])
def test_open_selector_excludes_cancelled_and_closed_work_orders():
    open_work_order = _create_work_order_with_assignee()

    cancelled_work_order = _create_work_order_with_assignee()
    work_order_cancel(
        work_order=cancelled_work_order,
        reason="Trabajo cancelado por duplicidad.",
    )

    assert list(work_order_list_open()) == [open_work_order]