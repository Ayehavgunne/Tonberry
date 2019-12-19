from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, List, MutableMapping, Optional, Type, Union


@dataclass
class RouteMapping:
    route: str = ""
    func: Optional[Callable] = None
    module_name: Optional[str] = None
    qual_name: Optional[str] = None
    http_method: Optional[str] = None

    def __bool__(self) -> bool:
        return (
            True
            if self.route
            and self.func
            and self.module_name
            and self.qual_name
            and self.http_method
            else False
        )

    def __hash__(self) -> int:
        return (
            hash(self.route)
            ^ hash(self.http_method)
            ^ hash(self.module_name)
            ^ hash(self.qual_name)
        )


@dataclass
class RouteMappings:
    mappings: List[RouteMapping] = field(default_factory=list)
    http_method: str = "GET"

    def get_map_by_func(self, func_name: str, parent_name: str = None) -> RouteMapping:
        for mapping in self.mappings:
            if mapping.func and mapping.func.__name__ == func_name:
                if parent_name:
                    if mapping.qual_name == parent_name:
                        return mapping
                else:
                    return mapping
        return RouteMapping()

    def get_map_by_route(self, route: str, parent_name: str = None) -> RouteMapping:
        for mapping in self.mappings:
            if mapping.route == route:
                if parent_name:
                    if mapping.qual_name == parent_name:
                        return mapping
                else:
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

    def __init__(self) -> None:
        self.GET = RouteMappings(http_method="GET")
        self.POST = RouteMappings(http_method="POST")
        self.PUT = RouteMappings(http_method="PUT")
        self.DELETE = RouteMappings(http_method="DELETE")
        self.PATCH = RouteMappings(http_method="PATCH")
        self.HEAD = RouteMappings(http_method="HEAD")
        self.OPTIONS = RouteMappings(http_method="OPTIONS")

    def get(self, http_method: str) -> RouteMappings:
        if hasattr(self, http_method):
            return getattr(self, http_method)
        else:
            raise TypeError(f"{http_method} is not a supported HTTP Method")


class Node:
    def __init__(self, route: str, class_instance: Type):
        self.route = route
        self.class_instance = class_instance
        self.parent: Optional[Branch] = None


class Branch(Node):
    def __init__(
        self, route: str, class_instance: Type, children: List["TreePart"] = None
    ):
        super().__init__(route, class_instance)
        self.children = children or []


class Leaf(Node):
    def __init__(self, route: str, class_instance: Type, route_mapping: RouteMapping):
        super().__init__(route, class_instance)
        self.route_mapping = route_mapping

    def get_url(self) -> str:
        url = ""
        if self.parent:
            url = self.route
            parent = self.parent
            while parent is not None:
                url = f"{parent.route}/{url}"
                parent = parent.parent  # type: ignore
        return f"/{url}"


TreePart = Union[Branch, Leaf]

Scope = MutableMapping[str, Any]
Message = MutableMapping[str, Any]

Receive = Callable[[], Awaitable[Message]]
Send = Callable[[Message], Awaitable[None]]
