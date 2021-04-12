from shared.chess_engine import ChessEngine
from shared.move import Move, Capturing, Promotion, PromotionWithCapturing, EnPassant, Castling
from shared.position import Vector2d
from shared.piece import Team, Pawn, Bishop, Knight, King, Rook, Queen


def test_default_init():
    engine = ChessEngine()
    assert engine.move_history.last_move is None
    assert not engine.check_status.checked
    assert engine.check_status.checking_piece_1 is None
    assert engine.check_status.checking_piece_2 is None
    assert engine.currently_moving_team == Team.WHITE

    assert len(engine.board.pieces[Team.WHITE].pawns) == 8
    assert engine.board.piece_at(Vector2d(0, 1)) in engine.board.pieces[Team.WHITE].pawns
    assert engine.board.piece_at(Vector2d(1, 1)) in engine.board.pieces[Team.WHITE].pawns
    assert engine.board.piece_at(Vector2d(2, 1)) in engine.board.pieces[Team.WHITE].pawns
    assert engine.board.piece_at(Vector2d(3, 1)) in engine.board.pieces[Team.WHITE].pawns
    assert engine.board.piece_at(Vector2d(4, 1)) in engine.board.pieces[Team.WHITE].pawns
    assert engine.board.piece_at(Vector2d(5, 1)) in engine.board.pieces[Team.WHITE].pawns
    assert engine.board.piece_at(Vector2d(6, 1)) in engine.board.pieces[Team.WHITE].pawns
    assert engine.board.piece_at(Vector2d(7, 1)) in engine.board.pieces[Team.WHITE].pawns
    assert len(engine.board.pieces[Team.WHITE].knights) == 2
    assert engine.board.piece_at(Vector2d(1, 0)) in engine.board.pieces[Team.WHITE].knights
    assert engine.board.piece_at(Vector2d(6, 0)) in engine.board.pieces[Team.WHITE].knights
    assert len(engine.board.pieces[Team.WHITE].bishops) == 2
    assert engine.board.piece_at(Vector2d(2, 0)) in engine.board.pieces[Team.WHITE].bishops
    assert engine.board.piece_at(Vector2d(5, 0)) in engine.board.pieces[Team.WHITE].bishops
    assert len(engine.board.pieces[Team.WHITE].rooks) == 2
    assert engine.board.piece_at(Vector2d(0, 0)) in engine.board.pieces[Team.WHITE].rooks
    assert engine.board.piece_at(Vector2d(7, 0)) in engine.board.pieces[Team.WHITE].rooks
    assert len(engine.board.pieces[Team.WHITE].queens) == 1
    assert engine.board.piece_at(Vector2d(3, 0)) in engine.board.pieces[Team.WHITE].queens
    assert engine.board.piece_at(Vector2d(4, 0)) is engine.board.pieces[Team.WHITE].king

    assert len(engine.board.pieces[Team.BLACK].pawns) == 8
    assert engine.board.piece_at(Vector2d(0, 6)) in engine.board.pieces[Team.BLACK].pawns
    assert engine.board.piece_at(Vector2d(1, 6)) in engine.board.pieces[Team.BLACK].pawns
    assert engine.board.piece_at(Vector2d(2, 6)) in engine.board.pieces[Team.BLACK].pawns
    assert engine.board.piece_at(Vector2d(3, 6)) in engine.board.pieces[Team.BLACK].pawns
    assert engine.board.piece_at(Vector2d(4, 6)) in engine.board.pieces[Team.BLACK].pawns
    assert engine.board.piece_at(Vector2d(5, 6)) in engine.board.pieces[Team.BLACK].pawns
    assert engine.board.piece_at(Vector2d(6, 6)) in engine.board.pieces[Team.BLACK].pawns
    assert engine.board.piece_at(Vector2d(7, 6)) in engine.board.pieces[Team.BLACK].pawns
    assert len(engine.board.pieces[Team.BLACK].knights) == 2
    assert engine.board.piece_at(Vector2d(1, 7)) in engine.board.pieces[Team.BLACK].knights
    assert engine.board.piece_at(Vector2d(6, 7)) in engine.board.pieces[Team.BLACK].knights
    assert len(engine.board.pieces[Team.BLACK].bishops) == 2
    assert engine.board.piece_at(Vector2d(2, 7)) in engine.board.pieces[Team.BLACK].bishops
    assert engine.board.piece_at(Vector2d(5, 7)) in engine.board.pieces[Team.BLACK].bishops
    assert len(engine.board.pieces[Team.BLACK].rooks) == 2
    assert engine.board.piece_at(Vector2d(0, 7)) in engine.board.pieces[Team.BLACK].rooks
    assert engine.board.piece_at(Vector2d(7, 7)) in engine.board.pieces[Team.BLACK].rooks
    assert len(engine.board.pieces[Team.BLACK].queens) == 1
    assert engine.board.piece_at(Vector2d(3, 7)) in engine.board.pieces[Team.BLACK].queens
    assert engine.board.piece_at(Vector2d(4, 7)) is engine.board.pieces[Team.BLACK].king


def test_pieces_init_not_checked():
    white_king = King(Team.WHITE, Vector2d(1, 4))
    black_king = King(Team.BLACK, Vector2d(5, 6))
    engine = ChessEngine([white_king, black_king])

    assert engine.board.piece_at(Vector2d(1, 4)) is white_king
    assert engine.board.piece_at(Vector2d(5, 6)) is black_king


def test_move_history():
    pieces = [
        King(Team.WHITE, Vector2d(1, 4)),
        King(Team.BLACK, Vector2d(5, 6))
    ]

    move_1 = Move(Vector2d(6, 5), Vector2d(5, 6))
    move_2 = Move(Vector2d(1, 3), Vector2d(1, 4))

    engine = ChessEngine(pieces, [move_1, move_2])

    assert engine.move_history.last_move is move_2
    assert engine.currently_moving_team == Team.BLACK


def test_pieces_init_single_checked():
    white_rook = Rook(Team.WHITE, Vector2d(1, 5))
    pieces = [
        King(Team.WHITE, Vector2d(4, 0)),
        King(Team.BLACK, Vector2d(4, 5)),
        white_rook
    ]

    engine = ChessEngine(pieces, [Move(Vector2d(1, 0), Vector2d(1, 5))])

    assert engine.check_status.checked
    assert not engine.check_status.double_checked
    assert engine.check_status.checking_piece_1 is white_rook
    assert engine.check_status.checking_piece_2 is None


def test_pieces_init_double_checked():
    white_knight = Knight(Team.WHITE, Vector2d(3, 3))
    white_rook = Rook(Team.WHITE, Vector2d(1, 5))
    pieces = [
        King(Team.WHITE, Vector2d(4, 0)),
        King(Team.BLACK, Vector2d(4, 5)),
        white_knight,
        white_rook
    ]

    engine = ChessEngine(pieces, [Move(Vector2d(2, 5), Vector2d(3, 3))])

    assert engine.check_status.checked
    assert engine.check_status.double_checked
    assert engine.check_status.checking_piece_1 in (white_knight, white_rook)
    assert engine.check_status.checking_piece_2 in (white_knight, white_rook)


def test_pawn_available_moves_not_checked():
    pieces = [
        Pawn(Team.WHITE, Vector2d(0, 1), has_moved=True),
        Pawn(Team.WHITE, Vector2d(0, 6), has_moved=True),
        Pawn(Team.WHITE, Vector2d(1, 1), has_moved=False),
        Pawn(Team.WHITE, Vector2d(2, 6), has_moved=True),
        Pawn(Team.WHITE, Vector2d(3, 2), has_moved=True),
        Pawn(Team.WHITE, Vector2d(6, 1), has_moved=False),
        Pawn(Team.WHITE, Vector2d(6, 3), has_moved=True),
        Pawn(Team.WHITE, Vector2d(7, 5), has_moved=True),
        Knight(Team.WHITE, Vector2d(6, 6)),
        Knight(Team.WHITE, Vector2d(7, 6)),
        King(Team.WHITE, Vector2d(3, 0)),
        King(Team.BLACK, Vector2d(7, 0)),
        Pawn(Team.BLACK, Vector2d(5, 1), has_moved=True),
        Knight(Team.BLACK, Vector2d(0, 7)),
        Knight(Team.BLACK, Vector2d(4, 3)),
        Bishop(Team.BLACK, Vector2d(2, 3)),
        Bishop(Team.BLACK, Vector2d(7, 4)),
        Rook(Team.BLACK, Vector2d(0, 2)),
        Rook(Team.BLACK, Vector2d(3, 7)),
    ]

    engine = ChessEngine(pieces, [Move(Vector2d(5, 3), Vector2d(5, 1))])

    moves_1 = engine.available_moves(Vector2d(0, 1))
    moves_2 = engine.available_moves(Vector2d(0, 6))
    moves_3 = engine.available_moves(Vector2d(1, 1))
    moves_4 = engine.available_moves(Vector2d(2, 6))
    moves_5 = engine.available_moves(Vector2d(3, 2))
    moves_6 = engine.available_moves(Vector2d(6, 1))
    moves_7 = engine.available_moves(Vector2d(6, 3))
    moves_8 = engine.available_moves(Vector2d(7, 5))

    assert len(moves_1) == 0
    assert len(moves_2) == 0
    assert len(moves_3) == 3
    assert len(moves_4) == 2
    assert len(moves_5) == 1
    assert len(moves_6) == 2
    assert len(moves_7) == 1
    assert len(moves_8) == 0

    assert Capturing(Vector2d(1, 1), Vector2d(0, 2)) in moves_3
    assert Move(Vector2d(1, 1), Vector2d(1, 2)) in moves_3
    assert Move(Vector2d(1, 1), Vector2d(1, 3)) in moves_3

    assert Promotion(Vector2d(2, 6), Vector2d(2, 7)) in moves_4
    assert PromotionWithCapturing(Vector2d(2, 6), Vector2d(3, 7)) in moves_4

    assert Move(Vector2d(3, 2), Vector2d(3, 3)) in moves_5

    assert EnPassant(Vector2d(6, 1), Vector2d(5, 2), Vector2d(5, 1)) in moves_6
    assert Move(Vector2d(6, 1), Vector2d(6, 2)) in moves_6

    assert Capturing(Vector2d(6, 3), Vector2d(7, 4)) in moves_7


def test_pawn_available_moves_single_checked():
    pieces = [
        Pawn(Team.WHITE, Vector2d(7, 6), has_moved=True),
        Rook(Team.WHITE, Vector2d(1, 5)),
        Rook(Team.WHITE, Vector2d(2, 0)),
        King(Team.WHITE, Vector2d(4, 0)),
        Pawn(Team.BLACK, Vector2d(1, 1), has_moved=True),
        Pawn(Team.BLACK, Vector2d(2, 6), has_moved=False),
        Pawn(Team.BLACK, Vector2d(4, 4), has_moved=True),
        Pawn(Team.BLACK, Vector2d(6, 6), has_moved=False),
        King(Team.BLACK, Vector2d(4, 5))
    ]

    engine = ChessEngine(pieces, [Move(Vector2d(1, 2), Vector2d(1, 5))])

    moves_2 = engine.available_moves(Vector2d(2, 6))
    assert len(engine.available_moves(Vector2d(1, 1))) == 0
    assert len(moves_2) == 2
    assert len(engine.available_moves(Vector2d(4, 4))) == 0
    assert len(engine.available_moves(Vector2d(6, 6))) == 0

    assert Capturing(Vector2d(2, 6), Vector2d(1, 5)) in moves_2
    assert Move(Vector2d(2, 6), Vector2d(2, 5)) in moves_2


def test_pawn_available_moves_double_checked():
    pieces = [
        Pawn(Team.WHITE, Vector2d(7, 6), has_moved=True),
        Knight(Team.WHITE, Vector2d(3, 3)),
        Rook(Team.WHITE, Vector2d(1, 5)),
        Rook(Team.WHITE, Vector2d(2, 0)),
        King(Team.WHITE, Vector2d(4, 0)),
        Pawn(Team.BLACK, Vector2d(1, 1), has_moved=True),
        Pawn(Team.BLACK, Vector2d(2, 6), has_moved=False),
        Pawn(Team.BLACK, Vector2d(4, 4), has_moved=True),
        Pawn(Team.BLACK, Vector2d(6, 6), has_moved=False),
        King(Team.BLACK, Vector2d(4, 5))
    ]

    engine = ChessEngine(pieces, [Move(Vector2d(7, 4), Vector2d(7, 6))])

    assert len(engine.available_moves(Vector2d(1, 1))) == 0
    assert len(engine.available_moves(Vector2d(2, 6))) == 0
    assert len(engine.available_moves(Vector2d(4, 4))) == 0
    assert len(engine.available_moves(Vector2d(6, 6))) == 0


def test_knight_available_moves_not_checked():
    pieces = [
        Knight(Team.WHITE, Vector2d(2, 2)),
        Knight(Team.WHITE, Vector2d(3, 2)),
        Knight(Team.WHITE, Vector2d(4, 3)),
        Knight(Team.WHITE, Vector2d(6, 6)),
        King(Team.WHITE, Vector2d(4, 0)),
        Bishop(Team.BLACK, Vector2d(1, 3)),
        Queen(Team.BLACK, Vector2d(4, 4)),
        King(Team.BLACK, Vector2d(4, 6))
    ]

    engine = ChessEngine(pieces, [Move(Vector2d(0, 4), Vector2d(1, 3))])

    moves_1 = engine.available_moves(Vector2d(2, 2))
    moves_2 = engine.available_moves(Vector2d(3, 2))
    moves_3 = engine.available_moves(Vector2d(4, 3))
    moves_4 = engine.available_moves(Vector2d(6, 6))

    assert len(moves_1) == 0
    assert len(moves_2) == 7
    assert len(moves_3) == 0
    assert len(moves_4) == 4

    assert Capturing(Vector2d(3, 2), Vector2d(1, 3)) in moves_2
    assert Move(Vector2d(3, 2), Vector2d(2, 4)) in moves_2
    assert Capturing(Vector2d(3, 2), Vector2d(4, 4)) in moves_2
    assert Move(Vector2d(3, 2), Vector2d(5, 3)) in moves_2
    assert Move(Vector2d(3, 2), Vector2d(5, 1)) in moves_2
    assert Move(Vector2d(3, 2), Vector2d(2, 0)) in moves_2
    assert Move(Vector2d(3, 2), Vector2d(1, 1)) in moves_2

    assert Move(Vector2d(6, 6), Vector2d(4, 7)) in moves_4
    assert Move(Vector2d(6, 6), Vector2d(7, 4)) in moves_4
    assert Move(Vector2d(6, 6), Vector2d(5, 4)) in moves_4
    assert Move(Vector2d(6, 6), Vector2d(4, 5)) in moves_4


def test_knight_available_moves_single_checked():
    pieces = [
        Knight(Team.WHITE, Vector2d(1, 4)),
        Knight(Team.WHITE, Vector2d(3, 1)),
        Knight(Team.WHITE, Vector2d(6, 4)),
        King(Team.WHITE, Vector2d(4, 0)),
        Knight(Team.BLACK, Vector2d(5, 2)),
        Queen(Team.BLACK, Vector2d(2, 2)),
        King(Team.BLACK, Vector2d(4, 7))
    ]

    engine = ChessEngine(pieces, [Move(Vector2d(4, 4), Vector2d(5, 2))])

    moves_1 = engine.available_moves(Vector2d(1, 4))
    moves_2 = engine.available_moves(Vector2d(3, 1))
    moves_3 = engine.available_moves(Vector2d(6, 4))

    assert len(moves_1) == 0
    assert len(moves_2) == 0
    assert len(moves_3) == 1

    assert Capturing(Vector2d(6, 4), Vector2d(5, 2)) in moves_3


def test_knight_available_moves_double_checked():
    pieces = [
        Knight(Team.WHITE, Vector2d(1, 4)),
        Knight(Team.WHITE, Vector2d(6, 4)),
        King(Team.WHITE, Vector2d(4, 0)),
        Knight(Team.BLACK, Vector2d(5, 2)),
        Queen(Team.BLACK, Vector2d(2, 2)),
        King(Team.BLACK, Vector2d(4, 7))
    ]

    engine = ChessEngine(pieces, [Move(Vector2d(3, 1), Vector2d(5, 2))])

    assert len(engine.available_moves(Vector2d(1, 4))) == 0
    assert len(engine.available_moves(Vector2d(6, 4))) == 0


def test_bishop_available_moves_not_checked():
    pieces = [
        Pawn(Team.WHITE, Vector2d(6, 3)),
        Pawn(Team.WHITE, Vector2d(7, 3)),
        Bishop(Team.WHITE, Vector2d(0, 3)),
        Queen(Team.WHITE, Vector2d(6, 7)),
        King(Team.WHITE, Vector2d(3, 0)),
        Bishop(Team.BLACK, Vector2d(1, 4)),
        Bishop(Team.BLACK, Vector2d(5, 7)),
        Bishop(Team.BLACK, Vector2d(6, 2)),
        King(Team.BLACK, Vector2d(4, 7))
    ]

    engine = ChessEngine(pieces, [Move(Vector2d(6, 6), Vector2d(6, 7))])

    moves_1 = engine.available_moves(Vector2d(1, 4))
    moves_2 = engine.available_moves(Vector2d(5, 7))
    moves_3 = engine.available_moves(Vector2d(6, 2))

    assert len(moves_1) == 3
    assert len(moves_2) == 0
    assert len(moves_3) == 9

    assert Capturing(Vector2d(1, 4), Vector2d(0, 3)) in moves_1
    assert Move(Vector2d(1, 4), Vector2d(2, 5)) in moves_1
    assert Move(Vector2d(1, 4), Vector2d(3, 6)) in moves_1

    assert Capturing(Vector2d(6, 2), Vector2d(7, 3)) in moves_3
    assert Move(Vector2d(6, 2), Vector2d(7, 1)) in moves_3
    assert Move(Vector2d(6, 2), Vector2d(5, 1)) in moves_3
    assert Move(Vector2d(6, 2), Vector2d(4, 0)) in moves_3
    assert Move(Vector2d(6, 2), Vector2d(5, 3)) in moves_3
    assert Move(Vector2d(6, 2), Vector2d(4, 4)) in moves_3
    assert Move(Vector2d(6, 2), Vector2d(3, 5)) in moves_3
    assert Move(Vector2d(6, 2), Vector2d(2, 6)) in moves_3
    assert Move(Vector2d(6, 2), Vector2d(1, 7)) in moves_3


def test_bishop_available_moves_single_checked():
    pieces = [
        Pawn(Team.WHITE, Vector2d(6, 3)),
        Pawn(Team.WHITE, Vector2d(7, 3)),
        Rook(Team.WHITE, Vector2d(4, 0)),
        Queen(Team.WHITE, Vector2d(6, 7)),
        King(Team.WHITE, Vector2d(3, 0)),
        Bishop(Team.BLACK, Vector2d(2, 3)),
        Bishop(Team.BLACK, Vector2d(5, 7)),
        Bishop(Team.BLACK, Vector2d(6, 2)),
        King(Team.BLACK, Vector2d(4, 7))
    ]

    engine = ChessEngine(pieces, [Move(Vector2d(7, 0), Vector2d(4, 0))])

    moves_1 = engine.available_moves(Vector2d(2, 3))
    moves_2 = engine.available_moves(Vector2d(5, 7))
    moves_3 = engine.available_moves(Vector2d(6, 2))

    assert len(moves_1) == 2
    assert len(moves_2) == 0
    assert len(moves_3) == 2

    assert Move(Vector2d(2, 3), Vector2d(4, 5)) in moves_1
    assert Move(Vector2d(2, 3), Vector2d(4, 1)) in moves_1

    assert Capturing(Vector2d(6, 2), Vector2d(4, 0)) in moves_3
    assert Move(Vector2d(6, 2), Vector2d(4, 4)) in moves_3


def test_bishop_available_moves_double_checked():
    pieces = [
        Pawn(Team.WHITE, Vector2d(6, 3)),
        Pawn(Team.WHITE, Vector2d(7, 3)),
        Bishop(Team.WHITE, Vector2d(2, 5)),
        Rook(Team.WHITE, Vector2d(4, 0)),
        Queen(Team.WHITE, Vector2d(6, 7)),
        King(Team.WHITE, Vector2d(3, 0)),
        Bishop(Team.BLACK, Vector2d(1, 4)),
        Bishop(Team.BLACK, Vector2d(5, 7)),
        Bishop(Team.BLACK, Vector2d(6, 2)),
        King(Team.BLACK, Vector2d(4, 7))
    ]

    engine = ChessEngine(pieces, [Move(Vector2d(4, 3), Vector2d(2, 5))])

    moves_1 = engine.available_moves(Vector2d(1, 4))
    moves_2 = engine.available_moves(Vector2d(5, 7))
    moves_3 = engine.available_moves(Vector2d(6, 2))

    assert len(moves_1) == 0
    assert len(moves_2) == 0
    assert len(moves_3) == 0


def test_rook_available_moves_not_checked():
    pieces = [
        Rook(Team.WHITE, Vector2d(1, 0)),
        Rook(Team.WHITE, Vector2d(3, 3)),
        Rook(Team.WHITE, Vector2d(4, 1)),
        King(Team.WHITE, Vector2d(3, 0)),
        Bishop(Team.BLACK, Vector2d(3, 1)),
        Bishop(Team.BLACK, Vector2d(4, 3)),
        Rook(Team.BLACK, Vector2d(0, 0)),
        Queen(Team.BLACK, Vector2d(6, 3)),
        King(Team.BLACK, Vector2d(4, 7))
    ]

    engine = ChessEngine(pieces, [Move(Vector2d(3, 4), Vector2d(4, 3))])

    moves_1 = engine.available_moves(Vector2d(1, 0))
    moves_2 = engine.available_moves(Vector2d(3, 3))
    moves_3 = engine.available_moves(Vector2d(4, 1))

    assert len(moves_1) == 2
    assert len(moves_2) == 10
    assert len(moves_3) == 0

    assert Capturing(Vector2d(1, 0), Vector2d(0, 0)) in moves_1
    assert Move(Vector2d(1, 0), Vector2d(2, 0)) in moves_1

    assert Move(Vector2d(3, 3), Vector2d(3, 4)) in moves_2
    assert Move(Vector2d(3, 3), Vector2d(3, 5)) in moves_2
    assert Move(Vector2d(3, 3), Vector2d(3, 6)) in moves_2
    assert Move(Vector2d(3, 3), Vector2d(3, 7)) in moves_2
    assert Capturing(Vector2d(3, 3), Vector2d(4, 3)) in moves_2
    assert Move(Vector2d(3, 3), Vector2d(3, 2)) in moves_2
    assert Capturing(Vector2d(3, 3), Vector2d(3, 1)) in moves_2
    assert Move(Vector2d(3, 3), Vector2d(2, 3)) in moves_2
    assert Move(Vector2d(3, 3), Vector2d(1, 3)) in moves_2
    assert Move(Vector2d(3, 3), Vector2d(0, 3)) in moves_2


def test_rook_available_moves_single_checked():
    pieces = [
        Rook(Team.WHITE, Vector2d(1, 3)),
        Rook(Team.WHITE, Vector2d(4, 1)),
        King(Team.WHITE, Vector2d(3, 0)),
        Bishop(Team.BLACK, Vector2d(4, 3)),
        Queen(Team.BLACK, Vector2d(0, 3)),
        King(Team.BLACK, Vector2d(3, 7))
    ]

    engine = ChessEngine(pieces, [Move(Vector2d(1, 4), Vector2d(0, 3))])

    moves_1 = engine.available_moves(Vector2d(1, 3))
    moves_2 = engine.available_moves(Vector2d(4, 1))

    assert len(moves_1) == 2
    assert len(moves_2) == 1

    assert Capturing(Vector2d(1, 3), Vector2d(0, 3)) in moves_1
    assert Move(Vector2d(1, 3), Vector2d(1, 2)) in moves_1

    assert Move(Vector2d(4, 1), Vector2d(2, 1)) in moves_2


def test_rook_available_moves_double_checked():
    pieces = [
        Rook(Team.WHITE, Vector2d(1, 3)),
        Rook(Team.WHITE, Vector2d(4, 1)),
        King(Team.WHITE, Vector2d(3, 0)),
        Knight(Team.BLACK, Vector2d(4, 2)),
        Bishop(Team.BLACK, Vector2d(4, 3)),
        Queen(Team.BLACK, Vector2d(0, 3)),
        King(Team.BLACK, Vector2d(3, 7))
    ]

    engine = ChessEngine(pieces, [Capturing(Vector2d(2, 1), Vector2d(4, 2))])

    moves_1 = engine.available_moves(Vector2d(1, 3))
    moves_2 = engine.available_moves(Vector2d(4, 1))

    assert len(moves_1) == 0
    assert len(moves_2) == 0


def test_queen_available_moves_not_checked():
    pieces = [
        Queen(Team.WHITE, Vector2d(1, 3)),
        Queen(Team.WHITE, Vector2d(4, 1)),
        Queen(Team.WHITE, Vector2d(6, 2)),
        King(Team.WHITE, Vector2d(4, 0)),
        Knight(Team.BLACK, Vector2d(2, 2)),
        Knight(Team.BLACK, Vector2d(2, 3)),
        Rook(Team.BLACK, Vector2d(4, 6)),
        Bishop(Team.BLACK, Vector2d(7, 3)),
        King(Team.BLACK, Vector2d(4, 7))
    ]

    engine = ChessEngine(pieces, [Move(Vector2d(6, 4), Vector2d(7, 3))])

    moves_1 = engine.available_moves(Vector2d(1, 3))
    moves_2 = engine.available_moves(Vector2d(4, 1))
    moves_3 = engine.available_moves(Vector2d(6, 2))

    assert len(moves_1) == 15
    assert len(moves_2) == 5
    assert len(moves_3) == 2

    assert Move(Vector2d(1, 3), Vector2d(0, 4)) in moves_1
    assert Move(Vector2d(1, 3), Vector2d(1, 4)) in moves_1
    assert Move(Vector2d(1, 3), Vector2d(1, 5)) in moves_1
    assert Move(Vector2d(1, 3), Vector2d(1, 6)) in moves_1
    assert Move(Vector2d(1, 3), Vector2d(1, 7)) in moves_1
    assert Move(Vector2d(1, 3), Vector2d(2, 4)) in moves_1
    assert Move(Vector2d(1, 3), Vector2d(3, 5)) in moves_1
    assert Capturing(Vector2d(1, 3), Vector2d(4, 6)) in moves_1
    assert Capturing(Vector2d(1, 3), Vector2d(2, 3)) in moves_1
    assert Capturing(Vector2d(1, 3), Vector2d(2, 2)) in moves_1
    assert Move(Vector2d(1, 3), Vector2d(1, 2)) in moves_1
    assert Move(Vector2d(1, 3), Vector2d(1, 1)) in moves_1
    assert Move(Vector2d(1, 3), Vector2d(1, 0)) in moves_1
    assert Move(Vector2d(1, 3), Vector2d(0, 2)) in moves_1
    assert Move(Vector2d(1, 3), Vector2d(0, 3)) in moves_1

    assert Move(Vector2d(4, 1), Vector2d(4, 2)) in moves_2
    assert Move(Vector2d(4, 1), Vector2d(4, 3)) in moves_2
    assert Move(Vector2d(4, 1), Vector2d(4, 4)) in moves_2
    assert Move(Vector2d(4, 1), Vector2d(4, 5)) in moves_2
    assert Capturing(Vector2d(4, 1), Vector2d(4, 6)) in moves_2

    assert Capturing(Vector2d(6, 2), Vector2d(7, 3)) in moves_3
    assert Move(Vector2d(6, 2), Vector2d(5, 1)) in moves_3


def test_queen_available_moves_single_checked():
    pieces = [
        Queen(Team.WHITE, Vector2d(2, 2)),
        Queen(Team.WHITE, Vector2d(5, 4)),
        Queen(Team.WHITE, Vector2d(6, 2)),
        King(Team.WHITE, Vector2d(4, 0)),
        Knight(Team.BLACK, Vector2d(2, 3)),
        Bishop(Team.BLACK, Vector2d(7, 3)),
        Rook(Team.BLACK, Vector2d(4, 5)),
        King(Team.BLACK, Vector2d(4, 7))
    ]

    engine = ChessEngine(pieces, [Move(Vector2d(5, 5), Vector2d(4, 5))])

    moves_1 = engine.available_moves(Vector2d(2, 2))
    moves_2 = engine.available_moves(Vector2d(5, 4))
    moves_3 = engine.available_moves(Vector2d(6, 2))

    assert len(moves_1) == 2
    assert len(moves_2) == 3
    assert len(moves_3) == 0

    assert Move(Vector2d(2, 2), Vector2d(4, 4)) in moves_1
    assert Move(Vector2d(2, 2), Vector2d(4, 2)) in moves_1

    assert Capturing(Vector2d(5, 4), Vector2d(4, 5)) in moves_2
    assert Move(Vector2d(5, 4), Vector2d(4, 4)) in moves_2
    assert Move(Vector2d(5, 4), Vector2d(4, 3)) in moves_2


def test_queen_available_moves_double_checked():
    pieces = [
        Queen(Team.WHITE, Vector2d(2, 2)),
        Queen(Team.WHITE, Vector2d(5, 4)),
        King(Team.WHITE, Vector2d(4, 0)),
        Knight(Team.BLACK, Vector2d(2, 3)),
        Knight(Team.BLACK, Vector2d(3, 2)),
        Rook(Team.BLACK, Vector2d(4, 5)),
        King(Team.BLACK, Vector2d(4, 7))
    ]

    engine = ChessEngine(pieces, [Move(Vector2d(4, 4), Vector2d(3, 2))])

    moves_1 = engine.available_moves(Vector2d(2, 2))
    moves_2 = engine.available_moves(Vector2d(5, 4))

    assert len(moves_1) == 0
    assert len(moves_2) == 0


def test_both_castling_available():
    pieces = [
        King(Team.WHITE, Vector2d(4, 0)),
        Rook(Team.BLACK, Vector2d(0, 7), has_moved=False),
        Rook(Team.BLACK, Vector2d(7, 7), has_moved=False),
        King(Team.BLACK, Vector2d(4, 7), has_moved=False)
    ]

    engine = ChessEngine(pieces, [Move(Vector2d(5, 0), Vector2d(4, 0))])

    moves = engine.available_moves(Vector2d(4, 7))

    assert Castling(Vector2d(4, 7), Vector2d(2, 7), Vector2d(0, 7), Vector2d(3, 7)) in moves
    assert Castling(Vector2d(4, 7), Vector2d(6, 7), Vector2d(7, 7), Vector2d(5, 7)) in moves


def test_one_castling_available():
    pieces = [
        King(Team.WHITE, Vector2d(4, 0)),
        Rook(Team.BLACK, Vector2d(0, 7), has_moved=True),
        Rook(Team.BLACK, Vector2d(7, 7), has_moved=False),
        King(Team.BLACK, Vector2d(4, 7), has_moved=False)
    ]

    engine = ChessEngine(pieces, [Move(Vector2d(5, 0), Vector2d(4, 0))])

    moves = engine.available_moves(Vector2d(4, 7))

    assert Castling(Vector2d(4, 7), Vector2d(6, 7), Vector2d(7, 7), Vector2d(5, 7)) in moves
    assert Castling(Vector2d(4, 7), Vector2d(2, 7), Vector2d(0, 7), Vector2d(3, 7)) not in moves


def test_no_castling_available():
    pieces = [
        King(Team.WHITE, Vector2d(4, 0)),
        Rook(Team.BLACK, Vector2d(0, 7), has_moved=False),
        Rook(Team.BLACK, Vector2d(7, 7), has_moved=False),
        King(Team.BLACK, Vector2d(4, 7), has_moved=True)
    ]

    engine = ChessEngine(pieces, [Move(Vector2d(5, 0), Vector2d(4, 0))])

    moves = engine.available_moves(Vector2d(4, 7))

    assert Castling(Vector2d(4, 7), Vector2d(6, 7), Vector2d(7, 7), Vector2d(5, 7)) not in moves
    assert Castling(Vector2d(4, 7), Vector2d(2, 7), Vector2d(0, 7), Vector2d(3, 7)) not in moves


def test_king_available_moves_not_checked():
    pieces = [
        Pawn(Team.WHITE, Vector2d(4, 5)),
        Rook(Team.WHITE, Vector2d(5, 5)),
        King(Team.WHITE, Vector2d(4, 0)),
        Rook(Team.BLACK, Vector2d(0, 7), has_moved=False),
        Rook(Team.BLACK, Vector2d(7, 7), has_moved=False),
        King(Team.BLACK, Vector2d(4, 7), has_moved=False)
    ]

    engine = ChessEngine(pieces, [Move(Vector2d(5, 0), Vector2d(4, 0))])

    moves = engine.available_moves(Vector2d(4, 7))

    assert len(moves) == 3

    assert Move(Vector2d(4, 7), Vector2d(3, 7)) in moves
    assert Move(Vector2d(4, 7), Vector2d(4, 6)) in moves
    assert Castling(Vector2d(4, 7), Vector2d(2, 7), Vector2d(0, 7), Vector2d(3, 7)) in moves


def test_king_available_moves_single_checked():
    pieces = [
        Knight(Team.WHITE, Vector2d(4, 6)),
        Rook(Team.WHITE, Vector2d(5, 6)),
        King(Team.WHITE, Vector2d(4, 0)),
        Queen(Team.WHITE, Vector2d(2, 5)),
        Rook(Team.BLACK, Vector2d(0, 7), has_moved=False),
        Rook(Team.BLACK, Vector2d(7, 7), has_moved=False),
        King(Team.BLACK, Vector2d(4, 7), has_moved=False)
    ]

    engine = ChessEngine(pieces, [Move(Vector2d(2, 4), Vector2d(2, 5))])

    moves = engine.available_moves(Vector2d(4, 7))

    assert len(moves) == 2

    assert Move(Vector2d(4, 7), Vector2d(3, 7)) in moves
    assert Capturing(Vector2d(4, 7), Vector2d(5, 6)) in moves


def test_king_available_moves_double_checked():
    pieces = [
        Rook(Team.WHITE, Vector2d(4, 6)),
        King(Team.WHITE, Vector2d(4, 0)),
        Queen(Team.WHITE, Vector2d(2, 5)),
        Rook(Team.BLACK, Vector2d(0, 7), has_moved=False),
        Rook(Team.BLACK, Vector2d(7, 7), has_moved=False),
        King(Team.BLACK, Vector2d(4, 7), has_moved=False)
    ]

    engine = ChessEngine(pieces, [Capturing(Vector2d(3, 6), Vector2d(4, 6))])

    moves = engine.available_moves(Vector2d(4, 7))

    assert len(moves) == 3

    assert Move(Vector2d(4, 7), Vector2d(3, 7)) in moves
    assert Move(Vector2d(4, 7), Vector2d(5, 7)) in moves
    assert Capturing(Vector2d(4, 7), Vector2d(4, 6)) in moves