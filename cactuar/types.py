from typing import Any, Awaitable, Callable, List, MutableMapping, Type, Union

from cactuar.models import RouteMapping


class Node:
    def __init__(self, route: str, class_instance: Type):
        self.route = route
        self.class_instance = class_instance


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


TreePart = Union[Branch, Leaf]

Scope = MutableMapping[str, Any]
Message = MutableMapping[str, Any]

Receive = Callable[[], Awaitable[Message]]
Send = Callable[[Message], Awaitable[None]]
