import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, is_dataclass
from functools import partial
from pathlib import Path
from typing import Any, Dict, Union

from jinja2 import Environment, FileSystemLoader, select_autoescape

from tonberry.models import Alias, StrOrBytes


class DataClassEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Dict[str, Any]:
        if is_dataclass(obj):
            return asdict(obj)
        return json.JSONEncoder.default(self, obj)


def alias(app_route: str) -> Alias:
    return Alias(app_route)


def decode_bytes_to_str(value: StrOrBytes) -> str:
    """
    Will convert any byte strings to UTF-8 strings
    """
    if isinstance(value, bytes):
        value = value.decode("utf-8")
    return value


def format_data(kwargs: Dict) -> Dict:
    """
    De-lists any single-item lists and scrubs the values

    So {b'foo': [b'bar']} would become {'foo': 'bar'}
    """
    new_kwargs = {}
    for key, value in kwargs.items():
        if isinstance(value, list):
            for index, val in enumerate(value):
                value[index] = decode_bytes_to_str(val)
        if len(value) == 1:
            value = decode_bytes_to_str(value[0])
        new_kwargs[decode_bytes_to_str(key)] = value
    return new_kwargs


class File:
    def __init__(self, path: Union[str, Path]) -> None:
        if isinstance(path, str):
            path = Path(path)
        self.path = path
        self.chunk_size = 64

    async def read(self) -> bytes:
        chunks = []
        loop = asyncio.get_event_loop()
        pool = ThreadPoolExecutor()
        open_file = self.path.open("rb")
        read_func = partial(open_file.read, self.chunk_size)
        while True:
            chunk = await loop.run_in_executor(pool, read_func)
            if not chunk:
                break
            chunks.append(chunk)
        return b"".join(chunks)


class Jinja:
    def __init__(
        self, template_path: Path, file_name: str = None, context: dict = None
    ):
        self.template_path = template_path
        self.file_name = file_name or ""
        self.context = context or {}
        self.environment = Environment(
            loader=FileSystemLoader(self.template_path),
            autoescape=select_autoescape(["html", "xml"]),
        )

    def __call__(self, file_name: str, context: dict) -> str:
        return Jinja(self.template_path, file_name, context).render()

    def render(self) -> str:
        template = self.environment.get_template(self.file_name)
        return template.render(**self.context)
