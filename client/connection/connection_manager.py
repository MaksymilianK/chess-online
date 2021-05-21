import asyncio
import logging
from queue import Queue
from typing import Callable, Optional

import websockets
from websockets import ConnectionClosedError, ConnectionClosedOK


class ConnectionManager:
    def __init__(self):
        self.messages: Queue[str] = Queue()
        self._notify_message: Optional[Callable[[str], None]] = None
        self._loop = asyncio.new_event_loop()
        self._websocket = None

    def start(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def set_notify_message(self, notify_message: Callable):
        self._notify_message = notify_message

    def connect(self, message: str):
        logging.fatal("trying connect")
        self._loop.call_soon_threadsafe(lambda: asyncio.gather(self._connect(message)))

    async def _connect(self, message: str):
        try:
            async with websockets.connect("ws://localhost:80") as websocket:
                logging.fatal("connected")
                self._websocket = websocket
                await websocket.send(message)

                async for message in websocket:
                    self._notify_message(message)
        except ConnectionClosedError as e:
            if e.code == 4000:
                self._notify_message(e.reason)

        logging.fatal(f"{self._websocket.close_code} {self._websocket.close_reason}")

    def send(self, message: str):
        self._loop.call_soon_threadsafe(lambda: asyncio.gather(self._send(message)))

    async def _send(self, message: str):
        await self._websocket.send(message)
