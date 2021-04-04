import pytest

from shared.position import Vector2d
from shared.team import Pawn, Team, Knight, Bishop, Rook, Queen, King, PlayerPieceSet


def test_has_moved():
    white_pawn = Pawn(Team.WHITE, Vector2d(5, 4), False)

    white_pawn.position = Vector2d(5, 5)

    assert white_pawn.has_moved


def test_pawn_attack_move_vectors():
    white_pawn = Pawn(Team.WHITE, Vector2d(5, 1))
    black_pawn = Pawn(Team.BLACK, Vector2d(1, 7))

    assert len(white_pawn.attack_vectors) == 2
    assert Vector2d(-1, 1) in white_pawn.attack_vectors
    assert Vector2d(1, 1) in white_pawn.attack_vectors

    assert len(white_pawn.move_vectors) == 1
    assert Vector2d(0, 1) in white_pawn.move_vectors

    assert len(black_pawn.attack_vectors) == 2
    assert Vector2d(-1, -1) in black_pawn.attack_vectors
    assert Vector2d(1, -1) in black_pawn.attack_vectors

    assert len(black_pawn.move_vectors) == 1
    assert Vector2d(0, -1) in black_pawn.move_vectors


def test_knight_move_vectors():
    knight = Knight(Team.WHITE, Vector2d(3, 4))

    assert len(knight.move_vectors) == 8
    assert Vector2d(-2, 1) in knight.move_vectors
    assert Vector2d(-1, 2) in knight.move_vectors
    assert Vector2d(1, 2) in knight.move_vectors
    assert Vector2d(2, 1) in knight.move_vectors
    assert Vector2d(2, -1) in knight.move_vectors
    assert Vector2d(1, -2) in knight.move_vectors
    assert Vector2d(-1, -2) in knight.move_vectors
    assert Vector2d(-2, -1) in knight.move_vectors


def test_bishop_move_vectors():
    bishop = Bishop(Team.BLACK, Vector2d(2, 6))

    assert len(bishop.move_vectors) == 4
    assert Vector2d(-1, 1) in bishop.move_vectors
    assert Vector2d(1, 1) in bishop.move_vectors
    assert Vector2d(1, -1) in bishop.move_vectors
    assert Vector2d(-1, -1) in bishop.move_vectors


def test_rook_move_vectors():
    rook = Rook(Team.BLACK, Vector2d(2, 6))

    assert len(rook.move_vectors) == 4
    assert Vector2d(0, 1) in rook.move_vectors
    assert Vector2d(-1, 0) in rook.move_vectors
    assert Vector2d(1, 0) in rook.move_vectors
    assert Vector2d(0, -1) in rook.move_vectors


def test_queen_move_vectors():
    queen = Queen(Team.BLACK, Vector2d(2, 6))

    assert len(queen.move_vectors) == 8
    assert Vector2d(-1, 1) in queen.move_vectors
    assert Vector2d(1, 1) in queen.move_vectors
    assert Vector2d(1, -1) in queen.move_vectors
    assert Vector2d(-1, -1) in queen.move_vectors
    assert Vector2d(0, 1) in queen.move_vectors
    assert Vector2d(-1, 0) in queen.move_vectors
    assert Vector2d(1, 0) in queen.move_vectors
    assert Vector2d(0, -1) in queen.move_vectors


def test_king_move_vectors():
    king = King(Team.WHITE, Vector2d(2, 6))

    assert len(king.move_vectors) == 8
    assert Vector2d(-1, 1) in king.move_vectors
    assert Vector2d(1, 1) in king.move_vectors
    assert Vector2d(1, -1) in king.move_vectors
    assert Vector2d(-1, -1) in king.move_vectors
    assert Vector2d(0, 1) in king.move_vectors
    assert Vector2d(-1, 0) in king.move_vectors
    assert Vector2d(1, 0) in king.move_vectors
    assert Vector2d(0, -1) in king.move_vectors


def test_get_all_pieces():
    pawn = Pawn(Team.WHITE, Vector2d(1, 1))
    knight_1 = Knight(Team.WHITE, Vector2d(2, 1))
    knight_2 = Knight(Team.WHITE, Vector2d(4, 2))
    bishop = Bishop(Team.WHITE, Vector2d(6, 1))
    rook_1 = Rook(Team.WHITE, Vector2d(7, 4))
    rook_2 = Rook(Team.WHITE, Vector2d(1, 7))
    queen = Queen(Team.WHITE, Vector2d(2, 5))
    king = King(Team.WHITE, Vector2d(4, 5))
    piece_set = PlayerPieceSet()
    piece_set.pawns.append(pawn)
    piece_set.knights.append(knight_1)
    piece_set.knights.append(knight_2)
    piece_set.bishops.append(bishop)
    piece_set.rooks.append(rook_1)
    piece_set.rooks.append(rook_2)
    piece_set.queens.append(queen)
    piece_set.king = king

    all_pieces = piece_set.all

    assert len(all_pieces) == 8
    assert pawn in all_pieces
    assert knight_1 in all_pieces
    assert knight_2 in all_pieces
    assert bishop in all_pieces
    assert rook_1 in all_pieces
    assert rook_2 in all_pieces
    assert queen in all_pieces
    assert king in all_pieces


def test_add_piece():
    pieces = PlayerPieceSet()
    white_pawn = Pawn(Team.WHITE, Vector2d(1, 1))
    white_knight = Knight(Team.WHITE, Vector2d(2, 1))
    white_bishop = Bishop(Team.WHITE, Vector2d(3, 1))
    white_rook = Rook(Team.WHITE, Vector2d(4, 1))
    white_queen = Queen(Team.WHITE, Vector2d(5, 1))
    white_king = King(Team.WHITE, Vector2d(6, 1))
    pieces.add(white_pawn)
    pieces.add(white_knight)
    pieces.add(white_bishop)
    pieces.add(white_rook)
    pieces.add(white_queen)
    pieces.add(white_king)

    assert len(pieces.all) == 6
    assert white_pawn in pieces.pawns
    assert white_knight in pieces.knights
    assert white_bishop in pieces.bishops
    assert white_rook in pieces.rooks
    assert white_queen in pieces.queens
    assert white_king is pieces.king


def test_remove_piece():
    pieces = PlayerPieceSet()
    white_pawn = Pawn(Team.WHITE, Vector2d(1, 1))
    white_knight = Knight(Team.WHITE, Vector2d(2, 1))
    white_bishop = Bishop(Team.WHITE, Vector2d(3, 1))
    white_rook = Rook(Team.WHITE, Vector2d(4, 1))
    white_queen = Queen(Team.WHITE, Vector2d(5, 1))
    white_king = King(Team.WHITE, Vector2d(6, 1))
    pieces.add(white_pawn)
    pieces.add(white_knight)
    pieces.add(white_bishop)
    pieces.add(white_rook)
    pieces.add(white_queen)
    pieces.add(white_king)
    pieces.remove(white_pawn)
    pieces.remove(white_knight)
    pieces.remove(white_bishop)
    pieces.remove(white_rook)
    pieces.remove(white_queen)

    assert len(pieces.all) == 1
    assert white_king is pieces.king

    with pytest.raises(RuntimeError):
        pieces.remove(white_king)
