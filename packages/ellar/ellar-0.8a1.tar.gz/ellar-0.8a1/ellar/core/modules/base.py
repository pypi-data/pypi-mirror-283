import typing as t

from ellar.common.constants import MODULE_FIELDS
from ellar.di.injector import Container
from injector import Binder
from injector import Module as _InjectorModule

from .builder import ModuleBaseBuilder

if t.TYPE_CHECKING:  # pragma: no cover
    from ellar.core.conf import Config


class ModuleBaseMeta(type):
    MODULE_FIELDS: t.Dict = {}

    def build_module_actions(cls) -> None:
        ModuleBaseBuilder(cls).build()

    @t.no_type_check
    def __init__(cls, name, bases, namespace) -> None:
        super().__init__(name, bases, namespace)
        setattr(cls, MODULE_FIELDS, {})

        # for base in reversed(bases):
        #     ModuleBaseBuilder(cls).build(getattr(base, MODULE_FIELDS, base.__dict__))
        # ModuleBaseBuilder(cls).build(namespace)


class ModuleBase(_InjectorModule, metaclass=ModuleBaseMeta):
    @classmethod
    def before_init(cls, config: "Config") -> t.Dict:
        """Before Module initialisation. Whatever value that is returned here will be passed
        to the Module constructor during initialisation"""
        return {}

    def register_services(self, container: Container) -> None:
        """Register other services manually"""

    def configure(self, container: Binder) -> None:
        """Injector Module Support. Override register_services instead"""
        self.register_services(t.cast(Container, container))
