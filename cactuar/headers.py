from datetime import datetime
from http.cookies import SimpleCookie
from typing import List, Tuple, Dict, Any, Union

# TODO: Account for user added headers
# TODO: Create subclass of Header for responses
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

    def __contains__(self, item: str) -> bool:
        if item in self.__header_attrs:
            return True
        return False

    def __getitem__(self, item: str) -> Any:
        if item in self.__header_attrs:
            return self.__header_attrs[item]

    def __setitem__(self, key: str, value: Union[str, int]) -> None:
        self.__header_attrs[key] = str(value)

    def encode(self) -> List[Tuple[bytes, bytes]]:
        raw_header = []
        for header_key, attr in self.__header_attrs.items():
            key = bytes(header_key, "utf-8")
            if attr is None:
                value = b""
            else:
                value = bytes(attr, "utf-8")
            raw_header.append((key, value))
        return raw_header

    def decode(self) -> None:
        for key, value in self._header:
            self.__header_attrs[key.decode("utf-8")] = value.decode("utf-8")

    def set_cookie(
        self,
        key: str,
        morsel: str,
        path: Union[str, bytes] = None,
        domain: Union[str, bytes] = None,
        secure: bool = False,
        expires: datetime = None,
        max_age: int = None,
        comment: str = None,
        version: str = None,
    ) -> None:
        if "Set-Cookie" not in self:
            self.__header_attrs["Set-Cookie"] = ""
        cookie: SimpleCookie = SimpleCookie()
        cookie[key] = morsel
        if path is not None:
            cookie[key]["path"] = path
        if domain is not None:
            cookie[key]["domain"] = domain
        if secure:
            cookie[key]["secure"] = True
        if expires is not None:
            cookie[key]["expires"] = expires.strftime("%a, %d %b %Y %H:%M:%S")
        if max_age is not None:
            cookie[key]["max-age"] = max_age
        if comment is not None:
            cookie[key]["comment"] = comment
        if version is not None:
            cookie[key]["version"] = version
        cookie_str = str(cookie)
        self.__header_attrs["Set-Cookie"] += cookie_str
