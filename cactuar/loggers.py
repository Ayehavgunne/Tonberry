from logging import Logger, StreamHandler, Formatter, INFO, LogRecord
from typing import Optional

from cactuar.request import Request
from cactuar.response import Response


class CactuarLogger(Logger):
    def __init__(self, name: str, level: int):
        super().__init__(name, level)
        self.request: Optional[Request] = None
        self.response: Optional[Response] = None

    def set_request_obj(self, request: Request) -> None:
        self.request = request

    def set_response_obj(self, response: Response) -> None:
        self.response = response

    def info(self, msg: str = "", *args, **kwargs) -> None:  # type: ignore
        super().info(msg, *args, **kwargs)

    # noinspection PyTypeHints
    def makeRecord(  # type: ignore
        self,
        name,
        level,
        fn,
        lno,
        msg,
        args,
        exc_info,
        func=None,
        extra=None,
        sinfo=None,
    ) -> LogRecord:
        record = super().makeRecord(
            name, level, fn, lno, msg, args, exc_info, func, extra, sinfo
        )
        if self.request is not None:
            record.client: str = self.request.client[0]  # type: ignore
            record.path = self.request.path  # type: ignore
        if self.response is not None:  # type: ignore
            record.status = self.response.status  # type: ignore
        return record


def create_access_logger() -> CactuarLogger:
    logger = CactuarLogger("ct_access", INFO)
    handler = StreamHandler()
    formatter = Formatter("{asctime} {client} {status} {path} {message}", style="{")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
