from typing import List, Tuple, Dict

# TODO: Account for user added headers
# TODO: Create subclasses of Header for responses
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
        self.__header_attrs: Dict[str, str] = {}
        self.decode()

    def __contains__(self, item):
        if item in self.__header_attrs:
            return True
        return False

    def __getitem__(self, item):
        return self.__header_attrs[item]

    def __setitem__(self, key, value):
        self.__header_attrs[key] = value

    def encode(self) -> List[Tuple[bytes, bytes]]:
        raw_header = []
        for header_key, attr in HEADER_MAP.items():
            value = self.__header_attrs.get(attr, "")
            key = bytes(header_key, "utf-8")
            if value is None:
                value = b""
            else:
                value = bytes(value, "utf-8")
            raw_header.append((key, value))
        return raw_header

    def decode(self):
        for key, value in self._header:
            self.__header_attrs[key.decode("utf-8")] = value.decode("utf-8")
