# import asyncio
from typing import Dict, Callable

# from hypercorn.config import Config
# from hypercorn.asyncio import serve

from cactuar.handlers import HTTPHandler, WebSocketHandler, LifespanHandler
from cactuar.request import Request
from cactuar.response import Response
from cactuar.routers import Router, MethodRouter

# config = Config()
# config.bind = ["localhost:8080"]


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


# if __name__ == "__main__":
#     asyncio.run(serve(App(), config))
