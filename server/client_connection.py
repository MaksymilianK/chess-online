import asyncio
import time
from collections import OrderedDict

from websockets import WebSocketServerProtocol

from server.auth import Player
from server.message_broker import MessageBroker
from server.errors import LOGIN_TIME_EXCEEDED


class ConnectionPool:
    def __init__(self, message_broker: MessageBroker):
        self._anonymous: OrderedDict[WebSocketServerProtocol, int] = OrderedDict()
        self._authenticated: dict[WebSocketServerProtocol, Player] = {}
        self._message_broker = message_broker

    async def handle_connection(self, websocket: WebSocketServerProtocol, path: str = None):
        self._anonymous[websocket] = int(time.time())
        try:
            async for message in websocket:
                await self.on_message(message, websocket)
        finally:
            if websocket in self._anonymous:
                self._anonymous.pop(websocket)
            elif websocket in self._authenticated:
                self._authenticated.pop(websocket)

    async def monitor_unauthenticated(self):
        while True:
            now = int(time.time())
            to_del = []

            # Cannot delete entries from a dictionary while iterating over it, therefore two loops are necessary
            for client, conn_time in self._anonymous.items():
                if now - conn_time > 10:
                    to_del.append(client)
                else:
                    break

            for client in to_del:
                self._anonymous.pop(client)
                await client.close(code=LOGIN_TIME_EXCEEDED, reason="Login time exceeded")

            await asyncio.sleep(2)

    async def on_message(self, message: str, websocket: WebSocketServerProtocol):
        if websocket in self._anonymous:
            player = await self._message_broker.on_anonymous_message(message, websocket)
            if player:
                self._anonymous.pop(websocket)
                self._authenticated[websocket] = player
        else:
            await self._message_broker.on_authenticated_message(message, websocket)
