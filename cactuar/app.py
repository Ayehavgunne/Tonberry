from typing import Dict
from uuid import UUID

from cactuar.handlers import HTTPHandler, WebSocketHandler, LifespanHandler, Handler
from cactuar.loggers import create_access_logger, create_app_logger
from cactuar.contexed.request import Request
from cactuar.contexed.response import Response
from cactuar.routers import Router, MethodRouter
from cactuar.contexed.session import SessionStore, Session
from cactuar.types import Receive, Send


class App:
    def __init__(self, router: Router = None):
        self.router = router or MethodRouter(self)
        self.access_logger = create_access_logger()
        self.app_logger = create_app_logger()
        self.sessions = SessionStore()

    async def __call__(self, scope: Dict, recieve: Receive, send: Send) -> None:
        # noinspection PyUnusedLocal
        handler: Handler
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

    def startup(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    async def handle_request(self, request: Request) -> Response:
        response = await self.router.handle_request(request)
        self.access_logger.set_request_obj(request)
        self.access_logger.set_response_obj(response)
        self.access_logger.info()
        return response

    def store_session_id(self, session_id: UUID) -> None:
        if session_id not in self.sessions:
            self.sessions[session_id] = Session(session_id)
