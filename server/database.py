import logging

import motor.motor_asyncio
import yaml
from motor.core import AgnosticClient, AgnosticDatabase


DB_CONFIG_FILE = "db-config.yaml"


class DBConfig:
    default = {
        "username": "user",
        "password": "pass",
        "host": "localhost",
        "port": 27017,
        "database": "admin"
    }

    def __init__(self):
        self.username = ""
        self.password = ""
        self.host = ""
        self.port = 0
        self.database = ""

        try:
            self._load()
        except FileNotFoundError:
            self._save_def()

    def _load(self):
        with open(DB_CONFIG_FILE, "r") as file:
            self._set_cfg(yaml.load(file))
        logging.info("Loading database configuration file")

    def _save_def(self):
        with open(DB_CONFIG_FILE, "w") as file:
            yaml.dump(self.default, file)
            self._set_cfg(self.default)
        logging.info("Writing database default configuration file")

    def _set_cfg(self, cfg: dict[str, any]):
        self.username = cfg["username"]
        self.password = cfg["password"]
        self.host = cfg["host"]
        self.port = cfg["port"]
        self.database = cfg["database"]


class DBConnection:
    def __init__(self, config: DBConfig, db_client: AgnosticClient = None):
        self._config = config
        self._client: AgnosticClient = db_client or self._connect()
        self.db: AgnosticDatabase = self._client[self._config.database]

    def close(self):
        self._client.close()

    def _connect(self) -> AgnosticClient:
        c = self._config
        return motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{c.username}:{c.password}@{c.host}:{c.port}/{c.database}"
        )
