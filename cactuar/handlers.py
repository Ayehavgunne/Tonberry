import asyncio
from typing import TYPE_CHECKING, Dict

from cactuar.exceptions import CactuarException
from cactuar.request import Request
from cactuar.response import Response
from cactuar.types import Send, Receive

if TYPE_CHECKING:
    from cactuar.app import App


class Handler:
    def __init__(self, app: "App", scope: Dict):
        self.app = app
        self.scope = scope
        # self.request = Request(scope)

    async def __call__(self, recieve: Receive, send: Send) -> None:
        pass


class HTTPHandler(Handler):
    def __init__(self, app, scope):
        super().__init__(app, scope)

    async def __call__(self, recieve: Receive, send: Send) -> None:
        request = Request(self.scope, recieve)
        try:
            await self.handle_request(request, send)
        except CactuarException as err:
            await self.app.handle_exception(err)

    async def handle_request(self, request: Request, send: Send):
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
    def __init__(self, app, scope):
        super().__init__(app, scope)

    async def __call__(self, recieve: Receive, send: Send) -> None:
        pass


class LifespanHandler(Handler):
    def __init__(self, app, scope):
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
