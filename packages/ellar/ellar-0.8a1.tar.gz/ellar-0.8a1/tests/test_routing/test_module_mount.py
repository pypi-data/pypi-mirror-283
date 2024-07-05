from ellar.core.routing import EllarMount


class ControlType:
    pass


def test_module_mount_default_handler(test_client_factory):
    mount = EllarMount("/", control_type=ControlType)
    client = test_client_factory(mount.handle)
    res = client.get("/")
    assert res.status_code == 404
    assert res.text == "Not Found"
