from typing import Optional

from shared.chessboard import Piece, Chessboard, on_same_line, on_same_row, within_board, \
    is_between, SECOND_RANK, FIRST_RANK, on_same_diagonal, unit_vector_to
from shared.move import AbstractMove, Move, EnPassant, Capturing, Promotion, PromotionWithCapturing, Castling
from shared.position import Vector2d, distance_y
from shared.piece import Team, Pawn, Knight, King, PieceType, Bishop, Rook, Queen


class CheckStatus:
    def __init__(self):
        self.checking_piece_1: Optional[Piece] = None
        self.checking_piece_2: Optional[Piece] = None

    def update_checking_pieces(self, checking_piece_1: Piece = None, checking_piece_2: Piece = None):
        self.checking_piece_1 = checking_piece_1
        self.checking_piece_2 = checking_piece_2

    @property
    def checked(self) -> bool:
        return self.checking_piece_1 is not None

    @property
    def double_checked(self):
        return self.checking_piece_1 is not None and self.checking_piece_2 is not None


class MoveHistory:
    def __init__(self, moves: list[AbstractMove] = None):
        self.moves: list[AbstractMove] = moves or []

    @property
    def last_move(self) -> Optional[AbstractMove]:
        return None if len(self.moves) == 0 else self.moves[-1]


class ChessEngine:
    def __init__(self, pieces: list[Piece] = None, move_history: list[AbstractMove] = None):
        self.move_history = MoveHistory(move_history)
        self.board = Chessboard(pieces or _init_pieces())
        self.currently_moving_team = self._init_currently_moving_team()
        self.check_status = self._init_check_status()

    def available_moves(self, piece_at: Vector2d) -> list[AbstractMove]:
        piece = self.board.piece_at(piece_at)
        if piece is None:
            raise Exception("Cannot move a piece at the specified field, because the piece is not there")

        if not piece.team == self.currently_moving_team:
            raise Exception("Cannot move a piece of the opponent's team")

        if self.check_status.double_checked and piece.type != PieceType.KING:
            return []

        if piece.type == PieceType.PAWN:
            return self._available_pawn_moves(piece)
        elif piece.type == PieceType.KNIGHT:
            return self._available_knight_moves(piece)
        elif piece.type == PieceType.KING:
            return self._available_king_moves(piece)
        else:
            return self._available_other_pieces_moves(piece)

    def _init_currently_moving_team(self) -> Team:
        if self.move_history.last_move:
            last_moving_team = self._last_moving_piece().team
            return Team.WHITE if last_moving_team == Team.BLACK else Team.BLACK
        else:
            return Team.WHITE

    def _init_check_status(self) -> CheckStatus:
        check_status = CheckStatus()
        checking_pieces = self._checking_pieces()
        if len(checking_pieces) == 1:
            check_status.update_checking_pieces(checking_pieces[0])
        elif len(checking_pieces) == 2:
            check_status.update_checking_pieces(checking_pieces[0], checking_pieces[1])

        return check_status

    def _checking_pieces(self) -> list[Piece]:
        checking_pieces: list[Piece] = []
        king_pos = self.board.pieces[self.currently_moving_team].king.position

        for move_vector in Knight.moves:
            other_pos = king_pos - move_vector
            if within_board(other_pos):
                other_piece = self.board.piece_at(other_pos)
                if other_piece and other_piece.type == PieceType.KNIGHT \
                        and other_piece.team != self.currently_moving_team:
                    checking_pieces.append(other_piece)

        for move_vector in Pawn.moves[self._currently_opposite_team()]:
            other_pos = king_pos - move_vector
            if within_board(other_pos):
                other_piece = self.board.piece_at(other_pos)
                if other_piece and other_piece.type == PieceType.PAWN \
                        and other_piece.team != self.currently_moving_team:
                    checking_pieces.append(other_piece)

        for move_vector in Bishop.moves:
            other_pos = king_pos - move_vector
            while within_board(other_pos):
                other_piece = self.board.piece_at(other_pos)
                if other_piece:
                    if other_piece.type in (PieceType.BISHOP, PieceType.QUEEN) \
                            and other_piece.team != self.currently_moving_team:
                        checking_pieces.append(other_piece)
                    break
                other_pos -= move_vector

        for move_vector in Rook.moves:
            other_pos = king_pos - move_vector
            while within_board(other_pos):
                other_piece = self.board.piece_at(other_pos)
                if other_piece:
                    if other_piece.type in (PieceType.ROOK, PieceType.QUEEN) \
                            and other_piece.team != self.currently_moving_team:
                        checking_pieces.append(other_piece)
                    break
                other_pos -= move_vector

        return checking_pieces

    def _available_pawn_moves(self, pawn: Pawn) -> list[AbstractMove]:
        available_moves: list[AbstractMove] = []
        small_move_pos = pawn.position + pawn.move_vectors[0]

        if within_board(small_move_pos) and not self._will_move_reveal_king(pawn.position, small_move_pos) \
                and not self.board.piece_at(small_move_pos):
            if not self.check_status.checked or self._will_move_cover_king(small_move_pos):
                if pawn.position.y == SECOND_RANK[self._currently_opposite_team()]:
                    available_moves.append(Promotion(pawn.position, small_move_pos))
                else:
                    available_moves.append(Move(pawn.position, small_move_pos))

            big_move_pos = small_move_pos + pawn.move_vectors[0]
            if not pawn.has_moved and not self.board.piece_at(big_move_pos) \
                    and (not self.check_status.checked or self._will_move_cover_king(big_move_pos)):
                available_moves.append(Move(pawn.position, big_move_pos))

        for attack_vector in pawn.attack_vectors:
            attack_pos = pawn.position + attack_vector

            if not within_board(attack_pos) or self._will_move_reveal_king(pawn.position, attack_pos) \
                    or (self.check_status.checked and not self._will_capture_checking_piece(attack_pos)):
                continue

            if self.board.piece_at(attack_pos) and self.board.piece_at(attack_pos).team != self.currently_moving_team:
                if pawn.position.y == SECOND_RANK[self._currently_opposite_team()]:
                    available_moves.append(PromotionWithCapturing(pawn.position, attack_pos))
                else:
                    available_moves.append(Capturing(pawn.position, attack_pos))
            elif self._last_moving_piece() and self._last_moving_piece().type == PieceType.PAWN and distance_y(
                    self.move_history.last_move.position_from, self.move_history.last_move.position_to) == 2 \
                    and self.move_history.last_move.position_to.x == attack_pos.x:
                available_moves.append(EnPassant(pawn.position, attack_pos, self.move_history.last_move.position_to))

        return available_moves

    def _available_knight_moves(self, knight: Knight) -> list[AbstractMove]:
        available_moves: list[AbstractMove] = []

        for move_vector in knight.move_vectors:
            new_pos = knight.position + move_vector
            if not within_board(new_pos):
                continue
            elif self._will_move_reveal_king(knight.position, new_pos):
                continue
            elif self.check_status.checked and not self._will_move_cover_king(new_pos) \
                    and not self._will_capture_checking_piece(new_pos):
                continue
            elif self.board.piece_at(new_pos) and self.board.piece_at(new_pos).team == self.currently_moving_team:
                continue

            if self.board.piece_at(new_pos):
                available_moves.append(Capturing(knight.position, new_pos))
            else:
                available_moves.append(Move(knight.position, new_pos))

        return available_moves

    def _available_king_moves(self, king: King):
        available_moves: list[AbstractMove] = []
        attacked_fields = self._attacked_fields()

        for move_vector in king.move_vectors:
            new_pos = king.position + move_vector
            if not within_board(new_pos) or (self.board.piece_at(new_pos)
                                             and self.board.piece_at(new_pos).team == self.currently_moving_team):
                continue
            elif new_pos in attacked_fields:
                continue

            if self.board.piece_at(new_pos):
                available_moves.append(Capturing(king.position, new_pos))
            else:
                available_moves.append(Move(king.position, new_pos))

        if king.has_moved or self.check_status.checked:
            return available_moves

        rooks = self.board.pieces[self.currently_moving_team].rooks
        for rook in rooks:
            if rook.has_moved or self.board.any_piece_between(king.position, rook.position):
                continue

            unit_vector = unit_vector_to(king.position, rook.position)
            new_rook_pos = king.position + unit_vector
            new_king_pos = king.position + (2 * unit_vector)
            if new_rook_pos in attacked_fields or new_king_pos in attacked_fields:
                continue

            available_moves.append(Castling(king.position, new_king_pos, rook.position, new_rook_pos))

        return available_moves

    def _available_other_pieces_moves(self, piece: Piece) -> list[AbstractMove]:
        available_moves: list[AbstractMove] = []

        for move_vector in piece.move_vectors:
            new_pos = piece.position + move_vector
            if not within_board(new_pos) or self._will_move_reveal_king(piece.position, new_pos):
                continue

            while within_board(new_pos):
                if self.check_status.checked and not self._will_move_cover_king(new_pos) \
                        and not self._will_capture_checking_piece(new_pos):
                    new_pos += move_vector
                    continue

                if self.board.piece_at(new_pos):
                    if self.board.piece_at(new_pos).team != self.currently_moving_team:
                        available_moves.append(Capturing(piece.position, new_pos))
                    break

                available_moves.append(Move(piece.position, new_pos))
                new_pos += move_vector

        return available_moves

    def _currently_opposite_team(self):
        return Team.WHITE if self.currently_moving_team == Team.BLACK else Team.BLACK

    def _current_king_position(self):
        return self.board.pieces[self.currently_moving_team].king.position

    def _will_move_cover_king(self, pos_to: Vector2d) -> bool:
        return self.check_status.checking_piece_1.type != PieceType.KNIGHT \
               and on_same_line(pos_to, self._current_king_position(), self.check_status.checking_piece_1.position) \
               and is_between(pos_to, self._current_king_position(), self.check_status.checking_piece_1.position)

    def _will_capture_checking_piece(self, attack_pos: Vector2d) -> bool:
        return self.check_status.checking_piece_1.position == attack_pos

    def _will_move_reveal_king(self, pos_from: Vector2d, pos_to: Vector2d):
        king_pos = self._current_king_position()

        if not on_same_line(king_pos, pos_from) or on_same_line(king_pos, pos_from, pos_to):
            return False

        revealed_piece = self.board.next_piece_on_line(king_pos, pos_from)
        if not revealed_piece:
            return False

        if revealed_piece.type is PieceType.QUEEN:
            return True

        if (on_same_row(king_pos, pos_from) and revealed_piece.type is PieceType.ROOK) \
                or (on_same_diagonal(king_pos, pos_from) and revealed_piece.type is PieceType.BISHOP):
            return True
        else:
            return False

    def _attacked_fields(self) -> set[Vector2d]:
        attacked_fields: set[Vector2d] = set()
        opponent_pieces = self.board.pieces[self._currently_opposite_team()]

        for piece in opponent_pieces.pawns:
            for attack_vector in piece.attack_vectors:
                new_pos = piece.position + attack_vector
                if within_board(new_pos) and not self.board.piece_at(new_pos):
                    attacked_fields.add(new_pos)

        for piece in opponent_pieces.knights + [opponent_pieces.king]:
            for move_vector in piece.move_vectors:
                new_pos = piece.position + move_vector
                if within_board(new_pos) and not self.board.piece_at(new_pos):
                    attacked_fields.add(new_pos)

        for piece in opponent_pieces.bishops + opponent_pieces.rooks + opponent_pieces.queens:
            for move_vector in piece.move_vectors:
                new_pos = piece.position + move_vector
                while within_board(new_pos):
                    attacked_fields.add(new_pos)
                    piece_at = self.board.piece_at(new_pos)
                    if piece_at and piece_at.team == self.currently_moving_team and piece_at.type != PieceType.KING:
                        break
                    new_pos += move_vector

        return attacked_fields

    def _last_moving_piece(self) -> Optional[Piece]:
        if self.move_history.last_move:
            return self.board.piece_at(self.move_history.last_move.position_to)
        else:
            return None


def _init_pieces() -> list[Piece]:
    pieces: list[Piece] = []

    for team in (Team.WHITE, Team.BLACK):
        for i in range(8):
            pieces.append(Pawn(team, Vector2d(i, SECOND_RANK[team])))

        pieces.append(Knight(team, Vector2d(1, FIRST_RANK[team])))
        pieces.append(Knight(team, Vector2d(6, FIRST_RANK[team])))

        pieces.append(Bishop(team, Vector2d(2, FIRST_RANK[team])))
        pieces.append(Bishop(team, Vector2d(5, FIRST_RANK[team])))

        pieces.append(Rook(team, Vector2d(0, FIRST_RANK[team])))
        pieces.append(Rook(team, Vector2d(7, FIRST_RANK[team])))

        pieces.append(Queen(team, Vector2d(3, FIRST_RANK[team])))

        pieces.append(King(team, Vector2d(4, FIRST_RANK[team])))

    return pieces
