import typing as t

from ellar.common.constants import SCOPE_RESPONSE_STARTED
from ellar.common.interfaces import IExceptionHandler, IHostContextFactory
from ellar.common.responses import Response
from ellar.common.types import ASGIApp, TMessage, TReceive, TScope, TSend
from ellar.core.connection.http import Request
from ellar.di import EllarInjector
from starlette.middleware.errors import (
    ServerErrorMiddleware as BaseServerErrorMiddleware,
)
from starlette.requests import Request as StarletteRequest
from starlette.responses import JSONResponse


class ServerErrorMiddleware(BaseServerErrorMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        *,
        debug: bool,
        injector: "EllarInjector",
        handler: t.Optional["IExceptionHandler"] = None,
    ) -> None:
        _handler = None
        if handler:
            self._500_error_handler = handler
            _handler = self.error_handler

        super(ServerErrorMiddleware, self).__init__(
            debug=debug,
            handler=_handler,  # type:ignore[arg-type]
            app=app,
        )
        self.injector = injector

    async def __call__(self, scope: TScope, receive: TReceive, send: TSend) -> None:
        if scope["type"] not in ["http", "websocket"]:  # pragma: no cover
            await super().__call__(scope, receive, send)
            return

        scope[SCOPE_RESPONSE_STARTED] = False

        async def sender(message: TMessage) -> None:
            if (
                message["type"] == "http.response.start"
                or message["type"] == "websocket.accept"
            ):
                scope[SCOPE_RESPONSE_STARTED] = True
            await send(message)
            return

        if scope["type"] == "http":
            await super().__call__(scope, receive, sender)
        else:
            await self.app(scope, receive, sender)

    async def error_handler(self, request: Request, exc: Exception) -> Response:
        host_context_factory: IHostContextFactory = self.injector.get(
            IHostContextFactory
        )
        host_context = host_context_factory.create_context(request.scope)

        assert self._500_error_handler
        response = await self._500_error_handler.catch(host_context, exc)
        return response

    def error_response(self, request: StarletteRequest, exc: Exception) -> Response:
        return JSONResponse(
            {"detail": "Internal server error", "status_code": 500}, status_code=500
        )
