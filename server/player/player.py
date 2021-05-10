from websockets import WebSocketServerProtocol

from shared.game_type import GameType


DEFAULT_ELO = 1000


class Player:
    def __init__(self, nick: str, elo: dict[GameType, int], connection: WebSocketServerProtocol):
        self.nick = nick
        self.elo = elo
        self._connection = connection
        self._response = self._to_response()

    def send(self, message: str):
        self._connection.send(message)

    def as_response(self) -> dict:
        return self._response

    def _to_response(self) -> dict:
        return {
            "nick": self.nick,
            "elo": self.elo
        }
