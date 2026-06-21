from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

from apps.accounts.models import Role, TenantUser
from apps.accounts.services import tenant_user_assign_role, tenant_user_create
from apps.tenancy.models import Tenant, TenantStatus


class Command(BaseCommand):
    help = "Create a local demo tenant and admin user for frontend auth testing."

    def add_arguments(self, parser):
        parser.add_argument("--username", default="admin")
        parser.add_argument("--password", default="admin12345")
        parser.add_argument("--tenant-code", default="demo")
        parser.add_argument("--tenant-name", default="Demo CMMS")

    def handle(self, *args, **options):
        username = options["username"]
        password = options["password"]
        tenant_code = options["tenant_code"]
        tenant_name = options["tenant_name"]

        call_command("seed_access_control")

        tenant, _created = Tenant.objects.update_or_create(
            code=tenant_code,
            defaults={
                "name": tenant_name,
                "status": TenantStatus.ACTIVE,
                "database_name": "cmms_client_template",
            },
        )

        user_model = get_user_model()
        user, _created = user_model.objects.get_or_create(
            username=username,
            defaults={
                "email": f"{username}@example.com",
                "first_name": "Demo",
                "last_name": "Admin",
                "is_staff": True,
            },
        )
        user.set_password(password)
        user.save()

        role = Role.objects.get(code="system_admin")

        tenant_user = TenantUser.objects.filter(
            tenant=tenant,
            user=user,
            deleted_at__isnull=True,
        ).first()

        if tenant_user is None:
            tenant_user = tenant_user_create(
                tenant=tenant,
                user=user,
                display_name=user.username,
            )

        tenant_user_assign_role(tenant_user=tenant_user, role=role)

        self.stdout.write(
            self.style.SUCCESS(
                f"Demo access ready. username={username}, tenant={tenant_code}"
            )
        )