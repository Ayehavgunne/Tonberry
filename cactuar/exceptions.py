class CactuarException(Exception):
    pass


class HTTPError(CactuarException):
    pass


class RouteNotFoundError(CactuarException):
    pass


class FigureItOutLaterException(CactuarException):
    pass
