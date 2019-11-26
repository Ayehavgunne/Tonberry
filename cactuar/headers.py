from typing import List, Optional, Tuple

# TODO: Account for user added headers
# TODO: Create subclasses of Header for requests and responses separately
# TODO: Organise fields by standard and common non-standard ones
# https://en.wikipedia.org/wiki/List_of_HTTP_header_fields

HEADER_MAP = {
    "Host": "host",
    "Content-Type": "content_type",
}


class Header:
    def __init__(self, header: List = None):
        if header is None:
            header = []
        self._header = header
        self.host: Optional[str] = None
        self.content_type: Optional[str] = None
        self.decode()

    def encode(self) -> List[Tuple[bytes, bytes]]:
        raw_header = []
        for header_key, attr in HEADER_MAP.items():
            value = getattr(self, attr)
            if value is None:
                value = b""
            else:
                value = bytes(value, "utf-8")
            raw_header.append((bytes(header_key, "utf-8"), value))
        return raw_header

    def decode(self):
        for key, value in self._header:
            if key in HEADER_MAP:
                setattr(self, HEADER_MAP[key], value)
