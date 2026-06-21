from django.db import models


class InventoryLocationType(models.TextChoices):
    WAREHOUSE = "warehouse", "Warehouse"
    AREA_STOCK = "area_stock", "Area stock"
    TECHNICIAN_KIT = "technician_kit", "Technician kit"
    SUPPLIER = "supplier", "Supplier"
    OTHER = "other", "Other"


class SparePartStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    OBSOLETE = "obsolete", "Obsolete"


class StockMovementType(models.TextChoices):
    INITIAL_BALANCE = "initial_balance", "Initial balance"
    RECEIPT = "receipt", "Receipt"
    ISSUE = "issue", "Issue"
    RETURN = "return", "Return"
    ADJUSTMENT_IN = "adjustment_in", "Adjustment in"
    ADJUSTMENT_OUT = "adjustment_out", "Adjustment out"


class StockMovementReason(models.TextChoices):
    INITIAL_LOAD = "initial_load", "Initial load"
    PURCHASE = "purchase", "Purchase"
    MAINTENANCE_USE = "maintenance_use", "Maintenance use"
    RETURN_FROM_MAINTENANCE = "return_from_maintenance", "Return from maintenance"
    PHYSICAL_COUNT = "physical_count", "Physical count"
    DAMAGE = "damage", "Damage"
    LOSS = "loss", "Loss"
    CORRECTION = "correction", "Correction"
    OTHER = "other", "Other"