from django.core.management.base import BaseCommand
from django.db import transaction

from apps.accounts.models import OperationalPermission, Role
from apps.accounts.permissions_catalog import OPERATIONAL_PERMISSIONS, ROLE_TEMPLATES
from apps.accounts.services import role_assign_permission


class Command(BaseCommand):
    help = "Seed operational permissions and base roles."

    @transaction.atomic(using="default")
    def handle(self, *args, **options):
        permission_by_code = {}

        for permission_data in OPERATIONAL_PERMISSIONS:
            permission, created = OperationalPermission.objects.update_or_create(
                code=permission_data["code"],
                defaults={
                    "name": permission_data["name"],
                    "module": permission_data["module"],
                    "description": permission_data["description"],
                    "is_active": True,
                },
            )
            permission_by_code[permission.code] = permission

            status = "created" if created else "updated"
            self.stdout.write(f"Permission {status}: {permission.code}")

        for role_data in ROLE_TEMPLATES:
            role, created = Role.objects.update_or_create(
                code=role_data["code"],
                defaults={
                    "name": role_data["name"],
                    "description": role_data["description"],
                    "is_system": True,
                    "is_active": True,
                },
            )

            status = "created" if created else "updated"
            self.stdout.write(f"Role {status}: {role.code}")

            for permission_code in role_data["permission_codes"]:
                permission = permission_by_code[permission_code]
                role_assign_permission(role=role, permission=permission)

        self.stdout.write(self.style.SUCCESS("Access control seed completed."))