from config.database_routers import CMMSDatabaseRouter


class FakeMeta:
    def __init__(self, app_label):
        self.app_label = app_label


class FakeModelOrObject:
    def __init__(self, app_label):
        self._meta = FakeMeta(app_label)


def test_control_apps_are_routed_to_default_database():
    router = CMMSDatabaseRouter()
    model = FakeModelOrObject("tenancy")

    assert router.db_for_read(model) == "default"
    assert router.db_for_write(model) == "default"


def test_client_apps_are_routed_to_client_template_database():
    router = CMMSDatabaseRouter()
    model = FakeModelOrObject("assets")

    assert router.db_for_read(model) == "client_template"
    assert router.db_for_write(model) == "client_template"


def test_control_apps_migrate_only_on_default_database():
    router = CMMSDatabaseRouter()

    assert router.allow_migrate("default", "tenancy") is True
    assert router.allow_migrate("client_template", "tenancy") is False


def test_client_apps_migrate_only_on_client_template_database():
    router = CMMSDatabaseRouter()

    assert router.allow_migrate("client_template", "assets") is True
    assert router.allow_migrate("default", "assets") is False


def test_unknown_apps_do_not_migrate_by_default():
    router = CMMSDatabaseRouter()

    assert router.allow_migrate("default", "unknown_app") is False
    assert router.allow_migrate("client_template", "unknown_app") is False


def test_relations_are_allowed_inside_same_database_group():
    router = CMMSDatabaseRouter()

    tenant = FakeModelOrObject("tenancy")
    account = FakeModelOrObject("accounts")

    assert router.allow_relation(tenant, account) is True


def test_relations_are_not_allowed_between_control_and_client_groups():
    router = CMMSDatabaseRouter()

    tenant = FakeModelOrObject("tenancy")
    asset = FakeModelOrObject("assets")

    assert router.allow_relation(tenant, asset) is False