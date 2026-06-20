import pytest

from django.core.exceptions import ValidationError

from .models import (
    AssetCriticality,
    AssetDocumentType,
    AssetStatus,
    AssetType,
    LocationNodeType,
)
from .selectors import (
    asset_document_list,
    asset_get_by_code,
    asset_list,
    location_node_children,
    location_node_get_by_code,
)
from .services import (
    asset_create,
    asset_document_create,
    asset_soft_delete,
    location_node_create,
)


def _create_location_tree():
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

    return company, site, facility, area, location


@pytest.mark.django_db(databases=["client_template"])
def test_location_tree_can_be_created_with_required_hierarchy():
    company, site, facility, area, location = _create_location_tree()

    assert site.parent == company
    assert facility.parent == site
    assert area.parent == facility
    assert location.parent == area
    assert location_node_get_by_code(code="loc_plasma_01") == location
    assert list(location_node_children(parent=area)) == [location]


@pytest.mark.django_db(databases=["client_template"])
def test_location_tree_rejects_invalid_parent_hierarchy():
    company = location_node_create(
        code="company",
        name="Grupo Monelca",
        node_type=LocationNodeType.COMPANY,
    )

    with pytest.raises(ValidationError):
        location_node_create(
            code="bad_site",
            name="Bad site",
            node_type=LocationNodeType.SITE,
        )

    with pytest.raises(ValidationError):
        location_node_create(
            code="bad_location",
            name="Bad location",
            node_type=LocationNodeType.LOCATION,
            parent=company,
        )


@pytest.mark.django_db(databases=["client_template"])
def test_asset_can_be_created_only_on_final_location_node():
    _company, _site, _facility, area, location = _create_location_tree()

    with pytest.raises(ValidationError):
        asset_create(
            code="PLASMA-BAD",
            name="Invalid plasma asset",
            location=area,
            asset_type=AssetType.EQUIPMENT,
            status=AssetStatus.ACTIVE,
            criticality=AssetCriticality.NOT_ASSESSED,
        )

    asset = asset_create(
        code="PLASMA-01",
        name="CNC Plasma 01",
        location=location,
        asset_type=AssetType.EQUIPMENT,
        status=AssetStatus.ACTIVE,
        criticality=AssetCriticality.HIGH,
        manufacturer="Hypertherm",
        model="XPR-300",
        serial_number="SN-001",
        technical_specs={
            "voltage": "480 VAC",
            "process": "plasma cutting",
        },
    )

    assert asset_get_by_code(code="PLASMA-01") == asset
    assert list(asset_list()) == [asset]


@pytest.mark.django_db(databases=["client_template"])
def test_asset_soft_delete_hides_asset_from_default_selectors():
    _company, _site, _facility, _area, location = _create_location_tree()

    asset = asset_create(
        code="COMP-01",
        name="Air compressor 01",
        location=location,
        asset_type=AssetType.EQUIPMENT,
        status=AssetStatus.ACTIVE,
        criticality=AssetCriticality.MEDIUM,
    )

    asset_soft_delete(asset=asset)

    assert asset_get_by_code(code="COMP-01") is None
    assert list(asset_list()) == []


@pytest.mark.django_db(databases=["client_template"])
def test_asset_document_can_be_registered_for_asset():
    _company, _site, _facility, _area, location = _create_location_tree()

    asset = asset_create(
        code="CRANE-01",
        name="Overhead Crane 01",
        location=location,
        asset_type=AssetType.EQUIPMENT,
        status=AssetStatus.ACTIVE,
        criticality=AssetCriticality.CRITICAL,
    )

    document = asset_document_create(
        asset=asset,
        document_type=AssetDocumentType.MANUAL,
        title="Operation Manual",
        document_uri="documents/assets/crane-01/manual.pdf",
    )

    assert list(asset_document_list(asset=asset)) == [document]


@pytest.mark.django_db(databases=["client_template"])
def test_asset_code_rejects_invalid_format():
    _company, _site, _facility, _area, location = _create_location_tree()

    with pytest.raises(ValidationError):
        asset_create(
            code="BAD CODE WITH SPACES",
            name="Invalid code asset",
            location=location,
            asset_type=AssetType.EQUIPMENT,
            status=AssetStatus.ACTIVE,
            criticality=AssetCriticality.NOT_ASSESSED,
        )