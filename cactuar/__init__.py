from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from cactuar.routers import Router


def create_app(router: "Router" = None):
    from cactuar.app import App

    app = App()
    if router is not None:
        app.router = router
    return app


def quick_start(root: Type):
    import asyncio

    from hypercorn.config import Config
    from hypercorn.asyncio import serve

    config = Config()
    config.bind = ["localhost:8080"]

    app = create_app()
    app.router.root = root()

    asyncio.run(serve(app, config))
