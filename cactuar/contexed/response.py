from cactuar.header import Header


class Body:
    chunk_size = 1024

    def __init__(self, data: bytes):
        self.data = data
        self._position = 0

    def __aiter__(self) -> "Body":
        return self

    async def __anext__(self) -> bytes:
        data = self.data[self._position : self._position + self.chunk_size]
        if not data:
            self._position = 0
            raise StopAsyncIteration
        self._position += self.chunk_size
        return data


class Response:
    def __init__(self, headers: Header = None):
        self._body = Body(b"")
        self.headers: Header = headers or Header()
        self.status: int = 200
        self._content_type: str = ""
        self.timeout = 60

    @property
    def body(self) -> Body:
        return self._body

    @body.setter
    def body(self, data: bytes) -> None:
        self._body.data = data

    @property
    def content_type(self) -> str:
        return self._content_type

    @content_type.setter
    def content_type(self, value: str) -> None:
        self._content_type = value
        self.headers["content-type"] = value
