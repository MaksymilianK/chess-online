import pytest

from shared.chessboard import Chessboard, within_board, distance, on_same_line, is_between, on_same_row, \
    on_same_diagonal
from shared.position import Vector2d
from shared.team import Pawn, Team, Queen, Knight


def test_init_without_pieces():
    board = Chessboard()

    for i in range(8):
        for j in range(8):
            assert board.piece_at(Vector2d(i, j)) is None

    with pytest.raises(KeyError):
        board.piece_at(Vector2d(-1, 5))

    with pytest.raises(KeyError):
        board.piece_at(Vector2d(5, -1))

    with pytest.raises(KeyError):
        board.piece_at(Vector2d(8, 5))

    with pytest.raises(KeyError):
        board.piece_at(Vector2d(5, 8))


def test_init_with_pieces():
    white_pawn = Pawn(Team.WHITE, Vector2d(2, 5))
    white_knight = Knight(Team.WHITE, Vector2d(1, 1))
    black_queen = Queen(Team.BLACK, Vector2d(5, 7))

    board = Chessboard([white_pawn, white_knight, black_queen])

    assert board.piece_at(Vector2d(2, 5)) is white_pawn
    assert board.piece_at(Vector2d(1, 1)) is white_knight
    assert board.piece_at(Vector2d(5, 7)) is black_queen

    for i in range(8):
        for j in range(8):
            if (i, j) not in ((2, 5), (1, 1), (5, 7)):
                assert board.piece_at(Vector2d(i, j)) is None


def test_remove_piece():
    board = Chessboard([Pawn(Team.WHITE, Vector2d(2, 5))])

    board.remove_piece(Vector2d(2, 5))

    assert board.piece_at(Vector2d(2, 5)) is None


def test_set_piece():
    board = Chessboard()
    white_pawn = Pawn(Team.WHITE, Vector2d(2, 5))

    board.set_piece(white_pawn)

    assert board.piece_at(Vector2d(2, 5)) is white_pawn


def test_move():
    white_pawn = Pawn(Team.WHITE, Vector2d(2, 5))
    board = Chessboard([white_pawn])

    board.move(Vector2d(2, 5), Vector2d(2, 6))

    assert board.piece_at(Vector2d(2, 5)) is None
    assert board.piece_at(Vector2d(2, 6)) is white_pawn
    assert white_pawn.position == Vector2d(2, 6)


def test_is_any_piece_between():
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
    board = Chessboard([Pawn(Team.WHITE, Vector2d(4, 5)), Pawn(Team.BLACK, Vector2d(6, 5))])

    assert board.next_piece_on_line(Vector2d(5, 1), Vector2d(5, 7)) is None
    assert board.next_piece_on_line(Vector2d(5, 7), Vector2d(5, 1)) is None
    assert board.next_piece_on_line(Vector2d(2, 6), Vector2d(5, 6)) is None
    assert board.next_piece_on_line(Vector2d(5, 6), Vector2d(2, 6)) is None
    assert board.next_piece_on_line(Vector2d(1, 7), Vector2d(5, 3)) is None
    assert board.next_piece_on_line(Vector2d(5, 3), Vector2d(1, 7)) is None
    assert board.next_piece_on_line(Vector2d(3, 3), Vector2d(6, 6)) is None
    assert board.next_piece_on_line(Vector2d(6, 6), Vector2d(3, 3)) is None
    assert board.next_piece_on_line(Vector2d(7, 6), Vector2d(5, 4)) is not None
    assert board.next_piece_on_line(Vector2d(5, 4), Vector2d(7, 6)) is not None
    assert board.next_piece_on_line(Vector2d(4, 7), Vector2d(7, 4)) is not None
    assert board.next_piece_on_line(Vector2d(7, 4), Vector2d(4, 7)) is not None
    assert board.next_piece_on_line(Vector2d(6, 6), Vector2d(6, 2)) is not None
    assert board.next_piece_on_line(Vector2d(6, 2), Vector2d(6, 6)) is not None
    assert board.next_piece_on_line(Vector2d(2, 5), Vector2d(5, 5)) is not None
    assert board.next_piece_on_line(Vector2d(5, 5), Vector2d(2, 5)) is not None


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


def test_is_on_same_row():
    assert not on_same_row(Vector2d(1, 5), Vector2d(0, 4))
    assert on_same_row(Vector2d(1, 5), Vector2d(1, 7))
    assert on_same_row(Vector2d(1, 5), Vector2d(4, 5))


def test_is_on_same_diagonal():
    assert not on_same_diagonal(Vector2d(1, 5), Vector2d(1, 7))
    assert on_same_diagonal(Vector2d(1, 5), Vector2d(3, 7))
    assert on_same_diagonal(Vector2d(1, 5), Vector2d(6, 0))



