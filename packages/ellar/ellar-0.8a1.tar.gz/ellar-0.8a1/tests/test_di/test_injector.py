import pytest
from ellar.common import Module
from ellar.core import ModuleBase
from ellar.di import (
    SCOPED_CONTEXT_VAR,
    Container,
    EllarInjector,
    request_scope,
    transient_scope,
)
from ellar.di.providers import ClassProvider, InstanceProvider
from injector import Binder, Injector, UnsatisfiedRequirement

from .examples import Foo, Foo1, Foo2


class EllarTestPlainModule(ModuleBase):
    pass


@Module(template_folder="some_template")
class EllarTestTemplateModule(ModuleBase):
    pass


def test_container_install_module_case_1():
    called = False
    app_container = EllarInjector().container

    class PlainModule(ModuleBase):
        def register_services(self, container: Container) -> None:
            nonlocal called
            called = True

    @Module()
    class DecoratedModuleWithBase(ModuleBase):
        def register_services(self, container: Container) -> None:
            nonlocal called
            called = True

    plain_module = app_container.install(PlainModule)
    assert called
    assert isinstance(plain_module, PlainModule)

    called = False

    decorated_module = app_container.install(DecoratedModuleWithBase)
    assert called
    assert isinstance(decorated_module, DecoratedModuleWithBase)

    called = False
    app_container.install(PlainModule())
    assert called

    called = False

    app_container.install(DecoratedModuleWithBase())
    assert called


def test_container_install_module_return_case_2():
    called = False
    app_container = EllarInjector().container

    @Module()
    class DecoratedModule:
        def register_services(self, container: Container) -> None:
            nonlocal called
            called = True

    decorated_module = app_container.install(DecoratedModule)
    assert called is False
    assert isinstance(decorated_module, DecoratedModule)

    decorated_module = app_container.install(DecoratedModule())
    assert called is False
    assert isinstance(decorated_module, DecoratedModule)


def test_default_container_registration():
    injector = EllarInjector(auto_bind=False)
    assert isinstance(injector.get(Container), Container)
    assert isinstance(injector.get(EllarInjector), EllarInjector)
    assert isinstance(injector.get(EllarInjector), EllarInjector)

    with pytest.raises(UnsatisfiedRequirement):
        injector.get(Injector)

    with pytest.raises(UnsatisfiedRequirement):
        injector.get(Binder)


@pytest.mark.asyncio
async def test_request_service_context():
    injector = EllarInjector(auto_bind=False)
    injector.container.register(Foo1, scope=request_scope)
    injector.container.register(Foo2, scope=transient_scope)

    async with injector.create_asgi_args():
        asgi_context = SCOPED_CONTEXT_VAR.get()

        foo1 = injector.get(Foo1)  # result will be tracked by asgi_context
        injector.get(Foo2)  # registered as transient scoped

        assert isinstance(asgi_context.context[Foo1], InstanceProvider)
        assert asgi_context.context.get(Foo2) is None

        # transient scoped
        foo2 = injector.get(Foo2)
        assert isinstance(foo2, Foo2)
        assert injector.get(Foo2) != foo2  # transient scoped

        assert injector.get(Foo1) == foo1  # still within the context....

        with pytest.raises(UnsatisfiedRequirement):
            injector.get(Foo)

    with pytest.raises(UnsatisfiedRequirement):
        injector.get(Foo1)


@pytest.mark.asyncio
async def test_injector_update_scoped_context():
    injector = EllarInjector(auto_bind=False)

    async with injector.create_asgi_args():
        asgi_context = SCOPED_CONTEXT_VAR.get()

        injector.update_scoped_context(Foo1, Foo1())
        injector.update_scoped_context(Foo, ClassProvider(Foo))

        assert isinstance(asgi_context.context[Foo1], InstanceProvider)
        assert isinstance(asgi_context.context[Foo], ClassProvider)

    injector.update_scoped_context(Foo1, Foo1())
    assert SCOPED_CONTEXT_VAR.get() is None
