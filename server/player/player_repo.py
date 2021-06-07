from __future__ import annotations

import logging
from typing import Optional
from motor.core import AgnosticCollection
from server.database import DBConnection
from shared.game.game_type import GameType, GAME_TYPES_BY_NAME


class PlayerModel:
    def __init__(self, nick: str = None, elo: dict[GameType, int] = None, email: str = None, password_hash: str = None):
        self.nick = nick
        self.elo = elo
        self.email = email
        self.password_hash = password_hash

    def as_doc(self) -> dict:
        doc = {}
        if self.nick:
            doc["nick"] = self.nick
        if self.elo:
            doc["elo"]: dict[int, int] = {}
            for game_type, elo in self.elo.items():
                doc["elo"][game_type.value] = elo
        if self.email:
            doc["email"] = self.email
        if self.password_hash:
            doc["password_hash"] = self.password_hash

        return doc

    @staticmethod
    def from_doc(doc: dict) -> PlayerModel:
        model = PlayerModel()
        if "nick" in doc:
            model.nick = doc["nick"]
        if "elo" in doc:
            model.elo = {}
            for game_type, elo in doc["elo"].items():
                model.elo[GAME_TYPES_BY_NAME[game_type]] = elo
        if "email" in doc:
            model.email = doc["email"]
        if "password_hash" in doc:
            model.password_hash = doc["password_hash"]

        return model


class PlayerRepository:
    def __init__(self, conn: DBConnection):
        self._collection: AgnosticCollection = conn.db["players"]

        self._collection.create_index("nick")
        self._collection.create_index("email")

    async def find_one_by_email(self, email: str) -> Optional[PlayerModel]:
        doc = await self._collection.find_one({"email": email})
        if doc is None:
            return None
        else:
            return PlayerModel.from_doc(doc)

    async def exists_with_nick(self, nick: str) -> bool:
        return await self._collection.find_one({"nick": nick}) is not None

    async def exists_with_email(self, email: str) -> bool:
        return await self._collection.find_one({"email": email}) is not None

    async def insert_one(self, model: PlayerModel):
        await self._collection.insert_one(model.as_doc())

    async def update_elo(self, nick: str, new_elo: int, game_type: GameType):
        logging.fatal("update1")
        await self._collection.update_one({"nick": nick}, {"$set": {f"elo.{game_type.value}": new_elo}})
        logging.fatal("update2")
