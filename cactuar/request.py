from typing import Dict, Optional, Callable
from urllib.parse import urlparse, parse_qs, ParseResult

from cactuar.headers import Header
from cactuar.route_tree import Node
from cactuar.util import format_data


class Request:
    def __init__(self, scope: Dict, recieve: Callable):
        self._recieve = recieve
        self.method = scope.get("method")
        self.type = scope.get("type")
        self._uri: ParseResult = urlparse(scope.get("path"))
        self.raw_uri = scope.get("raw_path")
        self.root_path = scope.get("root_path")
        self._query_string = scope.get("query_string")
        self._body: Optional[bytes] = None
        self.headers = Header(scope.get("headers"))
        self.current_route: Optional[Node] = None
        self._unsearched_path: str = ""

    async def stream(self):
        while True:
            chunk = await self._recieve()
            if chunk["type"] == "http.request":
                body = chunk.get("body", b"")
                if body:
                    yield body
                if not chunk.get("more_body", False):
                    break
        yield b""

    async def get_body(self):
        if self._body is None:
            chunks = []
            async for chunk in self.stream():
                chunks.append(chunk)
            self._body = b"".join(chunks)
        return self._body

    @property
    def body(self):
        return self._body

    @property
    def path(self):
        return self._uri.path

    @property
    def scheme(self):
        return self._uri.scheme

    @property
    def netloc(self):
        return self._uri.netloc

    @property
    def params(self):
        return self._uri.params

    @property
    def query_string(self):
        return format_data(parse_qs(self._query_string))

    @property
    def raw_query_string(self):
        return self._query_string

    @property
    def fragment(self):
        return self._uri.fragment

    @property
    def username(self):
        return self._uri.username

    @property
    def password(self):
        return self._uri.password

    @property
    def hostname(self):
        return self._uri.hostname

    @property
    def port(self):
        return self._uri.port

    def _update_uri(self, component: str, replacement: str):
        self._uri = self._uri._replace(component, replacement)
