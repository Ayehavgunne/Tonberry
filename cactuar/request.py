from typing import Dict
from urllib.parse import urlparse, parse_qs, ParseResult

from cactuar.headers import Header


class Request:
    def __init__(self, scope: Dict):
        self.method = scope.get("method")
        self.type = scope.get("type")
        self._uri: ParseResult = urlparse(scope.get("path"))
        self.raw_uri = scope.get("raw_path")
        self.root_path = scope.get("root_path")
        self._query_string = scope.get("query_string")
        self.body = scope.get("body")
        self.headers = Header(scope.get("headers"))

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
        return parse_qs(self._uri.query)

    @property
    def raw_query_string(self):
        return self._uri.query

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
