import json
from dataclasses import is_dataclass
from inspect import isclass, signature, Parameter, iscoroutinefunction
from typing import TYPE_CHECKING, Callable, Union, Dict

import dacite

from cactuar.exceptions import HTTPError
from cactuar.expose import Expose
from cactuar.request import Request
from cactuar.response import Response
from cactuar.util import format_data, DataClassEncoder

if TYPE_CHECKING:
    from cactuar.app import App


class Router:
    def __init__(self, app: "App"):
        self.app = app
        self.root = None

    async def handle_request(self, request: Request) -> Response:
        pass


class Register(type):
    def __new__(mcs, name, bases, dct):
        cls = super().__new__(mcs, name, bases, dct)
        # if not issubclass(cls, MethodRouter):
        #     raise TypeError("Can only be used for MethodRouter class")
        cls.method_registration = Expose._registrar
        Expose.new_registrar()

        subroutes = {
            key: value
            for key, value in cls.__dict__.items()
            if not key.startswith("_") and key.islower() and isclass(value)
        }
        cls.route_children = subroutes

        for value in cls.route_children.values():
            if not hasattr(value, "route_parents"):
                value.route_parents = {}
            value.route_parents[cls.get_route()] = cls

        return cls


class MethodRouter(Router, metaclass=Register):
    DEFAULT_ROUTE = "index"

    def __init__(self, app):
        super().__init__(app)

    async def handle_request(self, request: Request) -> Response:
        response = Response()
        response.body = bytes(await self._dispatch(request), "utf-8")
        return response

    async def _dispatch(self, request: Request) -> Union[str, bytes, Dict]:
        args = []
        kwargs = {}
        routing_key = None
        http_method = request.method

        # if request.arguments:
        #     kwargs = format_data(request.arguments)
        if request.body:
            if "json" in request.headers["Content-Type"]:
                kwargs.update(json.loads(request.body))
            # elif "xml" in request.headers["Content-Type"]:
            #     if "routing_key" in self.form_fields:
            #         routing_key = self.form_fields["routing_key"]
            #         del self.form_fields["routing_key"]
        # kwargs.update(self.form_fields)
        if request.query_string:
            kwargs.update(format_data(request.query_string))

        method = None
        methods = self.method_registration.get(http_method)
        route_names = [method_name.route for method_name in methods.mappings]

        if routing_key:
            request.uri = f"/{routing_key}"
        uri = request.uri

        paths = [pth for pth in uri.split("?")[0].split("/") if pth != ""]
        for path in paths:
            if path == self.get_route():
                continue
            if path in self.route_children:
                request.uri = f'/{uri.split("/", 2)[2]}'
                return await self._dispatch(request)

            if method is None:
                if path in route_names:
                    method = methods.get_map_by_route(path).method
                    continue
            else:
                args.append(path)

        # if not route_names:
        #     return await self.route_request(routing_key)

        if method is None:
            method = methods.get_map_by_route(self.DEFAULT_ROUTE).method
            args = paths[1:]

        # noinspection PyTypeChecker
        args.insert(0, self)
        arg_types = {"positional": args, "keyword": {}}

        params = signature(method).parameters
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
                    Parameter.POSITIONAL_ONLY,
                    Parameter.POSITIONAL_OR_KEYWORD,
                    Parameter.VAR_POSITIONAL,
                ):
                    arg_types["positional"].append(kwargs.pop(name))
                else:
                    arg_types["keyword"][name] = kwargs.pop(name)
            if param.kind == Parameter.VAR_POSITIONAL:
                var_pos = True
            if param.kind == Parameter.VAR_KEYWORD:
                var_keyword = True

        for key in list(kwargs.keys()):
            if var_pos:
                arg_types["positional"].append(kwargs.pop(key))
            elif var_keyword:
                arg_types["keyword"][key] = kwargs.pop(key)

        if method is not None and not kwargs:
            # noinspection PyUnresolvedReferences
            is_async_callable_class = callable(method) and iscoroutinefunction(
                method.__call__
            )
            is_async_callable_function = iscoroutinefunction(method)
            if is_async_callable_class or is_async_callable_function:
                result = await method(*arg_types["positional"], **arg_types["keyword"])
            else:
                result = method(*arg_types["positional"], **arg_types["keyword"])

            if isinstance(result, (dict, list)) or is_dataclass(result):
                result = json.dumps(result, cls=DataClassEncoder)

            return result

        raise HTTPError(404)

    def get_url(self, request: Request, method: Callable) -> str:
        http_method = request.method
        mapping = self.method_registration.get(http_method).get_map_by_method(
            method.__name__
        )
        reversed_url = mapping.route
        if reversed_url == self.DEFAULT_ROUTE:
            reversed_url = ""
        reversed_url = f"{self.get_route()}/{reversed_url}"
        parent = list(self.route_parents.values())[0]
        while True:
            reversed_url = f"{parent.get_route()}/{reversed_url}"
            if hasattr(parent, "route_parents"):
                parent = list(parent.route_parents.values())[0]
            else:
                break
        return f"/{reversed_url}"

    @classmethod
    def get_route(cls):
        if hasattr(cls, "ROUTE"):
            route = cls.ROUTE
        else:
            route = cls.__name__.replace("Handler", "").lower()
        return route
