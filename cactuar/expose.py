from typing import Callable

from cactuar.models import Methods, RouteMapping


class Expose:
    _registrar = Methods()

    def __call__(self, func):
        self.get(func)

    @classmethod
    def new_registrar(cls):
        cls._registrar = Methods()

    @classmethod
    def _register(cls, method: Callable, http_method: str, route: str = None) -> None:
        if route is None:
            route = method.__name__
        cls._registrar.get(http_method).mappings.append(RouteMapping(route, method))

    @classmethod
    def get(cls, route: str = None) -> Callable:
        def wrapper(func: Callable):
            cls._register(func, "GET", route)
            return func

        if callable(route):
            method = route
            route = None
            return wrapper(method)
        else:
            return wrapper

    @classmethod
    def post(cls, route: str = None) -> Callable:
        def wrapper(func):
            cls._register(func, "POST", route)
            return func

        if callable(route):
            method = route
            route = None
            return wrapper(method)
        else:
            return wrapper

    @classmethod
    def put(cls, route: str = None) -> Callable:
        def wrapper(func):
            cls._register(func, "PUT", route)
            return func

        if callable(route):
            method = route
            route = None
            return wrapper(method)
        else:
            return wrapper

    @classmethod
    def delete(cls, route: str = None) -> Callable:
        def wrapper(func):
            cls._register(func, "DELETE", route)
            return func

        if callable(route):
            method = route
            route = None
            return wrapper(method)
        else:
            return wrapper

    @classmethod
    def patch(cls, route: str = None) -> Callable:
        def wrapper(func):
            cls._register(func, "PATCH", route)
            return func

        if callable(route):
            method = route
            route = None
            return wrapper(method)
        else:
            return wrapper

    @classmethod
    def head(cls, route: str = None) -> Callable:
        def wrapper(func):
            cls._register(func, "HEAD", route)
            return func

        if callable(route):
            method = route
            route = None
            return wrapper(method)
        else:
            return wrapper

    @classmethod
    def options(cls, route: str = None) -> Callable:
        def wrapper(func):
            cls._register(func, "OPTIONS", route)
            return func

        if callable(route):
            method = route
            route = None
            return wrapper(method)
        else:
            return wrapper
