from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from cactuar.app import App
    from cactuar.routers import Router


def create_app(router: "Router" = None) -> "App":
    from cactuar.app import App

    app_instance = App()
    if router is not None:
        app_instance.router = router
    return app_instance


def quick_start(root: Type) -> None:
    import asyncio

    from hypercorn.config import Config
    from hypercorn.asyncio import serve

    config = Config()
    config.bind = ["10.0.0.11:8080"]

    quick_app = create_app()
    quick_app.router.root = root()

    asyncio.run(serve(quick_app, config))
