from cactuar.headers import Header

# TODO: Create a Body class to allow streaming


class Response:
    def __init__(self, headers: Header = None):
        self.body: bytes = b""
        self.headers: Header = headers or Header()
        self.status: int = 200
        self.content_type: str = "text/html"
        self.timeout = 60
