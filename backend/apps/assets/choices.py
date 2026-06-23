from django.db import models


class AssetStructureNodeType(models.TextChoices):
    SUBSYSTEM = "subsystem", "Subsistema"
    COMPONENT = "component", "Componente"
    MAINTAINABLE_POINT = "maintainable_point", "Punto mantenible"