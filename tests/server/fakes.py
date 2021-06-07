from typing import Optional

from websockets import WebSocketServerProtocol

from server.player.player import Player
from server.player.player_repo import PlayerModel
from shared.game.game_type import GameType


class FakePlayerRepository:
    def __init__(self):
        self.players = [
            PlayerModel(
                "player1",
                {GameType.BLITZ: 1000, GameType.RAPID: 1000, GameType.CLASSIC: 1000},
                "email1@test.test",
                ""
            ),
            PlayerModel(
                "player2",
                {GameType.BLITZ: 1213, GameType.RAPID: 1240, GameType.CLASSIC: 994},
                "email2@test.test",
                ""
            ),
            PlayerModel(
                "player3",
                {GameType.BLITZ: 1200, GameType.RAPID: 1500, GameType.CLASSIC: 1010},
                "email3@test.test",
                ""
            ),
            PlayerModel(
                "player4",
                {GameType.BLITZ: 1100, GameType.RAPID: 1051, GameType.CLASSIC: 1205},
                "email4@test.test",
                ""
            ),
            PlayerModel(
                "player5",
                {GameType.BLITZ: 948, GameType.RAPID: 1060, GameType.CLASSIC: 1400},
                "email5@test.test",
                ""
            ),
        ]

    async def find_one_by_email(self, email: str) -> Optional[PlayerModel]:
        for p in self.players:
            if p.email == email:
                return p

        return None

    async def exists_with_nick(self, nick: str) -> bool:
        for p in self.players:
            if p.nick == nick:
                return True

        return False

    async def exists_with_email(self, email: str) -> bool:
        return self.find_one_by_email(email) is not None

    async def insert_one(self, model: PlayerModel):
        self.players.append(model)

    async def update_elo(self, nick: str, new_elo: int, game_type: GameType):
        for p in self.players:
            if p.nick == nick:
                p.elo[game_type] = new_elo
                return


class FakePlayer(Player):
    def __init__(self, nick: str, elo: dict[GameType, int], connection: WebSocketServerProtocol = None):
        super().__init__(nick, elo, connection)
        self.sent_messages: list[str] = []

    async def send(self, message: str):
        self.sent_messages.append(message)