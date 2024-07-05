from abc import ABC
from unittest.mock import patch

import click
import pytest
from ellar.app import App
from ellar.common import (
    Controller,
    ControllerBase,
    IModuleSetup,
    Module,
    ModuleRouter,
    get,
)
from ellar.common.constants import MODULE_METADATA
from ellar.common.exceptions import ImproperConfiguration
from ellar.core import Config, DynamicModule, LazyModuleImport, ModuleBase, ModuleSetup
from ellar.core.modules import ModuleRefBase
from ellar.core.router_builders import ModuleRouterBuilder
from ellar.core.services import Reflector
from ellar.di import EllarInjector, ModuleTreeManager, ProviderConfig, exceptions
from ellar.reflect import reflect
from ellar.testing import Test

from ..main import router


@click.command(name="command-one")
def command_one():
    click.echo("Hello World command one")


@click.command(name="command-two")
def command_two():
    click.echo("Hello World command two")


class IDynamic(ABC):
    a: int
    b: float


class SampleController(ControllerBase):
    @get("/sample")
    def sample_example(self):
        return {"message": 'You have reached "sample_example" home route'}


@Module(routers=(router,))
class SimpleModule(ModuleBase):
    @classmethod
    def invalid_setup(cls):
        return IDynamic


@Module(routers=(router,), exports=[IDynamic])
class DynamicInstantiatedModule(ModuleBase, IModuleSetup):
    @classmethod
    def setup(cls, a: int, b: int) -> DynamicModule:
        dynamic_type = type("DynamicSample", (IDynamic,), {"a": a, "b": b})
        dynamic_router = ModuleRouter("/dynamic")

        @dynamic_router.get("/index")
        async def home():
            return {"message": 'You have reached "dynamic" home route'}

        dynamic_controller = Controller("/dynamic-controller")(SampleController)

        return DynamicModule(
            cls,
            providers=[ProviderConfig(IDynamic, use_class=dynamic_type)],
            routers=[
                dynamic_router,
            ],
            controllers=[dynamic_controller],
        )


@Module()
class DynamicModuleSetupRegisterModule(ModuleBase, IModuleSetup):
    @classmethod
    def setup(cls, a: int, b: int) -> DynamicModule:
        dynamic_type = type("DynamicSample", (IDynamic,), {"a": a, "b": b})
        return DynamicModule(
            cls,
            providers=[ProviderConfig(IDynamic, use_class=dynamic_type, export=True)],
        )

    @classmethod
    def setup_register(cls) -> ModuleSetup:
        return ModuleSetup(cls, inject=[Config], factory=cls.setup_register_factory)

    @staticmethod
    def setup_register_factory(
        module_ref: ModuleRefBase, config: Config
    ) -> DynamicModule:
        return module_ref.module.setup(config.a, config.b)


SimpleModuleImportStr = "tests.test_modules.test_module_config:SimpleModule"
DynamicModuleSetupRegisterModuleImportStr = (
    "tests.test_modules.test_module_config:DynamicModuleSetupRegisterModule"
)


@Module(modules=[LazyModuleImport(SimpleModuleImportStr)])
class LazyModuleImportWithoutDynamicSetup(ModuleBase):
    pass


@Module(
    modules=[
        LazyModuleImport(
            DynamicModuleSetupRegisterModuleImportStr, "setup", a=233, b=344
        )
    ]
)
class LazyModuleImportWithDynamicSetup(ModuleBase):
    pass


@Module(
    modules=[
        LazyModuleImport(DynamicModuleSetupRegisterModuleImportStr, "setup_register")
    ]
)
class LazyModuleImportWithSetup(ModuleBase):
    pass


@Module(commands=[command_one])
class DynamicModuleRegisterCommand(ModuleBase, IModuleSetup):
    @classmethod
    def setup(cls, command_three_text: str) -> DynamicModule:
        @click.command
        def command_three():
            click.echo(command_three_text)

        return DynamicModule(cls, commands=[command_one, command_two, command_three])


def test_invalid_lazy_module_import(reflect_context):
    with pytest.raises(ImproperConfiguration) as ex:
        LazyModuleImport("tests.test_modules.test_module_config:IDynamic").get_module()
    assert str(ex.value) == "IDynamic is not a valid Module"


def test_lazy_module_import_fails_for_invalid_import(reflect_context):
    with pytest.raises(ImproperConfiguration) as ex:
        LazyModuleImport("tests.test_modules.test_module_config:IDynamic2").get_module()
    assert (
        str(ex.value)
        == 'Unable to import "tests.test_modules.test_module_config:IDynamic2" registered in "ApplicationModule"'
    )

    with pytest.raises(ImproperConfiguration) as ex:
        LazyModuleImport("tests.test_modules.test_module_config:IDynamic2").get_module(
            "xyzModule"
        )
    assert (
        str(ex.value)
        == 'Unable to import "tests.test_modules.test_module_config:IDynamic2" registered in "xyzModule"'
    )


def test_lazy_module_import_fails_for_dynamic_setup(reflect_context):
    with pytest.raises(ImproperConfiguration) as ex:
        LazyModuleImport(SimpleModuleImportStr, "invalid_setup").get_module()
    assert (
        str(ex.value)
        == "Lazy Module import with setup attribute must return a DynamicModule/ModuleSetup instance"
    )


def test_lazy_module_import(reflect_context):
    test_module = Test.create_test_module(
        modules=(LazyModuleImportWithoutDynamicSetup,)
    )
    assert len(test_module.create_application().routes[0].routes) == 39
    with pytest.raises(exceptions.UnsatisfiedRequirement):
        test_module.get(IDynamic)


def test_lazy_module_import_with_dynamic_module_setup(reflect_context):
    test_module = Test.create_from_module(LazyModuleImportWithDynamicSetup)
    dynamic_instance = test_module.get(IDynamic)
    assert dynamic_instance.b == 344 and dynamic_instance.a == 233


def test_lazy_module_import_with_dynamic_setup(reflect_context):
    test_module = Test.create_test_module(
        modules=(LazyModuleImportWithSetup,), config_module={"a": 233, "b": 445}
    )
    dynamic_instance = test_module.get(IDynamic)
    assert dynamic_instance.b == 445 and dynamic_instance.a == 233


def test_dynamic_module_haves_routes(reflect_context):
    routers = reflect.get_metadata(MODULE_METADATA.ROUTERS, DynamicInstantiatedModule)
    assert len(routers) == 1
    mount0 = ModuleRouterBuilder.build(routers[0])
    assert len(mount0.routes) == 39
    tm = Test.create_test_module(
        modules=(DynamicInstantiatedModule.setup(a=233, b=344),),
    )
    tm.create_application()
    routers = reflect.get_metadata(MODULE_METADATA.ROUTERS, DynamicInstantiatedModule)
    assert len(routers) == 1
    mount0 = ModuleRouterBuilder.build(routers[0])
    assert len(mount0.routes) == 1


def test_dynamic_module_setup_providers_works(reflect_context):
    test_module = Test.create_test_module(
        modules=(DynamicInstantiatedModule.setup(a=233, b=344),)
    )
    dynamic_object = test_module.get(IDynamic)
    assert dynamic_object.a == 233 and dynamic_object.b == 344


def test_dynamic_module_setup_router_controllers_works(reflect_context):
    test_module = Test.create_test_module(
        modules=(DynamicInstantiatedModule.setup(a=233, b=344),),
        config_module={"STATIC_MOUNT_PATH": None},
    )
    assert len(test_module.create_application().routes) == 2
    client = test_module.get_test_client()

    res = client.get("/dynamic/index")
    assert res.status_code == 200
    assert res.json() == {"message": 'You have reached "dynamic" home route'}

    res = client.get("/dynamic-controller/sample")
    assert res.status_code == 200
    assert res.json() == {"message": 'You have reached "sample_example" home route'}


def test_dynamic_module_setup_register_works(reflect_context):
    test_module = Test.create_test_module(
        modules=(DynamicModuleSetupRegisterModule.setup_register(),),
        config_module={"a": 24555, "b": 8899900, "STATIC_MOUNT_PATH": None},
    )
    assert len(test_module.create_application().routes) == 0
    dynamic_instance = test_module.get(IDynamic)
    assert dynamic_instance.a == 24555
    assert dynamic_instance.b == 8899900


@pytest.mark.parametrize(
    "name, dependencies",
    [
        ("depends on nothing but has factory", []),
        ("depends only on config", [Config]),
        ("depends on other services", [Config, Reflector]),
        (
            "depends on other services and Application instance",
            [Config, Reflector, App],
        ),
    ],
)
def test_module_setup_with_factory_works(name, dependencies, reflect_context):
    def dynamic_instantiate_factory(module_ref: ModuleRefBase, *args):
        for _type, instance in zip(dependencies, args):
            assert isinstance(instance, _type)
        return module_ref.module.setup(a=233, b=344)

    test_module = Test.create_test_module(
        modules=[
            ModuleSetup(
                DynamicInstantiatedModule,
                factory=dynamic_instantiate_factory,
                inject=dependencies,
            )
        ]
    )

    dynamic_object = test_module.get(IDynamic)
    assert dynamic_object.a == 233 and dynamic_object.b == 344
    client = test_module.get_test_client()

    res = client.get("/dynamic/index")
    assert res.status_code == 200
    assert res.json() == {"message": 'You have reached "dynamic" home route'}


def test_invalid_module_setup(reflect_context):
    config = Config()
    injector = EllarInjector()
    injector.container.register(
        ModuleTreeManager,
        ModuleTreeManager(),
    )

    def dynamic_instantiate_factory(module_ref: ModuleRefBase, *args):
        return ModuleSetup(module_ref.module)

    with pytest.raises(ImproperConfiguration) as ex:
        ModuleSetup(module=IDynamic)
    assert str(ex.value) == "IDynamic is not a valid Module"

    module_setup = ModuleSetup(
        DynamicInstantiatedModule, factory=dynamic_instantiate_factory
    )

    with pytest.raises(Exception) as ex:
        module_setup.get_module_ref(config, injector.container)
    assert (
        str(ex.value)
        == "Factory function for DynamicInstantiatedModule module configuration must return `DynamicModule` instance"
    )


def test_invalid_dynamic_module_setup(reflect_context):
    with pytest.raises(ImproperConfiguration) as ex:
        DynamicModule(module=IDynamic)
    assert str(ex.value) == "IDynamic is not a valid Module"


def test_can_not_apply_dynamic_module_twice(reflect_context):
    dynamic_type = type("DynamicSample", (IDynamic,), {"a": "1222", "b": "121212"})
    with patch.object(reflect.__class__, "define_metadata") as mock_define_metadata:
        dynamic_module = DynamicModule(
            module=DynamicInstantiatedModule,
            providers=[ProviderConfig(IDynamic, use_class=dynamic_type)],
        )
        dynamic_module.apply_configuration()
        assert mock_define_metadata.called

    with patch.object(reflect.__class__, "define_metadata") as mock_define_metadata:
        dynamic_module.apply_configuration()
        assert mock_define_metadata.called is False


def test_dynamic_command_register_command(cli_runner, reflect_context):
    commands = reflect.get_metadata(
        MODULE_METADATA.COMMANDS, DynamicModuleRegisterCommand
    )
    assert len(commands) == 1
    res = cli_runner.invoke(commands[0], [])
    assert res.stdout == "Hello World command one\n"

    DynamicModuleRegisterCommand.setup("Command Three Here").apply_configuration()
    commands = reflect.get_metadata(
        MODULE_METADATA.COMMANDS, DynamicModuleRegisterCommand
    )
    assert len(commands) == 3

    res = cli_runner.invoke(commands[2], [])
    assert res.stdout == "Command Three Here\n"

    assert len(reflect._meta_data) > 10
