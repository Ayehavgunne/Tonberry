import json
from enum import Enum
from typing import TYPE_CHECKING, Any

from cactuar.exceptions import WebSocketDisconnect
from cactuar.header import Header
from cactuar.models import Message, Receive, Scope, Send

if TYPE_CHECKING:
    from cactuar import App

# Borrowed from Starlette


class WebSocketState(Enum):
    CONNECTING = 0
    CONNECTED = 1
    DISCONNECTED = 2


class WebSocket:
    def __init__(self, app: "App", scope: Scope, receive: Receive, send: Send):
        self.app = app
        self._send = send
        self._receive = receive
        self._scope = scope
        self.header = Header(scope.get("headers"))
        self.client_state = WebSocketState.CONNECTING
        self.application_state = WebSocketState.CONNECTING

    async def receive(self) -> Message:
        if self.client_state == WebSocketState.CONNECTING:
            message = await self._receive()
            message_type = message["type"]
            assert message_type == "websocket.connect"
            self.client_state = WebSocketState.CONNECTED
            return message
        elif self.client_state == WebSocketState.CONNECTED:
            message = await self._receive()
            message_type = message["type"]
            assert message_type in {"websocket.receive", "websocket.disconnect"}
            if message_type == "websocket.disconnect":
                self.client_state = WebSocketState.DISCONNECTED
            return message
        else:
            raise RuntimeError(
                'Cannot call "receive" once a disconnect message has been received.'
            )

    async def send(self, message: Message) -> None:
        if self.application_state == WebSocketState.CONNECTING:
            message_type = message["type"]
            assert message_type in {"websocket.accept", "websocket.close"}
            if message_type == "websocket.close":
                self.application_state = WebSocketState.DISCONNECTED
            else:
                self.application_state = WebSocketState.CONNECTED
            await self._send(message)
        elif self.application_state == WebSocketState.CONNECTED:
            message_type = message["type"]
            assert message_type in {"websocket.send", "websocket.close"}
            if message_type == "websocket.close":
                self.application_state = WebSocketState.DISCONNECTED
            await self._send(message)
        else:
            raise RuntimeError('Cannot call "send" once a close message has been sent.')

    async def accept(self, subprotocol: str = None) -> None:
        if self.client_state == WebSocketState.CONNECTING:
            await self.receive()
        await self.send({"type": "websocket.accept", "subprotocol": subprotocol})

    @staticmethod
    def _raise_on_disconnect(message: Message) -> None:
        if message["type"] == "websocket.disconnect":
            raise WebSocketDisconnect(message["code"])

    async def receive_text(self) -> str:
        assert self.application_state == WebSocketState.CONNECTED
        message = await self.receive()
        self._raise_on_disconnect(message)
        return message["text"]

    async def receive_bytes(self) -> bytes:
        assert self.application_state == WebSocketState.CONNECTED
        message = await self.receive()
        self._raise_on_disconnect(message)
        return message["bytes"]

    async def receive_json(self, mode: str = "text") -> Any:
        assert mode in ["text", "binary"]
        assert self.application_state == WebSocketState.CONNECTED
        message = await self.receive()
        self._raise_on_disconnect(message)

        if mode == "text":
            text = message["text"]
        else:
            text = message["bytes"].decode("utf-8")
        return json.loads(text)

    async def send_text(self, data: str) -> None:
        await self.send({"type": "websocket.send", "text": data})

    async def send_bytes(self, data: bytes) -> None:
        await self.send({"type": "websocket.send", "bytes": data})

    async def send_json(self, data: Any, mode: str = "text") -> None:
        assert mode in ["text", "binary"]
        text = json.dumps(data)
        if mode == "text":
            await self.send({"type": "websocket.send", "text": text})
        else:
            await self.send({"type": "websocket.send", "bytes": text.encode("utf-8")})

    async def close(self, code: int = 1000) -> None:
        await self.send({"type": "websocket.close", "code": code})

    @property
    def app_is_connected(self) -> bool:
        return self.application_state == WebSocketState.CONNECTED

    @property
    def app_is_connecting(self) -> bool:
        return self.application_state == WebSocketState.CONNECTING

    @property
    def app_is_closed(self) -> bool:
        return self.application_state == WebSocketState.DISCONNECTED

    @property
    def client_is_connected(self) -> bool:
        return self.client_state == WebSocketState.CONNECTED

    @property
    def client_is_connecting(self) -> bool:
        return self.client_state == WebSocketState.CONNECTING

    @property
    def client_is_closed(self) -> bool:
        return self.client_state == WebSocketState.DISCONNECTED
