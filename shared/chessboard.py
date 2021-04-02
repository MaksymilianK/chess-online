from typing import Optional

from shared.position import Vector2d, distance_x, distance_y
from shared.team import Team, Piece

# Chessboard 'ranks' are horizontal lines of fields.
FIRST_RANK = {Team.WHITE: 0, Team.BLACK: 8}
SECOND_RANK = {Team.WHITE: 1, Team.BLACK: 7}


class Chessboard:
    def __init__(self, pieces: list[Piece] = None):
        self._fields = {Vector2d(i, j): None for i in range(8) for j in range(8)}
        if pieces is not None:
            for piece in pieces:
                self._fields[piece.position] = piece

    def piece_at(self, position: Vector2d) -> Optional[Piece]:
        return self._fields[position]

    def remove_piece(self, position: Vector2d):
        self._fields[position] = None

    def set_piece(self, piece: Piece):
        self._fields[piece.position] = piece

    def move(self, pos_from: Vector2d, pos_to: Vector2d):
        piece = self._fields[pos_from]
        self._fields[pos_from] = None
        self._fields[pos_to] = piece
        piece.position = pos_to

    def any_piece_between(self, pos_1: Vector2d, pos_2: Vector2d) -> bool:
        """Method assumes that pos_1 and pos_2 are on the same line."""
        unit_vector = _unit_vector_to(pos_1, pos_2)
        pos = pos_1 + unit_vector
        while pos != pos_2:
            if self.piece_at(pos) is not None:
                return True
            pos += unit_vector

        return False

    def next_piece_on_line(self, pos_1: Vector2d, pos_2: Vector2d) -> Optional[Piece]:
        """Method assumes that pos_1 and pos_2 are on the same line."""
        unit_vector = _unit_vector_to(pos_1, pos_2)
        pos = pos_1 + unit_vector
        while within_board(pos):
            piece = self.piece_at(pos)
            if piece is not None:
                return piece
            pos += unit_vector

        return None


def within_board(position: Vector2d) -> bool:
    return 0 <= position.x < 8 and 0 <= position.y < 8


def distance(pos_1: Vector2d, pos_2: Vector2d) -> int:
    """Method assumes that pos_1 and pos_2 are on the same line."""
    if _on_same_file(pos_1, pos_2):
        return distance_y(pos_1, pos_2)
    else:
        return distance_x(pos_1, pos_2)


def on_same_line(pos_1: Vector2d, pos_2: Vector2d, pos_3: Vector2d = None) -> bool:
    """Checks if two or three positions are on the same line (file, rank or diagonal)."""
    if pos_3 is None:
        return on_same_row(pos_1, pos_2) or on_same_diagonal(pos_1, pos_2)
    else:
        return _on_same_file(pos_1, pos_2) and _on_same_file(pos_1, pos_3) \
               or _on_same_rank(pos_1, pos_2) and _on_same_rank(pos_1, pos_3) \
               or _on_same_right_up_diagonal(pos_1, pos_2) and _on_same_right_up_diagonal(pos_1, pos_3) \
               or _on_same_left_down_diagonal(pos_1, pos_2) and _on_same_left_down_diagonal(pos_1, pos_3)


def is_between(pos: Vector2d, other_1: Vector2d, other_2: Vector2d) -> bool:
    """Checks if pos is between other_1 and other_2. Method assumes that pos_1 and pos_2 are on the same line."""
    distance_others = distance(other_1, other_2)
    return distance(pos, other_1) < distance_others and distance(pos, other_2) < distance_others


def on_same_row(pos_1: Vector2d, pos_2: Vector2d) -> bool:
    return _on_same_file(pos_1, pos_2) or _on_same_rank(pos_1, pos_2)


def on_same_diagonal(pos_1: Vector2d, pos_2: Vector2d) -> bool:
    return _on_same_right_up_diagonal(pos_1, pos_2) or _on_same_left_down_diagonal(pos_1, pos_2)


# Chessboard 'files' are vertical lines of fields.
def _on_same_file(pos_1: Vector2d, pos_2: Vector2d) -> bool:
    return pos_1.x == pos_2.x


# Chessboard 'ranks' are horizontal lines of fields.
def _on_same_rank(pos_1: Vector2d, pos_2: Vector2d) -> bool:
    return pos_1.y == pos_2.y


def _on_same_right_up_diagonal(pos_1: Vector2d, pos_2: Vector2d) -> bool:
    """Checks if pos_1 and pos_2 are on a diagonal where position with greater x has lower y."""
    return pos_1.x - pos_2.x == pos_1.y - pos_2.y


def _on_same_left_down_diagonal(pos_1: Vector2d, pos_2: Vector2d) -> bool:
    """Checks if pos_1 and pos_2 are on a diagonal where position with greater x has greater y."""
    return pos_1.x - pos_2.x == pos_2.y - pos_1.y


def _unit_vector_to(pos_1: Vector2d, pos_2: Vector2d) -> Vector2d:
    """Returns a unit vector pointing from pos_1 to pos_2. It assumes that pos_1 and pos_2 are on the same line."""
    return (pos_2 - pos_1) // distance(pos_1, pos_2)
