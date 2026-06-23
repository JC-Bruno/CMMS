import uuid
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q

from apps.assets.choices import AssetStructureNodeType


asset_code_validator = RegexValidator(
    regex=r"^[A-Za-z0-9][A-Za-z0-9_.-]*$",
    message=(
        "Code must start with a letter or number and contain only letters, "
        "numbers, underscores, hyphens, or dots."
    ),
)


class LocationNodeType(models.TextChoices):
    COMPANY = "company", "Company"
    SITE = "site", "Site"
    FACILITY = "facility", "Facility / Building / Hangar"
    AREA = "area", "Area / Process"
    LOCATION = "location", "Location"


class AssetStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    IN_MAINTENANCE = "in_maintenance", "In maintenance"
    OUT_OF_SERVICE = "out_of_service", "Out of service"
    INACTIVE = "inactive", "Inactive"
    RETIRED = "retired", "Retired"


class AssetType(models.TextChoices):
    EQUIPMENT = "equipment", "Equipment"
    INFRASTRUCTURE = "infrastructure", "Infrastructure"
    TOOLING = "tooling", "Tooling"
    VEHICLE = "vehicle", "Vehicle"
    SYSTEM = "system", "System"
    OTHER = "other", "Other"


class AssetCriticality(models.TextChoices):
    NOT_ASSESSED = "not_assessed", "Not assessed"
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"
    CRITICAL = "critical", "Critical"


class AssetDocumentType(models.TextChoices):
    MANUAL = "manual", "Manual"
    DATASHEET = "datasheet", "Datasheet"
    DIAGRAM = "diagram", "Diagram"
    PROCEDURE = "procedure", "Procedure"
    NAMEPLATE = "nameplate", "Nameplate"
    WARRANTY = "warranty", "Warranty"
    INVOICE = "invoice", "Invoice"
    PHOTO = "photo", "Photo"
    OTHER = "other", "Other"


class AssetLocationNode(models.Model):
    ALLOWED_PARENT_TYPES = {
        LocationNodeType.COMPANY: None,
        LocationNodeType.SITE: LocationNodeType.COMPANY,
        LocationNodeType.FACILITY: LocationNodeType.SITE,
        LocationNodeType.AREA: LocationNodeType.FACILITY,
        LocationNodeType.LOCATION: LocationNodeType.AREA,
    }

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    code = models.CharField(
        max_length=80,
        validators=[asset_code_validator],
        help_text="Unique code for this hierarchy node.",
    )
    name = models.CharField(
        max_length=150,
    )
    node_type = models.CharField(
        max_length=30,
        choices=LocationNodeType.choices,
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        null=True,
        blank=True,
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
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["node_type", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["code"],
                condition=models.Q(deleted_at__isnull=True),
                name="unique_active_asset_location_code",
            )
        ]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["node_type"]),
            models.Index(fields=["parent"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["deleted_at"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"

    def clean(self):
        super().clean()

        expected_parent_type = self.ALLOWED_PARENT_TYPES.get(self.node_type)

        if self.parent_id is None:
            if expected_parent_type is not None:
                raise ValidationError(
                    {
                        "parent": (
                            f"{self.get_node_type_display()} nodes must have "
                            "a parent."
                        )
                    }
                )
            return

        if self.parent_id == self.id:
            raise ValidationError(
                {
                    "parent": "A hierarchy node cannot be its own parent."
                }
            )

        if expected_parent_type is None:
            raise ValidationError(
                {
                    "parent": (
                        f"{self.get_node_type_display()} nodes cannot have "
                        "a parent."
                    )
                }
            )

        if self.parent.node_type != expected_parent_type:
            raise ValidationError(
                {
                    "parent": (
                        f"{self.get_node_type_display()} nodes must have "
                        f"a {LocationNodeType(expected_parent_type).label} parent."
                    )
                }
            )


class Asset(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    code = models.CharField(
        max_length=80,
        validators=[asset_code_validator],
        help_text="Unique asset code inside the client database.",
    )
    name = models.CharField(
        max_length=180,
    )
    asset_type = models.CharField(
        max_length=30,
        choices=AssetType.choices,
        default=AssetType.EQUIPMENT,
    )
    status = models.CharField(
        max_length=30,
        choices=AssetStatus.choices,
        default=AssetStatus.ACTIVE,
    )
    criticality = models.CharField(
        max_length=30,
        choices=AssetCriticality.choices,
        default=AssetCriticality.NOT_ASSESSED,
    )
    location = models.ForeignKey(
        AssetLocationNode,
        on_delete=models.PROTECT,
        related_name="assets",
    )
    parent_asset = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="child_assets",
        null=True,
        blank=True,
        help_text="Optional parent asset for future component hierarchy.",
    )
    manufacturer = models.CharField(
        max_length=120,
        blank=True,
    )
    model = models.CharField(
        max_length=120,
        blank=True,
    )
    serial_number = models.CharField(
        max_length=120,
        blank=True,
    )
    technical_specs = models.JSONField(
        default=dict,
        blank=True,
        help_text="Flexible technical data for the asset.",
    )
    acquisition_date = models.DateField(
        null=True,
        blank=True,
    )
    installation_date = models.DateField(
        null=True,
        blank=True,
    )
    notes = models.TextField(
        blank=True,
    )
    is_maintainable = models.BooleanField(
        default=True,
        help_text="Defines whether the asset can receive maintenance orders.",
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
        ordering = ["code"]
        constraints = [
            models.UniqueConstraint(
                fields=["code"],
                condition=models.Q(deleted_at__isnull=True),
                name="unique_active_asset_code",
            )
        ]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["status"]),
            models.Index(fields=["asset_type"]),
            models.Index(fields=["criticality"]),
            models.Index(fields=["location"]),
            models.Index(fields=["parent_asset"]),
            models.Index(fields=["deleted_at"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"

    def clean(self):
        super().clean()

        if self.location_id and self.location.node_type != LocationNodeType.LOCATION:
            raise ValidationError(
                {
                    "location": "Assets must be assigned to a final location node."
                }
            )

        if self.parent_asset_id and self.parent_asset_id == self.id:
            raise ValidationError(
                {
                    "parent_asset": "An asset cannot be its own parent asset."
                }
            )

class AssetStructureNode(models.Model):
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="structure_nodes",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
        blank=True,
    )
    node_type = models.CharField(
        max_length=40,
        choices=AssetStructureNodeType.choices,
    )
    code = models.CharField(max_length=80)
    name = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    is_maintainable = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["asset__code", "sort_order", "code"]
        constraints = [
            models.UniqueConstraint(
                fields=["asset", "code"],
                condition=Q(deleted_at__isnull=True),
                name="unique_active_asset_structure_code_per_asset",
            )
        ]

    def __str__(self):
        return f"{self.asset.code} / {self.code} - {self.name}"

    def clean(self):
        if self.parent and self.parent.asset_id != self.asset_id:
            raise ValidationError(
                "El nodo padre debe pertenecer al mismo activo."
            )

        if self.node_type == AssetStructureNodeType.SUBSYSTEM and self.parent_id is not None:
            raise ValidationError(
                "Un subsistema debe depender directamente del activo y no debe tener padre."
            )

        if self.node_type == AssetStructureNodeType.COMPONENT:
            if self.parent is None:
                raise ValidationError(
                    "Un componente debe depender de un subsistema."
                )

            if self.parent.node_type != AssetStructureNodeType.SUBSYSTEM:
                raise ValidationError(
                    "Un componente solo puede depender de un subsistema."
                )

        if self.node_type == AssetStructureNodeType.MAINTAINABLE_POINT:
            if self.parent is None:
                raise ValidationError(
                    "Un punto mantenible debe depender de un componente."
                )

            if self.parent.node_type != AssetStructureNodeType.COMPONENT:
                raise ValidationError(
                    "Un punto mantenible solo puede depender de un componente."
                )

            self.is_maintainable = True

class AssetDocument(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="documents",
    )
    document_type = models.CharField(
        max_length=30,
        choices=AssetDocumentType.choices,
        default=AssetDocumentType.OTHER,
    )
    title = models.CharField(
        max_length=180,
    )
    document_uri = models.CharField(
        max_length=500,
        blank=True,
        help_text="File path, URL, or storage reference for the document.",
    )
    description = models.TextField(
        blank=True,
    )
    issued_at = models.DateField(
        null=True,
        blank=True,
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
        ordering = ["asset__code", "document_type", "title"]
        indexes = [
            models.Index(fields=["asset"]),
            models.Index(fields=["document_type"]),
            models.Index(fields=["deleted_at"]),
        ]

    def __str__(self):
        return f"{self.asset.code} - {self.title}"