import motor.motor_asyncio
import yaml
from motor.core import AgnosticClient, AgnosticDatabase


class DBConfig:
    default = {
        "username": "user",
        "password": "pass",
        "host": "localhost",
        "port": 27017,
        "db": "admin"
    }

    def __init__(self):
        self.username = ""
        self.password = ""
        self.host = ""
        self.port = 0
        self.db = ""

        try:
            self._load()
        except FileNotFoundError:
            self._save_def()

    def _load(self):
        with open("db-config.yaml", "r") as file:
            self._set_cfg(yaml.load(file))

    def _save_def(self):
        with open("db-config.yaml", "w") as file:
            yaml.dump(self.default, file)
            self._set_cfg(self.default)

    def _set_cfg(self, cfg: dict[str, any]):
        self.username = cfg["username"]
        self.password = cfg["password"]
        self.host = cfg["host"]
        self.port = cfg["port"]
        self.def_auth_db = cfg["db"]


class DBConnection:
    def __init__(self, config: DBConfig = None, db_client: AgnosticClient = None):
        self._config = config or DBConfig()
        self._client: AgnosticClient = db_client or self._connect()
        self.db: AgnosticDatabase = self._client[self._config.db]

    def close(self):
        self._client.close()

    def _connect(self) -> AgnosticClient:
        c = self._config
        return motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{c.username}:{c.password}@{c.host}:{c.port}/{c.db}"
        )
