from shared.game.game_type import GameType


class Player:
    def __init__(self, nick: str, elo: dict[GameType, int]):
        self.nick = nick
        self.elo = elo
