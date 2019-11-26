from dataclasses import dataclass, field
from typing import Callable, List


@dataclass
class RouteMapping:
    route: str = ""
    method: Callable = None


@dataclass
class RouteMappings:
    mappings: List[RouteMapping] = field(default_factory=list)

    def get_map_by_method(self, method_name: str) -> RouteMapping:
        for mapping in self.mappings:
            if mapping.method.__name__ == method_name:
                return mapping
        return RouteMapping()

    def get_map_by_route(self, route: str) -> RouteMapping:
        for mapping in self.mappings:
            if mapping.route == route:
                return mapping
        return RouteMapping()


@dataclass
class Methods:
    GET: RouteMappings
    POST: RouteMappings
    PUT: RouteMappings
    DELETE: RouteMappings
    PATCH: RouteMappings
    HEAD: RouteMappings
    OPTIONS: RouteMappings

    def __init__(self):
        self.GET = RouteMappings()
        self.POST = RouteMappings()
        self.PUT = RouteMappings()
        self.DELETE = RouteMappings()
        self.PATCH = RouteMappings()
        self.HEAD = RouteMappings()
        self.OPTIONS = RouteMappings()

    def get(self, http_method: str):
        if hasattr(self, http_method):
            return getattr(self, http_method)
        else:
            raise TypeError(f"{http_method} is not a supported HTTP Method")
