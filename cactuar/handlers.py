import asyncio
from typing import Callable, TYPE_CHECKING, Dict

from cactuar.request import Request
from cactuar.response import Response

if TYPE_CHECKING:
    from cactuar.app import App


class Handler:
    def __init__(self, app: "App", scope: Dict):
        self.app = app
        self.scope = scope
        self.request = Request(scope)

    async def __call__(self, recieve: Callable, send: Callable) -> None:
        pass


class HTTPHandler(Handler):
    def __init__(self, app, scope):
        super().__init__(app, scope)

    async def __call__(self, recieve: Callable, send: Callable) -> None:
        request = Request(self.scope)
        await self.handle_request(request, send)

    async def handle_request(self, request: Request, send: Callable):
        response: Response = await self.app.handle_request(request)
        try:
            await asyncio.wait_for(
                self.respond(send, response), timeout=response.timeout
            )
        except asyncio.TimeoutError:
            pass

    @staticmethod
    async def respond(send: Callable, response: Response) -> None:
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

    async def __call__(self, recieve: Callable, send: Callable) -> None:
        pass


class LifespanHandler(Handler):
    def __init__(self, app, scope):
        super().__init__(app, scope)

    async def __call__(self, recieve: Callable, send: Callable) -> None:
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
