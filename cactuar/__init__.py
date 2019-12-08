from _contextvars import ContextVar
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from cactuar.app import App
    from cactuar.routers import Router


request = ContextVar("request")
response = ContextVar("response")
session = ContextVar("session")


def create_app(router: "Router" = None) -> "App":
    from cactuar.app import App

    app_instance = App()
    if router is not None:
        app_instance.router = router
    return app_instance


def quick_start(root: Type, host: str = "localhost", port: int = 8080) -> None:
    import uvicorn  # type: ignore

    quick_app = create_app()
    quick_app.router.root = root()

    uvicorn.run(quick_app, host=host, port=port, log_level="info", access_log=False)
