import pytest

from django.core.exceptions import ValidationError

from apps.assets.models import (
    AssetCriticality,
    AssetStatus,
    AssetType,
    LocationNodeType,
)
from apps.assets.services import asset_create, location_node_create

from .models import (
    MaintenanceRequestPriority,
    MaintenanceRequestStatus,
)
from .selectors import (
    maintenance_request_get_by_number,
    maintenance_request_list_by_asset,
    maintenance_request_list_open,
)
from .services import (
    maintenance_request_cancel,
    maintenance_request_create,
    maintenance_request_mark_converted,
    maintenance_request_mark_received,
    maintenance_request_reject,
)


def _create_location_tree_and_asset():
    company = location_node_create(
        code="company",
        name="Grupo Monelca",
        node_type=LocationNodeType.COMPANY,
    )
    site = location_node_create(
        code="site_sv",
        name="El Salvador",
        node_type=LocationNodeType.SITE,
        parent=company,
    )
    facility = location_node_create(
        code="plant_opico",
        name="Planta Opico",
        node_type=LocationNodeType.FACILITY,
        parent=site,
    )
    area = location_node_create(
        code="area_cutting",
        name="Área de corte",
        node_type=LocationNodeType.AREA,
        parent=facility,
    )
    location = location_node_create(
        code="loc_plasma_01",
        name="Ubicación plasma CNC 01",
        node_type=LocationNodeType.LOCATION,
        parent=area,
    )
    asset = asset_create(
        code="PLASMA-01",
        name="CNC Plasma 01",
        location=location,
        asset_type=AssetType.EQUIPMENT,
        status=AssetStatus.ACTIVE,
        criticality=AssetCriticality.HIGH,
    )

    return asset


@pytest.mark.django_db(databases=["client_template"])
def test_maintenance_request_can_be_created_for_asset():
    asset = _create_location_tree_and_asset()

    request = maintenance_request_create(
        asset=asset,
        title="No enciende la fuente plasma",
        description="El operador reporta que la fuente no enciende al iniciar turno.",
        requester_name="Supervisor Producción",
        requester_user_id=1,
        requester_email="supervisor@example.com",
        perceived_priority=MaintenanceRequestPriority.HIGH,
        asset_was_stopped=True,
        production_impact=True,
    )

    assert request.asset == asset
    assert request.status == MaintenanceRequestStatus.CREATED
    assert request.is_confirmed_by_requester is True
    assert request.confirmed_at is not None
    assert request.request_number.startswith("MR-")
    assert maintenance_request_get_by_number(
        request_number=request.request_number
    ) == request


@pytest.mark.django_db(databases=["client_template"])
def test_maintenance_request_can_be_marked_received():
    asset = _create_location_tree_and_asset()
    request = maintenance_request_create(
        asset=asset,
        title="Fuga de aire",
        description="Se detecta fuga de aire en línea principal.",
        requester_name="Supervisor Producción",
    )

    maintenance_request_mark_received(request=request)
    request.refresh_from_db()

    assert request.status == MaintenanceRequestStatus.RECEIVED
    assert request.received_at is not None


@pytest.mark.django_db(databases=["client_template"])
def test_maintenance_request_can_be_rejected_with_reason():
    asset = _create_location_tree_and_asset()
    request = maintenance_request_create(
        asset=asset,
        title="Reporte duplicado",
        description="Reporte posiblemente duplicado.",
        requester_name="Supervisor Producción",
    )

    maintenance_request_reject(
        request=request,
        reason="Solicitud duplicada.",
    )
    request.refresh_from_db()

    assert request.status == MaintenanceRequestStatus.REJECTED
    assert request.rejected_at is not None
    assert request.status_reason == "Solicitud duplicada."


@pytest.mark.django_db(databases=["client_template"])
def test_maintenance_request_can_be_cancelled_with_reason():
    asset = _create_location_tree_and_asset()
    request = maintenance_request_create(
        asset=asset,
        title="Ruido anormal",
        description="Ruido ya no se presenta.",
        requester_name="Supervisor Producción",
    )

    maintenance_request_cancel(
        request=request,
        reason="El problema desapareció antes de inspección.",
    )
    request.refresh_from_db()

    assert request.status == MaintenanceRequestStatus.CANCELLED
    assert request.cancelled_at is not None


@pytest.mark.django_db(databases=["client_template"])
def test_maintenance_request_can_be_marked_converted():
    asset = _create_location_tree_and_asset()
    request = maintenance_request_create(
        asset=asset,
        title="Motor no arranca",
        description="Motor principal no arranca.",
        requester_name="Supervisor Producción",
    )

    maintenance_request_mark_converted(request=request)
    request.refresh_from_db()

    assert request.status == MaintenanceRequestStatus.CONVERTED_TO_WORK_ORDER
    assert request.converted_at is not None


@pytest.mark.django_db(databases=["client_template"])
def test_open_selector_excludes_closed_request_statuses():
    asset = _create_location_tree_and_asset()

    open_request = maintenance_request_create(
        asset=asset,
        title="Falla abierta",
        description="Solicitud pendiente de recepción.",
        requester_name="Supervisor Producción",
    )
    rejected_request = maintenance_request_create(
        asset=asset,
        title="Falla rechazada",
        description="Solicitud que será rechazada.",
        requester_name="Supervisor Producción",
    )

    maintenance_request_reject(
        request=rejected_request,
        reason="No corresponde a mantenimiento.",
    )

    assert list(maintenance_request_list_open()) == [open_request]
    assert list(maintenance_request_list_by_asset(asset=asset)).count(open_request) == 1


@pytest.mark.django_db(databases=["client_template"])
def test_maintenance_request_rejects_deleted_asset():
    asset = _create_location_tree_and_asset()
    asset.deleted_at = asset.created_at
    asset.save(update_fields=["deleted_at", "updated_at"])

    with pytest.raises(ValidationError):
        maintenance_request_create(
            asset=asset,
            title="Activo eliminado",
            description="No debe permitir solicitud para activo eliminado.",
            requester_name="Supervisor Producción",
        )