from abc import ABC, abstractmethod
from enum import Enum, auto

from shared.chess_engine.position import Vector2d, UP, DOWN, UP_RIGHT, UP_LEFT, DOWN_LEFT, DOWN_RIGHT, LEFT, RIGHT


class Team(Enum):
    WHITE = 1
    BLACK = 2


class PieceType(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6


PIECE_TYPES_FROM_CODE = {
    1: PieceType.PAWN,
    2: PieceType.KNIGHT,
    3: PieceType.BISHOP,
    4: PieceType.ROOK,
    5: PieceType.QUEEN,
    6: PieceType.KING
}


def opposite_team(team: Team) -> Team:
    return Team.WHITE if team == Team.BLACK else Team.BLACK


class Piece(ABC):
    def __init__(self, team: Team, position: Vector2d, has_moved: bool = False):
        self.team = team
        self._position = position
        self.has_moved = has_moved

    @property
    def position(self) -> Vector2d:
        return self._position

    @position.setter
    def position(self, new_pos: Vector2d):
        self._position = new_pos
        self.has_moved = True

    @property
    @abstractmethod
    def move_vectors(self) -> list[Vector2d]:
        pass

    @property
    @abstractmethod
    def type(self) -> PieceType:
        pass


class Pawn(Piece):
    moves = {Team.WHITE: [UP], Team.BLACK: [DOWN]}
    attacks = {Team.WHITE: [UP_LEFT, UP_RIGHT], Team.BLACK: [DOWN_LEFT, DOWN_RIGHT]}

    @property
    def attack_vectors(self) -> list[Vector2d]:
        return Pawn.attacks[self.team]

    @property
    def move_vectors(self) -> list[Vector2d]:
        return Pawn.moves[self.team]

    @property
    def type(self) -> PieceType:
        return PieceType.PAWN


class Knight(Piece):
    moves = [Vector2d(x, y) for (x, y) in ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))]

    @property
    def move_vectors(self) -> list[Vector2d]:
        return Knight.moves

    @property
    def type(self) -> PieceType:
        return PieceType.KNIGHT


class Bishop(Piece):
    moves = [UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT]

    @property
    def move_vectors(self) -> list[Vector2d]:
        return Bishop.moves

    @property
    def type(self) -> PieceType:
        return PieceType.BISHOP


class Rook(Piece):
    moves = [UP, RIGHT, DOWN, LEFT]

    @property
    def move_vectors(self) -> list[Vector2d]:
        return Rook.moves

    @property
    def type(self) -> PieceType:
        return PieceType.ROOK


class Queen(Piece):
    moves = Bishop.moves + Rook.moves

    @property
    def move_vectors(self) -> list[Vector2d]:
        return Queen.moves

    @property
    def type(self) -> PieceType:
        return PieceType.QUEEN


class King(Piece):
    @property
    def move_vectors(self) -> list[Vector2d]:
        return Queen.moves

    @property
    def type(self) -> PieceType:
        return PieceType.KING


class PlayerPieceSet:
    def __init__(self):
        self.pawns: list[Pawn] = []
        self.knights: list[Knight] = []
        self.bishops: list[Bishop] = []
        self.rooks: list[Rook] = []
        self.queens: list[Queen] = []
        self.king: King = None

    def add(self, piece: Piece):
        if piece.type == PieceType.PAWN:
            self.pawns.append(piece)
        elif piece.type == PieceType.KNIGHT:
            self.knights.append(piece)
        elif piece.type == PieceType.BISHOP:
            self.bishops.append(piece)
        elif piece.type == PieceType.ROOK:
            self.rooks.append(piece)
        elif piece.type == PieceType.QUEEN:
            self.queens.append(piece)
        else:
            self.king = piece

    def remove(self, piece: Piece):
        if piece.type == PieceType.PAWN:
            self.pawns.remove(piece)
        elif piece.type == PieceType.KNIGHT:
            self.knights.remove(piece)
        elif piece.type == PieceType.BISHOP:
            self.bishops.remove(piece)
        elif piece.type == PieceType.ROOK:
            self.rooks.remove(piece)
        elif piece.type == PieceType.QUEEN:
            self.queens.remove(piece)
        else:
            raise RuntimeError("Cannot remove the king from a piece set")

    @property
    def all(self) -> list[Piece]:
        pieces = self.pawns + self.knights + self.bishops + self.rooks + self.queens
        if self.king is not None:
            pieces.append(self.king)

        return pieces
