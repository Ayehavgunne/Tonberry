class CactuarException(Exception):
    pass


class HTTPError(CactuarException):
    pass


class RouteNotFoundError(CactuarException):
    pass


class FigureItOutLaterException(CactuarException):
    pass


class WebSocketError(CactuarException):
    pass


class WebSocketDisconnect(CactuarException):
    pass
