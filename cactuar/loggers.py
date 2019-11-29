from logging import Logger, getLogger, StreamHandler, Formatter, INFO


def create_access_logger() -> Logger:
    logger = getLogger("ct_access")
    logger.setLevel(INFO)
    handler = StreamHandler()
    formatter = Formatter("{asctime} {message}", style="{")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
