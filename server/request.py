from shared.chess_engine.chessboard import within_board
from shared.chess_engine.position import Vector2d


class InvalidRequestException(Exception):
    def __init__(self, message: str):
        self.message = message


def assert_in(message: dict, *fields: tuple[str, type]):
    for field, t in fields:
        if field not in message or not isinstance(field, t):
            raise InvalidRequestException("invalid message format")


def parse_vector(data: tuple) -> Vector2d:
    if len(data) != 2 or type(data[0]) != int or type[data[1]] != int:
        raise InvalidRequestException("invalid position format")

    vector = Vector2d(data[0], data[1])
    if not within_board(vector):
        raise InvalidRequestException("position is not within board")

    return vector

