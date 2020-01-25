from pathlib import Path
from typing import Callable, Dict, Generator, List, Union
from uuid import UUID, uuid4

from websockets import ConnectionClosedError, ConnectionClosedOK

from tonberry import request as request_context
from tonberry import response as response_context
from tonberry import session as session_context
from tonberry import websocket as websocket_context
from tonberry.context_var_manager import set_context_var
from tonberry.contexted.request import Request
from tonberry.contexted.response import Response
from tonberry.contexted.session import Session, SessionStore
from tonberry.exceptions import (
    HTTPError,
    RouteNotFoundError,
    WebSocketDisconnect,
    WebSocketError,
)
from tonberry.handlers import HTTPHandler, LifespanHandler, WebSocketHandler
from tonberry.loggers import (
    create_app_logger,
    create_http_access_logger,
    create_websocket_access_logger,
)
from tonberry.models import Receive, Send
from tonberry.routers import DynamicRouter, MethodRouter, Router, StaticRouter
from tonberry.websocket import WebSocket


class App:
    def __init__(self, routers: List[Router] = None):
        self.routers = routers or [MethodRouter(self)]
        self.http_access_logger = create_http_access_logger()
        self.websocket_access_logger = create_websocket_access_logger()
        self.app_logger = create_app_logger()
        self.sessions = SessionStore()
        self.startup_functions: List[Callable] = []
        self.shutdown_functions: List[Callable] = []

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

    @property
    def static_routes(self) -> Generator[StaticRouter, None, None]:
        return (router for router in self.routers if isinstance(router, StaticRouter))

    @property
    def dynamic_routes(self) -> Generator[DynamicRouter, None, None]:
        return (router for router in self.routers if isinstance(router, DynamicRouter))

    def add_router(self, router: Router) -> None:
        self.routers.append(router)

    def add_static_route(self, path_root: Union[str, Path], route: str = "/") -> None:
        self.add_router(StaticRouter(self, path_root, route))

    def on_startup(self, func: Callable) -> None:
        self.startup_functions.append(func)

    def on_shutdown(self, func: Callable) -> None:
        self.shutdown_functions.append(func)

    def startup(self) -> None:
        for func in self.startup_functions:
            func()

    def shutdown(self) -> None:
        for func in self.shutdown_functions:
            func()

    async def handle_request(self, request: Request) -> Response:
        set_context_var(request_context, request)
        response = Response()
        set_context_var(response_context, response)
        for s_router in self.static_routes:
            try:
                response = await s_router.handle_request(request, response)
                break
            except RouteNotFoundError:
                pass
        else:  # no break
            for d_router in self.dynamic_routes:
                try:
                    response = await d_router.handle_request(request, response)
                    break
                except RouteNotFoundError:
                    pass
            else:  # no break
                raise HTTPError(404)
        self.http_access_logger.info()
        return response

    async def handle_ws_request(self, websocket: WebSocket, request: Request) -> None:
        set_context_var(request_context, request)
        set_context_var(websocket_context, websocket)
        for router in self.dynamic_routes:
            try:
                func, args = await router.handle_ws_request(request)
                await websocket.accept()
                self.websocket_access_logger.info("Opened")
                try:
                    await func(*args)
                except (WebSocketDisconnect, ConnectionClosedOK):
                    self.websocket_access_logger.info("Disconnected")
                except ConnectionClosedError:
                    self.websocket_access_logger.error("Disconnected unexpectedly")
                break
            except RouteNotFoundError:
                pass
        else:  # no break
            raise WebSocketError

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
