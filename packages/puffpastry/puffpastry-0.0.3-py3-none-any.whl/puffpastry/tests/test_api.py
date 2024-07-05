import pytest

from puffpastry import Application, create, provides


def test_create():
    app = create("test_app")

    assert isinstance(app, Application)


def test_provides_and_load():
    cls = type("MyClass")

    @provides("my_component")
    def create_component(app):
        obj = cls()
        return obj

    app = create("test_app").load("my_component")

    assert isinstance(app, Application)
    assert isinstance(app.my_component, cls)


def test_create_twice_without_force():
    create("test_app")
    with pytest.raises(KeyError):
        create("test_App", force=False)
