from typing import Any, AsyncGenerator, Dict, Optional, Tuple, Union
from urllib.parse import ParseResult, ParseResultBytes, parse_qs, urlparse

import user_agents
from user_agents.parsers import UserAgent

from tonberry.header import Header
from tonberry.models import Receive, Scope, StrOrBytes, TreePart
from tonberry.util import format_data


class Request:
    def __init__(self, scope: Scope, recieve: Receive):
        self._recieve = recieve
        self.method = str(scope.get("method"))
        self.type = scope.get("type")
        self.http_version = scope.get("http_version")
        self._uri: Union[ParseResult, ParseResultBytes] = urlparse(scope.get("path"))
        self.raw_uri = scope.get("raw_path")
        self.root_path = scope.get("root_path")
        self.client: Tuple[str, str] = scope.get("client")  # type: ignore
        self._query_string = scope.get("query_string")
        self._body: Optional[bytes] = None
        self.headers = Header(scope.get("headers"))
        self.current_route: Optional[TreePart] = None
        self._unsearched_path: str = ""
        self._user_agent: str = ""
        self._scope = scope

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
    def path(self) -> str:
        if isinstance(self._uri.path, bytes):
            return self._uri.path.decode("utf-8")
        else:
            return self._uri.path

    @property
    def scheme(self) -> StrOrBytes:
        return self._uri.scheme

    @property
    def netloc(self) -> StrOrBytes:
        return self._uri.netloc

    @property
    def params(self) -> StrOrBytes:
        return self._uri.params

    @property
    def query_string(self) -> Dict:
        return format_data(parse_qs(self._query_string))

    @property
    def raw_query_string(self) -> Any:
        return self._query_string

    @property
    def fragment(self) -> StrOrBytes:
        return self._uri.fragment

    @property
    def username(self) -> Optional[StrOrBytes]:
        return self._uri.username

    @property
    def password(self) -> Optional[StrOrBytes]:
        return self._uri.password

    @property
    def hostname(self) -> Optional[StrOrBytes]:
        return self._uri.hostname

    @property
    def port(self) -> Optional[int]:
        return self._uri.port

    @property
    def user_agent(self) -> UserAgent:
        if not self._user_agent:
            self._user_agent = user_agents.parse(
                self.headers["user-agent"] or "unknown"
            )
        return self._user_agent
