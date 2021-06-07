from __future__ import annotations
from websockets import WebSocketServerProtocol

from shared.game.game_type import GameType


DEFAULT_ELO = 1000


class Player:
    def __init__(self, nick: str, elo: dict[GameType, int], connection: WebSocketServerProtocol):
        self.nick = nick
        self.elo = elo
        self._connection = connection

    async def send(self, message: str):
        await self._connection.send(message)

    def as_response(self) -> dict:
        return {
            "nick": self.nick,
            "elo": {gt.value: e for gt, e in self.elo.items()}
        }

    def __hash__(self) -> int:
        return hash(self.nick)

    def __eq__(self, other: Player) -> bool:
        return self.nick == other.nick
