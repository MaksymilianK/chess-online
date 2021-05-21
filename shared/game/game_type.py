from enum import Enum


class GameType(Enum):
    BLITZ = "BLITZ"
    RAPID = "RAPID"
    CLASSIC = "CLASSIC"


GAME_TYPES_BY_NAME = {
    "BLITZ": GameType.BLITZ,
    "RAPID": GameType.RAPID,
    "CLASSIC": GameType.CLASSIC
}


TIMES = {
    GameType.BLITZ: 5 * 60 * 1000,
    GameType.RAPID: 30 * 60 * 1000,
    GameType.CLASSIC: 2 * 60 * 60 * 1000
}
