from logging import INFO, Formatter, Logger, LogRecord, StreamHandler

from cactuar import request, response


class CactuarLogger(Logger):
    def __init__(self, name: str, level: int):
        super().__init__(name, level)

    def info(self, msg: str = "", *args, **kwargs) -> None:  # type: ignore
        super().info(msg, *args, **kwargs)

    def error(self, msg: str = "", *args, **kwargs) -> None:  # type: ignore
        super().error(msg, *args, **kwargs)

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
        record.client_ip: str = request.client[0]  # type: ignore
        record.client_port: str = request.client[1]  # type: ignore
        record.path: str = request.path  # type: ignore
        record.http_method: str = request.method  # type: ignore
        record.http_version: str = request.http_version  # type: ignore
        record.status: int = response.status  # type: ignore
        return record


def create_access_logger() -> CactuarLogger:
    logger = CactuarLogger("ct_access", INFO)
    handler = StreamHandler()
    formatter = Formatter(
        "{asctime} {levelname} {client_ip}:{client_port} {http_method} "
        "HTTP/{http_version} {status} {path} {message}",
        style="{",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def create_app_logger() -> CactuarLogger:
    logger = CactuarLogger("ct_app", INFO)
    handler = StreamHandler()
    formatter = Formatter("{asctime} {levelname} {message}", style="{")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
