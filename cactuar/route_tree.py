from typing import List, Union, Type

from cactuar.models import RouteMapping


class Node:
    def __init__(self, route: str, class_instance: Type):
        self.route = route
        self.class_instance = class_instance


class Branch(Node):
    def __init__(self, route: str, class_instance: Type, children: List[Node] = None):
        super().__init__(route, class_instance)
        self.children = children or []


class Leaf(Node):
    def __init__(self, route: str, class_instance: Type, route_mapping: RouteMapping):
        super().__init__(route, class_instance)
        self.route_mapping = route_mapping


TreePart = Union[Branch, Leaf]
