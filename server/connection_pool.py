import asyncio
import logging
import time
from collections import OrderedDict

from websockets import WebSocketServerProtocol

from server.request import InvalidRequestException
from server.message_broker import MessageBroker
from server.player.player import Player


class ConnectionPool:
    def __init__(self, message_broker: MessageBroker):
        self._anonymous: OrderedDict[WebSocketServerProtocol, int] = OrderedDict()
        self._authenticated: dict[WebSocketServerProtocol, Player] = {}
        self._message_broker = message_broker

    async def handle_connection(self, websocket: WebSocketServerProtocol, _: str = None):
        self._anonymous[websocket] = int(time.time())
        try:
            async for message in websocket:
                await self.on_message(message, websocket)
        finally:
            if websocket in self._anonymous:
                self._anonymous.pop(websocket)
            else:
                await self._message_broker.on_connection_closed(self._authenticated[websocket])
                self._authenticated.pop(websocket)

    async def monitor_unauthenticated(self):
        while True:
            now = int(time.time())
            to_del = []

            # It would be dangerous to close connections in this loop, because it would require to await closing
            # and dictionary could change in the meantime
            for client, conn_time in self._anonymous.items():
                if now - conn_time > 10:
                    to_del.append(client)
                else:
                    break

            for client in to_del:
                await client.close(reason="login time exceeded")

            await asyncio.sleep(2)

    async def on_message(self, message: str, websocket: WebSocketServerProtocol):
        logging.fatal(message)
        try:
            if websocket in self._anonymous:
                player = await self._message_broker.on_anonymous_message(message, websocket)
                if player:
                    self._anonymous.pop(websocket)
                    self._authenticated[websocket] = player
            else:
                await self._message_broker.on_authenticated_message(message, self._authenticated[websocket])
        except InvalidRequestException as e:
            logging.fatal(e)
            await websocket.close(reason="invalid request")

