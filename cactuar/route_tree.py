from typing import List

from cactuar.models import RouteMapping


class Node:
    def __init__(self, route: str):
        self.route = route


class Branch(Node):
    def __init__(self, route: str, children: List[Node] = None):
        super().__init__(route)
        self.children = children or []


class Leaf(Node):
    def __init__(self, route: str, route_mapping: RouteMapping):
        super().__init__(route)
        self.route_mapping = route_mapping
