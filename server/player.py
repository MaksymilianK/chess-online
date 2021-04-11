from typing import Optional

from motor.core import AgnosticCollection

from server.db import DBConnection


class Player:
    def __init__(self, nick: str, elo: int):
        self.nick = nick
        self.elo = elo


class PlayerRepository:
    def __init__(self, conn: DBConnection):
        self._collection: AgnosticCollection = conn.db["players"]

    def find_one_by_nick(self, nick: str) -> Optional[tuple[Player, str]]:
        doc = self._collection.db.find_one({"nick": nick})
        if doc is None:
            return None

        return (
            _doc_to_player(doc),
            doc["password"]
        )

    def exists_with_email_or_nick(self, email: str, nick: str) -> bool:
        return self._collection.find_one({"email": nick}) is not None

    def insert_one(self, player: Player, password: str):
        self._collection.insert_one(_player_to_doc(player, password))

    def update_elo(self, player: Player):
        pass
    

def _doc_to_player(doc: dict) -> Player:
    return Player(doc["nick"], doc["elo"])


def _player_to_doc(player: Player, password: str = None) -> dict:
    doc = {
        "nick": player.nick,
        "elo": player.elo
    }

    if password is not None:
        doc["password"] = password

    return doc
