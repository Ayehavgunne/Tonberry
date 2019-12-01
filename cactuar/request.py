from typing import Dict, Optional, Union, Any, Tuple, AsyncGenerator
from urllib.parse import urlparse, parse_qs, ParseResult, ParseResultBytes

from cactuar.headers import Header
from cactuar.types import TreePart, Receive, Scope
from cactuar.util import format_data


class Request:
    def __init__(self, scope: Scope, recieve: Receive):
        self._recieve = recieve
        self.method: str = str(scope.get("method"))
        self.type = scope.get("type")
        self._uri: Union[ParseResult, ParseResultBytes] = urlparse(scope.get("path"))
        self.raw_uri = scope.get("raw_path")
        self.root_path = scope.get("root_path")
        self.client: Tuple[str, str] = scope.get("client")  # type: ignore
        self._query_string = scope.get("query_string")
        self._body: Optional[bytes] = None
        self.headers = Header(scope.get("headers"))
        self.current_route: Optional[TreePart] = None
        self._unsearched_path: str = ""

    async def stream(self) -> AsyncGenerator[bytes, None]:
        while True:
            chunk = await self._recieve()
            if chunk["type"] == "http.request":
                body = chunk.get("body", b"")
                if body:
                    yield body
                if not chunk.get("more_body", False):
                    break
        yield b""

    async def get_body(self) -> bytes:
        if self._body is None:
            chunks = []
            async for chunk in self.stream():
                chunks.append(chunk)
            self._body = b"".join(chunks)
        return self._body

    @property
    def body(self) -> Optional[bytes]:
        return self._body

    @property
    def path(self) -> Union[str, bytes]:
        return self._uri.path

    @property
    def scheme(self) -> Union[str, bytes]:
        return self._uri.scheme

    @property
    def netloc(self) -> Union[str, bytes]:
        return self._uri.netloc

    @property
    def params(self) -> Union[str, bytes]:
        return self._uri.params

    @property
    def query_string(self) -> Dict:
        return format_data(parse_qs(self._query_string))

    @property
    def raw_query_string(self) -> Any:
        return self._query_string

    @property
    def fragment(self) -> Union[str, bytes]:
        return self._uri.fragment

    @property
    def username(self) -> Optional[Union[str, bytes]]:
        return self._uri.username

    @property
    def password(self) -> Optional[Union[str, bytes]]:
        return self._uri.password

    @property
    def hostname(self) -> Optional[Union[str, bytes]]:
        return self._uri.hostname

    @property
    def port(self) -> Optional[int]:
        return self._uri.port
