import pytest

from shared.chessboard import Chessboard, within_board, distance, on_same_line, is_between, on_same_row, \
    on_same_diagonal, unit_vector_to
from shared.position import Vector2d
from shared.piece import Pawn, Team, Queen, Knight


def test_init():
    white_pawn = Pawn(Team.WHITE, Vector2d(2, 5))
    white_knight = Knight(Team.WHITE, Vector2d(1, 1))
    black_queen = Queen(Team.BLACK, Vector2d(5, 7))

    board = Chessboard([white_pawn, white_knight, black_queen])

    assert board.piece_at(Vector2d(2, 5)) is white_pawn
    assert board.piece_at(Vector2d(1, 1)) is white_knight
    assert board.piece_at(Vector2d(5, 7)) is black_queen

    assert len(board.pieces[Team.WHITE].all) == 2
    assert white_pawn in board.pieces[Team.WHITE].pawns
    assert white_knight in board.pieces[Team.WHITE].knights

    assert len(board.pieces[Team.BLACK].all) == 1
    assert black_queen in board.pieces[Team.BLACK].queens

    for i in range(8):
        for j in range(8):
            if (i, j) not in ((2, 5), (1, 1), (5, 7)):
                assert board.piece_at(Vector2d(i, j)) is None


def test_outside_board():
    board = Chessboard([])

    with pytest.raises(KeyError):
        board.piece_at(Vector2d(-1, 5))

    with pytest.raises(KeyError):
        board.piece_at(Vector2d(5, -1))

    with pytest.raises(KeyError):
        board.piece_at(Vector2d(8, 5))

    with pytest.raises(KeyError):
        board.piece_at(Vector2d(5, 8))


def test_remove_piece():
    board = Chessboard([Pawn(Team.WHITE, Vector2d(2, 5))])

    board.remove_piece(Vector2d(2, 5))

    assert board.piece_at(Vector2d(2, 5)) is None
    assert len(board.pieces[Team.WHITE].all) == 0


def test_set_piece():
    board = Chessboard([])
    white_pawn = Pawn(Team.WHITE, Vector2d(2, 5))

    board.set_piece(white_pawn)

    assert board.piece_at(Vector2d(2, 5)) is white_pawn
    assert len(board.pieces[Team.WHITE].all) == 1
    assert white_pawn in board.pieces[Team.WHITE].pawns


def test_move():
    white_pawn = Pawn(Team.WHITE, Vector2d(2, 5))
    board = Chessboard([white_pawn])

    board.move(Vector2d(2, 5), Vector2d(2, 6))

    assert board.piece_at(Vector2d(2, 5)) is None
    assert board.piece_at(Vector2d(2, 6)) is white_pawn
    assert white_pawn.position == Vector2d(2, 6)


def test_any_piece_between():
    board = Chessboard([Pawn(Team.WHITE, Vector2d(4, 5)), Pawn(Team.BLACK, Vector2d(6, 5))])

    assert not board.any_piece_between(Vector2d(5, 1), Vector2d(5, 7))
    assert not board.any_piece_between(Vector2d(5, 7), Vector2d(5, 1))
    assert not board.any_piece_between(Vector2d(2, 6), Vector2d(5, 6))
    assert not board.any_piece_between(Vector2d(5, 6), Vector2d(2, 6))
    assert not board.any_piece_between(Vector2d(1, 7), Vector2d(5, 3))
    assert not board.any_piece_between(Vector2d(5, 3), Vector2d(1, 7))
    assert not board.any_piece_between(Vector2d(3, 3), Vector2d(6, 6))
    assert not board.any_piece_between(Vector2d(6, 6), Vector2d(3, 3))
    assert board.any_piece_between(Vector2d(7, 6), Vector2d(5, 4))
    assert board.any_piece_between(Vector2d(5, 4), Vector2d(7, 6))
    assert board.any_piece_between(Vector2d(4, 7), Vector2d(7, 4))
    assert board.any_piece_between(Vector2d(7, 4), Vector2d(4, 7))
    assert board.any_piece_between(Vector2d(6, 6), Vector2d(6, 2))
    assert board.any_piece_between(Vector2d(6, 2), Vector2d(6, 6))
    assert board.any_piece_between(Vector2d(2, 5), Vector2d(5, 5))
    assert board.any_piece_between(Vector2d(5, 5), Vector2d(2, 5))


def test_next_piece_on_line():
    white_pawn_1 = Pawn(Team.WHITE, Vector2d(0, 5))
    white_pawn_2 = Pawn(Team.WHITE, Vector2d(2, 1))
    white_pawn_3 = Pawn(Team.WHITE, Vector2d(2, 3))
    black_pawn_1 = Pawn(Team.WHITE, Vector2d(4, 3))
    black_pawn_2 = Pawn(Team.WHITE, Vector2d(4, 5))

    board = Chessboard([
        white_pawn_1,
        white_pawn_2,
        white_pawn_3,
        black_pawn_1,
        black_pawn_2
    ])

    assert board.next_piece_on_line(Vector2d(2, 1), Vector2d(2, 3)) is None
    assert board.next_piece_on_line(Vector2d(0, 5), Vector2d(2, 3)) is None
    assert board.next_piece_on_line(Vector2d(4, 3), Vector2d(2, 3)) is None
    assert board.next_piece_on_line(Vector2d(4, 5), Vector2d(2, 3)) is None
    assert board.next_piece_on_line(Vector2d(0, 1), Vector2d(2, 3)) is black_pawn_2
    assert board.next_piece_on_line(Vector2d(0, 3), Vector2d(2, 3)) is black_pawn_1
    assert board.next_piece_on_line(Vector2d(2, 7), Vector2d(2, 3)) is white_pawn_2
    assert board.next_piece_on_line(Vector2d(3, 2), Vector2d(2, 3)) is white_pawn_1


def test_within_board():
    assert within_board(Vector2d(0, 0))
    assert within_board(Vector2d(7, 7))
    assert within_board(Vector2d(7, 0))
    assert within_board(Vector2d(0, 7))
    assert not within_board(Vector2d(4, 8))
    assert not within_board(Vector2d(8, 3))
    assert not within_board(Vector2d(6, -1))
    assert not within_board(Vector2d(-1, 6))


def test_distance():
    assert distance(Vector2d(4, 6), Vector2d(3, 5)) == 1
    assert distance(Vector2d(4, 6), Vector2d(5, 7)) == 1
    assert distance(Vector2d(4, 6), Vector2d(3, 6)) == 1
    assert distance(Vector2d(4, 6), Vector2d(1, 6)) == 3


def test_on_same_line():
    assert not on_same_line(Vector2d(4, 6), Vector2d(2, 5))
    assert not on_same_line(Vector2d(4, 6), Vector2d(0, 7))
    assert not on_same_line(Vector2d(4, 6), Vector2d(0, 6), Vector2d(5, 7))
    assert not on_same_line(Vector2d(4, 6), Vector2d(5, 5), Vector2d(0, 2))
    assert on_same_line(Vector2d(4, 6), Vector2d(3, 5))
    assert on_same_line(Vector2d(4, 6), Vector2d(5, 7))
    assert on_same_line(Vector2d(4, 6), Vector2d(3, 6))
    assert on_same_line(Vector2d(4, 6), Vector2d(1, 6))
    assert on_same_line(Vector2d(4, 6), Vector2d(3, 6), Vector2d(6, 6))
    assert on_same_line(Vector2d(4, 6), Vector2d(3, 5), Vector2d(1, 3))


def test_is_between():
    assert not is_between(Vector2d(4, 4), Vector2d(1, 1), Vector2d(3, 3))
    assert not is_between(Vector2d(4, 4), Vector2d(5, 1), Vector2d(7, 4))
    assert is_between(Vector2d(4, 4), Vector2d(3, 3), Vector2d(7, 7))
    assert is_between(Vector2d(4, 4), Vector2d(4, 5), Vector2d(4, 3))


def test_on_same_row():
    assert not on_same_row(Vector2d(1, 5), Vector2d(0, 4))
    assert on_same_row(Vector2d(1, 5), Vector2d(1, 7))
    assert on_same_row(Vector2d(1, 5), Vector2d(4, 5))


def test_on_same_diagonal():
    assert not on_same_diagonal(Vector2d(1, 5), Vector2d(1, 7))
    assert on_same_diagonal(Vector2d(1, 5), Vector2d(3, 7))
    assert on_same_diagonal(Vector2d(1, 5), Vector2d(6, 0))


def test_unit_vector_to():
    assert unit_vector_to(Vector2d(3, 2), Vector2d(3, 6)) == Vector2d(0, 1)
    assert unit_vector_to(Vector2d(3, 2), Vector2d(2, 2)) == Vector2d(-1, 0)
    assert unit_vector_to(Vector2d(3, 2), Vector2d(2, 1)) == Vector2d(-1, -1)
    assert unit_vector_to(Vector2d(3, 2), Vector2d(4, 3)) == Vector2d(1, 1)
