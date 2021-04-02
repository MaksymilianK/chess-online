from abc import abstractmethod, ABC
from enum import Enum, auto

from shared.position import Vector2d
from shared.team import PieceType


class MoveType(Enum):
    MOVE = auto()
    CAPTURING = auto()
    CASTLING = auto()
    EN_PASSANT = auto()
    PROMOTION = auto()


class AbstractMove(ABC):
    def __init__(self, position_from: Vector2d, position_to: Vector2d):
        self.position_from = position_from
        self.position_to = position_to

    @abstractmethod
    @property
    def type(self) -> MoveType:
        pass


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


class EnPassant(AbstractMove):
    def __init__(self, position_from: Vector2d, position_to: Vector2d, captured_position: Vector2d):
        super().__init__(position_from, position_to)
        self.captured_position = captured_position

    @property
    def type(self) -> MoveType:
        return MoveType.EN_PASSANT


class Promotion(AbstractMove):
    def __init__(self, position_from: Vector2d, position_to: Vector2d, piece_type: PieceType = None):
        super().__init__(position_from, position_to)
        self.piece_type = piece_type

    @property
    def type(self) -> MoveType:
        return MoveType.PROMOTION
