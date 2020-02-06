import asyncio
import traceback
from typing import TYPE_CHECKING

from tonberry import response as response_context
from tonberry.context_var_manager import set_context_var
from tonberry.contexted.request import Request
from tonberry.contexted.response import Response
from tonberry.exceptions import HTTPError, HTTPRedirect
from tonberry.models import Receive, Scope, Send
from tonberry.websocket import WebSocket

if TYPE_CHECKING:
    from tonberry.app import App


class Handler:
    def __init__(self, app: "App", scope: Scope):
        self.app = app
        self.scope = scope

    async def __call__(self, recieve: Receive, send: Send) -> None:
        raise NotImplementedError


class HTTPHandler(Handler):
    def __init__(self, app: "App", scope: Scope):
        super().__init__(app, scope)

    async def __call__(self, recieve: Receive, send: Send) -> None:
        request = Request(self.scope, recieve)
        try:
            await self.handle_request(request, send)
        except HTTPError as err:
            response = Response()
            response.status = err.args[0]
            # noinspection PyTypeHints
            response.body = str(err.args[0]).encode("utf-8")  # type: ignore
            set_context_var(response_context, response)
            self.app.http_access_logger.error()
            await self.handle_exception(response, send)
        except HTTPRedirect as err:
            response = Response()
            response.status = err.code
            response.headers["Location"] = err.route
            set_context_var(response_context, response)
            self.app.http_access_logger.info()
            await self.handle_exception(response, send)
        except Exception as err:
            response = Response()
            # noinspection PyTypeHints
            response.body = traceback.format_exc().encode("utf-8")  # type: ignore
            response.status = 500
            set_context_var(response_context, response)
            self.app.http_access_logger.error()
            self.app.app_logger.exception(err)
            await self.handle_exception(response, send)

    async def handle_request(self, request: Request, send: Send) -> None:
        session_id = self.app.get_session_id(request)
        response: Response = await self.app.handle_request(request)
        if request.headers.get_cookie("TBSESSIONID") is None:
            response.headers.set_cookie(
                "TBSESSIONID",
                str(session_id),
                path=request.path,
                domain=request.hostname,
            )
        try:
            await asyncio.wait_for(
                self.respond(send, response), timeout=response.timeout
            )
        except asyncio.TimeoutError:
            pass

    async def handle_exception(self, response: Response, send: Send) -> None:
        try:
            await asyncio.wait_for(
                self.respond(send, response), timeout=response.timeout
            )
        except asyncio.TimeoutError:
            pass

    @staticmethod
    async def respond(send: Send, response: Response) -> None:
        await send(
            {
                "type": "http.response.start",
                "status": response.status,
                "headers": response.headers.encode(),
            }
        )
        async for data in response.body:
            await send({"type": "http.response.body", "body": data, "more_body": True})
        await send({"type": "http.response.body", "body": b"", "more_body": False})


class WebSocketHandler(Handler):
    def __init__(self, app: "App", scope: Scope):
        super().__init__(app, scope)

    async def __call__(self, recieve: Receive, send: Send) -> None:
        request = Request(self.scope, recieve)
        request.method = "WEBSOCKET"
        websocket = WebSocket(self.app, self.scope, recieve, send)
        await self.app.handle_ws_request(websocket, request)


class LifespanHandler(Handler):
    def __init__(self, app: "App", scope: Scope):
        super().__init__(app, scope)

    async def __call__(self, recieve: Receive, send: Send) -> None:
        message = await recieve()
        if message["type"] == "lifespan.startup":
            try:
                self.app.startup()
            except Exception as err:
                await send({"type": "lifespan.startup.failed", "message": str(err)})
            else:
                await send({"type": "lifespan.startup.complete"})
        elif message["type"] == "lifespan.shutdown":
            try:
                self.app.shutdown()
            except Exception as err:
                await send({"type": "lifespan.shutdown.failed", "message": str(err)})
            else:
                await send({"type": "lifespan.shutdown.complete"})
