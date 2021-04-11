import asyncio
import time
from collections import OrderedDict

from websockets import WebSocketServerProtocol

from server.message_broker import MessageBroker


class ClientPool:
    def __init__(self, message_broker: MessageBroker = None):
        self.anonymous: OrderedDict[WebSocketServerProtocol, int] = OrderedDict()
        self.authenticated: set[WebSocketServerProtocol] = set()
        self.message_broker = message_broker or MessageBroker()

    async def handle_connection(self, websocket: WebSocketServerProtocol):
        self.anonymous[websocket] = int(time.time())
        try:
            async for message in websocket:
                await self.message_broker.on_message(websocket, message)
        finally:
            if websocket in self.anonymous:
                self.anonymous.pop(websocket)
            else:
                self.authenticated.remove(websocket)

    async def monitor_unauthenticated(self):
        while True:
            now = time.time()
            to_del = []

            # Cannot delete entries from a dictionary while iterating over it, therefore two loops are necessary
            for (client, conn_time) in self.anonymous:
                if now - conn_time < 10:
                    to_del.append(client)
                else:
                    break

            for client in to_del:
                self.anonymous.pop(client)

            await asyncio.sleep(2)

    async def authenticate(self, websocket: WebSocketServerProtocol):
        if websocket in self.anonymous:
            self.anonymous.pop(websocket)
            self.authenticated.add(websocket)
