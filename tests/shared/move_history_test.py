from shared.move import Move, Capturing
from shared.move_history import MoveHistory, BoardSnapshot, CastleRight
from shared.piece import PieceType, Team
from shared.position import Vector2d


def test_repeated_three_times():
    move_history = MoveHistory()

    repeating_snapshot = BoardSnapshot(
        {Vector2d(1, 1): (PieceType.PAWN, Team.WHITE), Vector2d(2, 2): (PieceType.ROOK, Team.BLACK)},
        Team.WHITE,
        {Team.WHITE: CastleRight.LONG, Team.BLACK: CastleRight.BOTH},
        True
    )

    other_castle_right_snapshot = BoardSnapshot(
        {Vector2d(1, 1): (PieceType.PAWN, Team.WHITE), Vector2d(2, 2): (PieceType.ROOK, Team.BLACK)},
        Team.WHITE,
        {Team.WHITE: CastleRight.LONG, Team.BLACK: CastleRight.SHORT},
        True
    )

    move_history.add_snapshot(repeating_snapshot)
    move_history.add_snapshot(repeating_snapshot)

    assert not move_history.repeated_three_times()
    move_history.add_snapshot(repeating_snapshot)
    assert move_history.repeated_three_times()
    move_history.add_snapshot(other_castle_right_snapshot)
    assert not move_history.repeated_three_times()


def test_repeated_five_times():
    move_history = MoveHistory()

    repeating_snapshot = BoardSnapshot(
        {Vector2d(1, 1): (PieceType.PAWN, Team.WHITE), Vector2d(2, 2): (PieceType.ROOK, Team.BLACK)},
        Team.WHITE,
        {Team.WHITE: CastleRight.LONG, Team.BLACK: CastleRight.BOTH},
        True
    )

    other_en_passant_snapshot = BoardSnapshot(
        {Vector2d(1, 1): (PieceType.PAWN, Team.WHITE), Vector2d(2, 2): (PieceType.ROOK, Team.BLACK)},
        Team.WHITE,
        {Team.WHITE: CastleRight.LONG, Team.BLACK: CastleRight.BOTH},
        False
    )

    move_history.add_snapshot(repeating_snapshot)
    move_history.add_snapshot(repeating_snapshot)
    move_history.add_snapshot(repeating_snapshot)
    move_history.add_snapshot(repeating_snapshot)
    assert not move_history.repeated_five_times()
    move_history.add_snapshot(repeating_snapshot)
    assert move_history.repeated_five_times()
    move_history.add_snapshot(other_en_passant_snapshot)
    assert not move_history.repeated_five_times()


def test_fifty_move_rule():
    move_history = MoveHistory()

    snapshot = BoardSnapshot(
        {
            Vector2d(1, 1): (PieceType.BISHOP, Team.WHITE),
            Vector2d(4, 4): (PieceType.PAWN, Team.WHITE),
            Vector2d(2, 2): (PieceType.ROOK, Team.BLACK),
        },
        Team.WHITE,
        {Team.WHITE: CastleRight.LONG, Team.BLACK: CastleRight.BOTH},
        True
    )

    white_move = Move(Vector2d(1, 0), Vector2d(1, 1))
    black_move = Move(Vector2d(2, 1), Vector2d(2, 2))

    for i in range(49):
        move_history.update(white_move, snapshot)
        move_history.update(black_move, snapshot)

    assert not move_history.fifty_moves_rule_satisfied()
    move_history.update(white_move, snapshot)
    assert not move_history.fifty_moves_rule_satisfied()
    move_history.update(black_move, snapshot)
    assert move_history.fifty_moves_rule_satisfied()
    move_history.update(Capturing(Vector2d(1, 0), Vector2d(1, 1)), snapshot)
    assert not move_history.fifty_moves_rule_satisfied()

    white_move = Move(Vector2d(4, 3), Vector2d(4, 4))

    for i in range(55):
        move_history.update(white_move, snapshot)
        move_history.update(black_move, snapshot)

    assert not move_history.fifty_moves_rule_satisfied()
