class CMMSDatabaseRouter:
    """
    Routes CMMS apps to the correct database.

    Control database:
    - Platform administration.
    - Tenants.
    - Users.
    - Roles and permissions.

    Client template database:
    - Operational CMMS modules.
    - Assets.
    - Work orders.
    - Inventory.
    - Reports.
    """

    CONTROL_APP_LABELS = {
        "admin",
        "auth",
        "contenttypes",
        "sessions",
        "core",
        "tenancy",
        "accounts",
    }

    CLIENT_APP_LABELS = {
        "assets",
        "maintenance_requests",
        "work_orders",
        "inventory",
        "reporting",
    }

    def db_for_read(self, model, **hints):
        app_label = model._meta.app_label

        if app_label in self.CONTROL_APP_LABELS:
            return "default"

        if app_label in self.CLIENT_APP_LABELS:
            return "client_template"

        return None

    def db_for_write(self, model, **hints):
        app_label = model._meta.app_label

        if app_label in self.CONTROL_APP_LABELS:
            return "default"

        if app_label in self.CLIENT_APP_LABELS:
            return "client_template"

        return None

    def allow_relation(self, obj1, obj2, **hints):
        obj1_group = self._database_group(obj1._meta.app_label)
        obj2_group = self._database_group(obj2._meta.app_label)

        if obj1_group is None or obj2_group is None:
            return None

        return obj1_group == obj2_group

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.CONTROL_APP_LABELS:
            return db == "default"

        if app_label in self.CLIENT_APP_LABELS:
            return db == "client_template"

        return False

    def _database_group(self, app_label):
        if app_label in self.CONTROL_APP_LABELS:
            return "control"

        if app_label in self.CLIENT_APP_LABELS:
            return "client"

        return None