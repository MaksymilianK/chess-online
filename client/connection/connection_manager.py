import asyncio
import logging
from queue import Queue
from typing import Callable, Optional

import websockets
import yaml
from websockets import ConnectionClosedError, ConnectionClosedOK


CONNECTION_CONFIG_FILE = "client-config.yaml"


class ConnectionConfig:
    default = {
        "host": "localhost",
        "port": 80
    }

    def __init__(self):
        self.host = ""
        self.port = 0

        try:
            self._load()
        except FileNotFoundError:
            self._save_def()

    def _load(self):
        with open(CONNECTION_CONFIG_FILE, "r") as file:
            self._set_cfg(yaml.load(file))
        logging.info("Loading database configuration file")

    def _save_def(self):
        with open(CONNECTION_CONFIG_FILE, "w") as file:
            yaml.dump(self.default, file)
            self._set_cfg(self.default)
        logging.info("Writing database default configuration file")

    def _set_cfg(self, cfg: dict[str, any]):
        self.host = cfg["host"]
        self.port = cfg["port"]


class ConnectionManager:
    def __init__(self, config: ConnectionConfig):
        self.messages: Queue[str] = Queue()
        self._notify_message: Optional[Callable[[str], None]] = None
        self._loop = asyncio.new_event_loop()
        self._websocket = None
        self._config = config

    def start(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def set_notify_message(self, notify_message: Callable):
        self._notify_message = notify_message

    def connect(self, message: str):
        self._loop.call_soon_threadsafe(lambda: asyncio.gather(self._connect(message)))

    async def _connect(self, message: str):
        c = self._config
        try:
            async with websockets.connect(f"ws://{c.host}:{c.port}") as websocket:
                self._websocket = websocket
                await websocket.send(message)

                async for message in websocket:
                    logging.fatal(message)
                    self._notify_message(message)
        except ConnectionClosedError as e:
            if e.code == 4000:
                self._notify_message(e.reason)

        logging.fatal(f"{self._websocket.close_code} {self._websocket.close_reason}")

    def send(self, message: str):
        self._loop.call_soon_threadsafe(lambda: asyncio.gather(self._send(message)))

    async def _send(self, message: str):
        await self._websocket.send(message)
