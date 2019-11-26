from typing import Dict, Callable

from cactuar.handlers import HTTPHandler, WebSocketHandler, LifespanHandler
from cactuar.request import Request
from cactuar.response import Response
from cactuar.routers import Router, MethodRouter


class App:
    def __init__(self, router: Router = None):
        self.router = router or MethodRouter(self)

    async def __call__(self, scope: Dict, recieve: Callable, send: Callable) -> None:
        if scope["type"] == "http":
            handler = HTTPHandler(self, scope)
        elif scope["type"] == "websocket":
            handler = WebSocketHandler(self, scope)
        elif scope["type"] == "lifespan":
            handler = LifespanHandler(self, scope)
        else:
            raise RuntimeError(
                f"{scope['type']} is either not a standard ASGI scope type or is not "
                f"yet implimented"
            )
        await handler(recieve, send)

    def startup(self):
        pass

    def shutdown(self):
        pass

    async def handle_request(self, request: Request) -> Response:
        return await self.router.handle_request(request)
