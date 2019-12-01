import asyncio
import traceback
from typing import TYPE_CHECKING

from cactuar.exceptions import HTTPError
from cactuar.request import Request
from cactuar.response import Response
from cactuar.types import Send, Receive, Scope

if TYPE_CHECKING:
    from cactuar.app import App  # pytype: disable=pyi-error


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
        self.app.access_logger.set_request_obj(request)
        try:
            await self.handle_request(request, send)
        except HTTPError as err:
            response = Response()
            response.status = err.args[0]
            response.body = str(err.args[0]).encode("utf-8")
            self.app.access_logger.set_response_obj(response)
            self.app.access_logger.error()
            await self.handle_exception(response, send)
        except Exception as err:
            response = Response()
            response.body = traceback.format_exc().encode("utf-8")
            self.app.app_logger.exception(err)
            await self.handle_exception(response, send)

    async def handle_request(self, request: Request, send: Send) -> None:
        response: Response = await self.app.handle_request(request)
        response.headers.set_cookie(
            "something", "good", path=request.path, domain=request.hostname
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
        await send(
            {"type": "http.response.body", "body": response.body, "more_body": False}
        )


class WebSocketHandler(Handler):
    def __init__(self, app: "App", scope: Scope):
        super().__init__(app, scope)

    async def __call__(self, recieve: Receive, send: Send) -> None:
        pass


class LifespanHandler(Handler):
    def __init__(self, app: "App", scope: Scope):
        super().__init__(app, scope)

    async def __call__(self, recieve: Receive, send: Send) -> None:
        while True:
            event = await recieve()
            if event["type"] == "lifespan.startup":
                try:
                    self.app.startup()
                except Exception as err:
                    await send({"type": "lifespan.startup.failed", "message": str(err)})
                else:
                    await send({"type": "lifespan.startup.complete"})
            elif event["type"] == "lifespan.shutdown":
                try:
                    self.app.shutdown()
                except Exception as err:
                    await send(
                        {"type": "lifespan.shutdown.failed", "message": str(err)}
                    )
                else:
                    await send({"type": "lifespan.shutdown.complete"})
                break
