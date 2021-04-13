from websockets import WebSocketServerProtocol


class MessageBroker:

    async def on_message(self, websocket: WebSocketServerProtocol, message: str):
        pass

    async def authenticate(self, message):
        pass

