import motor.motor_asyncio
from motor.core import AgnosticClient, AgnosticDatabase


class DBConnection:
    def __init__(self, config: dict, db_client: AgnosticClient = None):
        self._config = config
        self._client: AgnosticClient = db_client or self._connect()
        self.db: AgnosticDatabase = self._client[self._config["database"]]

    def close(self):
        self._client.close()

    def _connect(self) -> AgnosticClient:
        c = self._config
        return motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{c['username']}:{c['password']}@{c['host']}:{c['port']}/{c['database']}"
        )
