from __future__ import annotations

from collections import defaultdict
from enum import Enum, auto
from typing import Optional, DefaultDict

from shared.move import AbstractMove
from shared.piece import Team, PieceType
from shared.position import Vector2d


class CastleRight(Enum):
    NONE = auto()
    SHORT = auto()
    LONG = auto()
    BOTH = auto()


class BoardSnapshot:
    def __init__(self, pieces: dict[Vector2d, PieceType], currently_moving_team: Team,
                 castle_rights: dict[Team, CastleRight], en_passant_available: bool):
        self._pieces = pieces
        self._currently_moving_team = currently_moving_team
        self._castle_rights = castle_rights
        self._en_passant_available = en_passant_available

    def __hash__(self) -> int:
        return hash((
            ((pos, piece) for pos, piece in self._pieces.items()),
            self._currently_moving_team,
            ((team, right) for team, right in self._castle_rights.items()),
            self._en_passant_available
        ))

    def __eq__(self, other: BoardSnapshot) -> bool:
        return self._pieces == other._pieces \
                and self._currently_moving_team == other._currently_moving_team \
                and self._castle_rights == other._castle_rights \
                and self._en_passant_available == other._en_passant_available


class MoveHistory:
    def __init__(self, moves: list[AbstractMove] = None):
        self._moves: list[AbstractMove] = moves or []
        self._board_snapshots: DefaultDict[BoardSnapshot, int] = defaultdict(int)
        self._last_snapshot: Optional[BoardSnapshot] = None

    def add_new(self, move: AbstractMove, board_snapshot: BoardSnapshot):
        self._moves.append(move)
        self._board_snapshots[board_snapshot] += 1
        self._last_snapshot = board_snapshot

    def repeated_three_times(self) -> bool:
        return self._board_snapshots[self._last_snapshot] >= 3

    def repeated_five_times(self) -> bool:
        return self._board_snapshots[self._last_snapshot] >= 5

    @property
    def last_move(self) -> Optional[AbstractMove]:
        return None if len(self._moves) == 0 else self._moves[-1]
