import typing as t

from ellar.common.interfaces import IExecutionContext
from ellar.common.logging import request_logger
from ellar.common.models import ControllerBase


class ControllerRouteOperationBase:
    _controller_type: t.Optional[t.Type["ControllerBase"]] = None
    endpoint: t.Callable
    get_controller_type: t.Callable

    def __init__(
        self, controller_type: t.Type[ControllerBase], *args: t.Any, **kwargs: t.Any
    ) -> None:
        self._controller_type = controller_type

        super().__init__(*args, **kwargs)

    def _get_controller_instance(self, ctx: IExecutionContext) -> ControllerBase:
        request_logger.debug("Getting Controller Instance")
        controller_type: t.Type[ControllerBase] = self.get_controller_type()

        service_provider = ctx.get_service_provider()

        controller_instance: ControllerBase = service_provider.get(controller_type)
        controller_instance.context = ctx
        return controller_instance

    # @t.no_type_check
    # def __call__(
    #     self, context: IExecutionContext, *args: t.Any, **kwargs: t.Any
    # ) -> t.Any:
    #     request_logger.debug("Calling Controller Endpoint manually")
    #     controller_instance = self._get_controller_instance(ctx=context)
    #     return self.endpoint(controller_instance, *args, **kwargs)
