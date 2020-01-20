from typing import Dict
from uuid import UUID, uuid4

from cactuar import response as response_context
from cactuar import session as session_context
from cactuar.contexed.request import Request
from cactuar.contexed.response import Response
from cactuar.contexed.session import Session, SessionStore
from cactuar.context_var_manager import set_context_var
from cactuar.handlers import HTTPHandler, LifespanHandler, WebSocketHandler
from cactuar.loggers import create_access_logger, create_app_logger
from cactuar.models import Receive, Send
from cactuar.routers import MethodRouter, Router


class App:
    def __init__(self, router: Router = None):
        self.router = router or MethodRouter(self)
        self.access_logger = create_access_logger()
        self.app_logger = create_app_logger()
        self.sessions = SessionStore()

    async def __call__(self, scope: Dict, recieve: Receive, send: Send) -> None:
        if scope["type"] == "http":
            handler = HTTPHandler(self, scope)
        elif scope["type"] == "websocket":
            handler = WebSocketHandler(self, scope)  # type: ignore
        elif scope["type"] == "lifespan":
            handler = LifespanHandler(self, scope)  # type: ignore
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
        response = Response()
        set_context_var(response_context, response)
        response = await self.router.handle_request(request, response)
        self.access_logger.info()
        return response

    def get_session_id(self, request: Request) -> UUID:
        sesson_cookie = request.headers.get_cookie("CTSESSIONID")
        if sesson_cookie is not None:
            session_id = UUID(str(sesson_cookie))
            session = self.sessions[session_id]
            set_context_var(session_context, session)
            return session_id
        else:
            return self.create_session()

    def create_session(self) -> UUID:
        new_session_id = uuid4()
        self.sessions[new_session_id] = Session(new_session_id)
        set_context_var(session_context, self.sessions[new_session_id])
        return new_session_id
