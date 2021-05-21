from enum import Enum


class GameType(Enum):
    BLITZ = 1
    RAPID = 2
    CLASSIC = 3


GAME_TYPES_BY_CODE = {
    1: GameType.BLITZ,
    2: GameType.RAPID,
    3: GameType.CLASSIC
}


TIMES = {
    GameType.BLITZ: 5 * 60 * 1000,
    GameType.RAPID: 30 * 60 * 1000,
    GameType.CLASSIC: 2 * 60 * 60 * 1000
}
