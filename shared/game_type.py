from enum import Enum


class GameType(Enum):
    BLITZ = 1
    RAPID = 2
    CLASSIC = 3


TIMES = {
    GameType.BLITZ: 5 * 60 * 1000,
    GameType.RAPID: 30 * 60 * 1000,
    GameType.CLASSIC: 2 * 60 * 60 * 1000
}
