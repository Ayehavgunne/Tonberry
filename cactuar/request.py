from typing import Dict, Optional

from cactuar.headers import Header


class Request:
    def __init__(self, scope: Dict):
        self.method = scope.get("method")
        self.type = scope.get("type")
        self.path = scope.get("path")
        self.raw_path = scope.get("raw_path")
        self.root_path = scope.get("root_path")
        self.query_string = scope.get("query_string")
        self.body = scope.get("body")
        self.headers = Header(scope.get("headers"))
        self._uri: Optional[str] = None

    @property
    def uri(self):
        if self._uri is None:
            self._uri = self.path.replace("http://localhost:8080", "")
        return self._uri

    @uri.setter
    def uri(self, uri_str: str):
        self._uri = uri_str
