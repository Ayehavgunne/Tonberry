class CactuarException(Exception):
    pass


class HTTPRedirect(CactuarException):
    def __init__(self, route: str, code: int = 307):
        self.route = route
        self.code = code


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
