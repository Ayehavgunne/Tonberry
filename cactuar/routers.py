import json
from dataclasses import is_dataclass
import inspect
from typing import TYPE_CHECKING, Union, Dict, Optional, Type, List

import dacite

from cactuar.exceptions import HTTPError
from cactuar.expose import _Expose
from cactuar.request import Request
from cactuar.response import Response
from cactuar.route_tree import Branch, Leaf
from cactuar.util import DataClassEncoder

if TYPE_CHECKING:
    from cactuar.app import App


class Router:
    def __init__(self, app: "App"):
        self.app = app

    async def handle_request(self, request: Request) -> Response:
        pass


class MethodRouter(Router):
    DEFAULT_ROUTE = "index"

    def __init__(self, app):
        super().__init__(app)
        self._root: Optional[Type] = None
        self._tree: Optional[Branch] = None
        self.method_registration = _Expose._registrar

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, root: Type):
        self._root = root
        self._tree = Branch("", self.build_tree(root))

    async def handle_request(self, request: Request) -> Response:
        response = Response()
        response.body = bytes(await self._dispatch(request), "utf-8")
        return response

    async def _dispatch(self, request: Request) -> Union[str, bytes, Dict]:
        func = self.get_func(request)

        args = []
        kwargs = {}

        if request.body:
            if "json" in request.headers["Content-Type"]:
                kwargs.update(json.loads(request.body))

        if request.query_string:
            kwargs.update(request.query_string)

        # noinspection PyTypeChecker
        args.insert(0, self)
        arg_types = {"positional": args, "keyword": {}}

        params = inspect.signature(func).parameters
        var_pos = False
        var_keyword = False
        for name, param in params.items():
            if (
                kwargs
                and hasattr(param, "annotation")
                and is_dataclass(param.annotation)
            ):
                instance = dacite.from_dict(param.annotation, kwargs)
                for key in list(kwargs.keys()):
                    if hasattr(instance, key):
                        del kwargs[key]
                arg_types["positional"].append(instance)
            if name in kwargs:
                if param.kind in (
                    inspect.Parameter.POSITIONAL_ONLY,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.VAR_POSITIONAL,
                ):
                    arg_types["positional"].append(kwargs.pop(name))
                else:
                    arg_types["keyword"][name] = kwargs.pop(name)
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                var_pos = True
            if param.kind == inspect.Parameter.VAR_KEYWORD:
                var_keyword = True

        for key in list(kwargs.keys()):
            if var_pos:
                arg_types["positional"].append(kwargs.pop(key))
            elif var_keyword:
                arg_types["keyword"][key] = kwargs.pop(key)

        if func is not None and not kwargs:
            # noinspection PyUnresolvedReferences
            is_async_callable_class = callable(func) and inspect.iscoroutinefunction(
                func.__call__
            )
            is_async_callable_function = inspect.iscoroutinefunction(func)
            if is_async_callable_class or is_async_callable_function:
                result = await func(*arg_types["positional"], **arg_types["keyword"])
            else:
                result = func(*arg_types["positional"], **arg_types["keyword"])

            if isinstance(result, (dict, list)) or is_dataclass(result):
                result = json.dumps(result, cls=DataClassEncoder)

            return result

        raise HTTPError(404)

    def get_func(self, request: Request):
        http_method = request.method
        url_path = request.path
        paths = [pth for pth in url_path.split("/") if pth != ""]
        level = 0
        route = self.match_route(paths[level], self._tree.children, http_method)
        while isinstance(route, Branch):
            level += 1
            route = self.match_route(paths[level], route.children, http_method)
        if route:
            return route.route_mapping.func
        else:
            raise HTTPError(404)

    @staticmethod
    def match_route(
        current_path: str, routes: List[Union[Branch, Leaf]], http_method: str
    ) -> Union[Branch, Leaf]:
        for route in routes:
            if route.route == current_path:
                if isinstance(route, Leaf):
                    if route.route_mapping.http_method == http_method:
                        return route
                elif isinstance(route, Branch):
                    return route

    def build_tree(self, cls):
        children = []

        for key, value in cls.__class__.__dict__.items():
            if not key.startswith("_"):
                if (
                    key.islower()
                    and hasattr(value, "__class__")
                    and inspect.isclass(value.__class__)
                    and not inspect.ismethod(value)
                    and not inspect.isfunction(value)
                ):
                    children.append(Branch(key, self.build_tree(value)))
                elif inspect.ismethod(value) or inspect.isfunction(value):
                    mappings = [
                        self.method_registration.GET.get_map_by_func(
                            value.__name__, cls.__class__.__name__
                        ),
                        self.method_registration.POST.get_map_by_func(
                            value.__name__, cls.__class__.__name__
                        ),
                        self.method_registration.PUT.get_map_by_func(
                            value.__name__, cls.__class__.__name__
                        ),
                        self.method_registration.PATCH.get_map_by_func(
                            value.__name__, cls.__class__.__name__
                        ),
                        self.method_registration.DELETE.get_map_by_func(
                            value.__name__, cls.__class__.__name__
                        ),
                        self.method_registration.HEAD.get_map_by_func(
                            value.__name__, cls.__class__.__name__
                        ),
                        self.method_registration.OPTIONS.get_map_by_func(
                            value.__name__, cls.__class__.__name__
                        ),
                    ]
                    mappings = [mapp for mapp in mappings if mapp]
                    for mapp in mappings:
                        children.append(Leaf(mapp.route, mapp))

        return children

    # def get_url(self, request: Request, func: Callable) -> str:
    #     http_method = request.method
    #     mapping = self.method_registration.get(http_method).get_map_by_func(
    #         func.__name__
    #     )
    #     reversed_url = mapping.route
    #     if reversed_url == self.DEFAULT_ROUTE:
    #         reversed_url = ""
    #     reversed_url = f"{self.get_route()}/{reversed_url}"
    #     parent = list(self.route_parents.values())[0]
    #     while True:
    #         reversed_url = f"{parent.get_route()}/{reversed_url}"
    #         if hasattr(parent, "route_parents"):
    #             parent = list(parent.route_parents.values())[0]
    #         else:
    #             break
    #     return f"/{reversed_url}"
    #
    # @classmethod
    # def get_route(cls):
    #     if hasattr(cls, "ROUTE"):
    #         route = cls.ROUTE
    #     else:
    #         route = cls.__name__.replace("Handler", "").lower()
    #     return route
