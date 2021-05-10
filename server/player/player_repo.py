from __future__ import annotations
from typing import Optional
from motor.core import AgnosticCollection
from server.database import DBConnection
from shared.game_type import GameType


class PlayerModel:
    def __init__(self, nick: str = None, elo: dict[GameType, int] = None, email: str = None, password_hash: str = None):
        self.nick = nick
        self.elo = elo
        self.email = email
        self.password_hash = password_hash


class PlayerRepository:
    def __init__(self, conn: DBConnection):
        self._collection: AgnosticCollection = conn.db["players"]

    async def find_one_by_email(self, email: str) -> Optional[PlayerModel]:
        doc = await self._collection.find_one({"email": email})
        if doc is None:
            return None
        else:
            return _doc_to_model(doc)

    async def exists_with_nick(self, nick: str) -> bool:
        return await self._collection.find_one({"nick": nick}) is not None

    async def exists_with_email(self, email: str) -> bool:
        return await self._collection.find_one({"email": email}) is not None

    async def insert_one(self, model: PlayerModel):
        await self._collection.insert_one(_model_to_doc(model))

    async def update_elo(self, model: PlayerModel):
        pass


def _doc_to_model(doc: dict) -> PlayerModel:
    model = PlayerModel()
    if "nick" in doc:
        model.nick = doc["nick"]
    if "elo" in doc:
        model.elo = doc["elo"]
    if "email" in doc:
        model.email = doc["email"]
    if "password_hash" in doc:
        model.password_hash = doc["password_hash"]

    return model


def _model_to_doc(model: PlayerModel) -> dict[str, any]:
    doc = {}
    if model.nick:
        doc["nick"] = model.nick
    if model.elo:
        doc["elo"] = model.elo
    if model.email:
        doc["email"] = model.email
    if model.password_hash:
        doc["password_hash"] = model.password_hash

    return doc
