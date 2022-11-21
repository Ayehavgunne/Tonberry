class TonberryException(Exception):
    pass


class HTTPRedirectError(TonberryException):
    def __init__(self, route: str, code: int = 307):
        self.route = route
        self.code = code


class HTTPError(TonberryException):
    pass


class RouteNotFoundError(TonberryException):
    pass


class FigureItOutLaterException(TonberryException):
    pass


class WebSocketError(TonberryException):
    pass


class WebSocketDisconnect(TonberryException):
    pass


class WebSocketDisconnectError(TonberryException):
    pass
