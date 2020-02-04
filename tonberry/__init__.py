from typing import TYPE_CHECKING, Type

from tonberry.context_var_manager import ContextVarManager
from tonberry.contexted.request import Request
from tonberry.contexted.response import Response
from tonberry.contexted.session import Session
from tonberry.expose import _Expose
from tonberry.util import File
from tonberry.websocket import WebSocket

if TYPE_CHECKING:
    from tonberry.app import App
    from tonberry.routers import Router

expose = _Expose

# noinspection PyTypeChecker
request: Request = ContextVarManager("request")  # type: ignore
# noinspection PyTypeChecker
response: Response = ContextVarManager("response")  # type: ignore
# noinspection PyTypeChecker
session: Session = ContextVarManager("session")  # type: ignore
# noinspection PyTypeChecker
websocket: WebSocket = ContextVarManager("websocket")  # type: ignore


def create_app(root: Type = None) -> "App":
    from tonberry.app import App

    app_instance = App()
    if root is not None:
        app_instance.routers[0].root = root()  # type: ignore
    return app_instance


def quick_start(root: Type, host: str = "localhost", port: int = 8080) -> None:
    import uvicorn

    quick_app = create_app()
    # noinspection PyTypeHints
    quick_app.routers[0].root = root()  # type: ignore

    uvicorn.run(quick_app, host=host, port=port, log_level="info", access_log=False)
