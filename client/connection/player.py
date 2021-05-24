from shared.game.game_type import GameType, GAME_TYPES_BY_NAME


def player_from_dict(player_dict: dict):
    elo: dict[GameType, int] = {}
    for game_type_name, elo_value in player_dict["elo"].items():
        elo[GAME_TYPES_BY_NAME[game_type_name]] = elo_value

    return Player(player_dict["nick"], elo)


class Player:
    def __init__(self, nick: str, elo: dict[GameType, int]):
        self.nick = nick
        self.elo = elo

    def __eq__(self, other):
        return isinstance(other, Player) and self.nick == other.nick

    def __hash__(self) -> int:
        return hash(self.nick)
