from cactuar.header import Header

# TODO: Create a Body class to allow streaming


class Response:
    def __init__(self, headers: Header = None):
        self.body: bytes = b""
        self.headers: Header = headers or Header()
        self.status: int = 200
        self._content_type: str = ""
        self.timeout = 60

    @property
    def content_type(self) -> str:
        return self._content_type

    @content_type.setter
    def content_type(self, value: str) -> None:
        self._content_type = value
        self.headers["content-type"] = value
