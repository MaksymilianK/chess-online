from __future__ import annotations

from abc import abstractmethod, ABC
from enum import Enum, auto

from shared.chess_engine.position import Vector2d
from shared.chess_engine.piece import PieceType


class MoveType(Enum):
    MOVE = auto()
    CAPTURING = auto()
    CASTLING = auto()
    EN_PASSANT = auto()
    PROMOTION = auto()
    PROMOTION_WITH_CAPTURING = auto()


class AbstractMove(ABC):
    def __init__(self, position_from: Vector2d, position_to: Vector2d):
        self.position_from = position_from
        self.position_to = position_to

    @property
    @abstractmethod
    def type(self) -> MoveType:
        pass

    def __eq__(self, other: AbstractMove):
        return self.type == other.type and self.position_from == other.position_from \
               and self.position_to == other.position_to

    def __hash__(self):
        return hash((self.type, self.position_from, self.position_to))


class Move(AbstractMove):
    def __init__(self, position_from: Vector2d, position_to: Vector2d):
        super().__init__(position_from, position_to)

    @property
    def type(self) -> MoveType:
        return MoveType.MOVE


class Capturing(AbstractMove):
    def __init__(self, position_from: Vector2d, position_to: Vector2d):
        super().__init__(position_from, position_to)

    @property
    def type(self) -> MoveType:
        return MoveType.CAPTURING


class Castling(AbstractMove):
    def __init__(self, position_from: Vector2d, position_to: Vector2d, rook_from: Vector2d, rook_to: Vector2d):
        super().__init__(position_from, position_to)
        self.rook_from = rook_from
        self.rook_to = rook_to

    @property
    def type(self) -> MoveType:
        return MoveType.CASTLING

    def __eq__(self, other: AbstractMove):
        return super().__eq__(other) and self.rook_from == other.rook_from and self.rook_to == other.rook_to

    def __hash__(self):
        return hash((self.type, self.position_from, self.position_to, self.rook_from, self.rook_to))


class EnPassant(AbstractMove):
    def __init__(self, position_from: Vector2d, position_to: Vector2d, captured_position: Vector2d):
        super().__init__(position_from, position_to)
        self.captured_position = captured_position

    @property
    def type(self) -> MoveType:
        return MoveType.EN_PASSANT

    def __eq__(self, other: AbstractMove):
        return super().__eq__(other) and self.captured_position == other.captured_position

    def __hash__(self):
        return hash((self.type, self.position_from, self.position_to, self.captured_position))


class Promotion(AbstractMove):
    def __init__(self, position_from: Vector2d, position_to: Vector2d, piece_type: PieceType = None):
        super().__init__(position_from, position_to)
        self.piece_type = piece_type

    @property
    def type(self) -> MoveType:
        return MoveType.PROMOTION

    def __eq__(self, other: AbstractMove):
        return super().__eq__(other) and self.piece_type == other.piece_type

    def __hash__(self):
        return hash((self.type, self.position_from, self.position_to, self.piece_type))


class PromotionWithCapturing(Promotion):
    def __init__(self, position_from: Vector2d, position_to: Vector2d, piece_type: PieceType = None):
        super().__init__(position_from, position_to)
        self.piece_type = piece_type

    @property
    def type(self) -> MoveType:
        return MoveType.PROMOTION_WITH_CAPTURING
