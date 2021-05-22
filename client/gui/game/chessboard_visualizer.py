from typing import Optional

from tkinter import *
from PIL import Image, ImageTk
import os
import platform

from client.gui.shared import DisplayBoundary
from shared.chess_engine.chess_engine import ChessEngine
from shared.chess_engine.move import Promotion, MoveType, AbstractMove
from shared.chess_engine.piece import Team, PieceType, Piece
from shared.chess_engine.position import Vector2d

if platform.system() == "Darwin":
    from tkmacosx import Button


class ChessboardVisualizer:
    def __init__(self, root: Tk, display: DisplayBoundary):
        self.root = root
        self.display = display

        self.table = Frame(self.root, bg="#222222")
        self.table_size = 8 / 9 * display.height
        self.table.place(x=display.x + 1 / 16 * display.width, y=display.y + 0.5 / 9 * display.height,
                         width=self.table_size, height=self.table_size)

        self.board_margin = 10
        self.board_size = round(self.table_size - 2 * self.board_margin)
        while self.board_size % 8 != 0:
            self.board_size -= 1
        self.field_size = self.board_size // 8

        self.field_padding = round(0.05 * self.field_size)
        self.piece_size = self.field_size - 2 * self.field_padding

        self.pieces: dict[Team, dict[PieceType, ImageTk.PhotoImage]] = {Team.WHITE: {}, Team.BLACK: {}}

        self._fields: dict[Vector2d, int] = {Vector2d(i, j): None for i in range(8) for j in range(8)}
        self._currently_available_moves: [int] = []
        self._selected_piece: Optional[Vector2d] = None
        self._promotion_move: Optional[Promotion] = None

        self.menu = None

        self.promotion_menu_pieces = {0: PieceType.KNIGHT, 1: PieceType.BISHOP, 2: PieceType.ROOK, 3: PieceType.QUEEN}

        self.chess_engine = ChessEngine()
        self.canvas = Canvas(self.table, width=self.board_size, height=self.board_size, borderwidth=0,
                             highlightthickness=0)
        self.canvas.place(x=self.board_margin, y=self.board_margin)
        self.init_board()

        self.canvas.bind("<Button-1>", self.handle_canvas_click_event)
        self.promotion_menu = self.init_promotion_menu()

    def init_board(self):
        self.import_pieces()
        self.init_fields()
        self.init_pieces()

    def import_pieces(self):
        """
        Imports images of pieces for both teams
        :return:
        """

        file_to_piece_type = {"king.png": PieceType.KING, "queen.png": PieceType.QUEEN, "knight.png": PieceType.KNIGHT,
                              "bishop.png": PieceType.BISHOP, "rook.png": PieceType.ROOK, "pawn.png": PieceType.PAWN}
        path_to_team = {"client/img/white/": Team.WHITE, "client/img/black/": Team.BLACK}

        for path in ["client/img/white/", "client/img/black/"]:
            files = os.listdir(path)
            for file in files:
                img = Image.open(path + file)
                img = img.resize((self.piece_size, self.piece_size), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(image=img)
                self.pieces[path_to_team[path]][file_to_piece_type[file]] = img

    def init_fields(self):
        """
        Fills frame with rectangles representing chessboard fields
        :return:
        """

        for row in range(8):
            for column in range(8):
                if row % 2 == column % 2:
                    square_color = "tan4"
                else:
                    square_color = "burlywood1"
                self.set_field(row, column, square_color)

    def init_pieces(self):
        """
        Places pieces on the chessboard in their initial positions for both teams
        :return:
        """

        for team in [Team.WHITE, Team.BLACK]:
            for piece in self.chess_engine.board.pieces[team].all:
                self.set_piece(piece)

    def clear_available_moves(self):
        for currently_available_move in self._currently_available_moves:
            self.canvas.delete(currently_available_move)
        self._currently_available_moves = []

    def display_available_moves(self, piece_at: Vector2d):
        radius = 10
        field_center = self.field_size // 2

        self.clear_available_moves()
        for available_move in self.chess_engine.available_moves(piece_at):
            x = field_center + available_move.position_to.x * self.field_size
            y = field_center + self.board_size - (available_move.position_to.y + 1) * self.field_size
            self.set_available_move(x, y, radius)

    def init_promotion_menu(self):
        team = self.chess_engine.currently_moving_team

        promotion_menu = Frame(self.root, bg="#000000")
        promotion_menu.place(x=self.display.x + self.board_margin + 2 * self.field_size,
                             y=self.display.y + self.board_margin + 1.5 * self.field_size,
                             width=2 * self.field_padding + 4 * self.piece_size,
                             height=2 * self.field_padding + self.piece_size)

        canvas = Canvas(promotion_menu, width=4 * self.piece_size, height=self.piece_size,
                        borderwidth=0, highlightthickness=0)
        canvas.place(x=self.field_padding, y=self.field_padding)

        for i, piece_type in self.promotion_menu_pieces.items():
            canvas.create_image(self.piece_size * i, 0, image=self.pieces[team][piece_type], anchor=NW)

        canvas.bind("<Button-1>", self.handle_promotion_menu_click)
        return promotion_menu

    def display_promotion_menu(self):
        self.promotion_menu.tkraise()

    def handle_promotion_menu_click(self, event: EventType):
        self._promotion_move.piece_type = self.promotion_menu_pieces[event.x // self.piece_size]
        self.process_promotion()

    def field_coords(self, pos: Vector2d) -> Optional[Vector2d]:
        coords = (pos // self.field_size)
        return Vector2d(coords.x, 7 - coords.y)

    def handle_canvas_click_event(self, event: EventType):
        position = self.field_coords(Vector2d(event.x, event.y))

        if not position or self._promotion_move:
            return

        if self._selected_piece:
            if position == self._selected_piece:
                self.clear_available_moves()
                self._selected_piece = None
            elif self._fields[position] and self.chess_engine.board.piece_at(
                    position).team == self.chess_engine.currently_moving_team:
                self._selected_piece = position
                self.display_available_moves(position)
            else:
                move = self.get_move(self._selected_piece, position)
                if move:
                    self.process_move(move)
                else:
                    self.clear_available_moves()
                    self._selected_piece = None
        else:
            self.display_available_moves(position)
            if self._currently_available_moves:
                self._selected_piece = position

    def get_move(self, pos_from, pos_to) -> Optional[AbstractMove]:
        for move in self.chess_engine.available_moves(pos_from):
            if move.position_to == pos_to:
                return move
        return None

    def process_promotion(self):
        self.chess_engine.process_move(self._promotion_move)
        self.clear_available_moves()

        if self._promotion_move.type == MoveType.PROMOTION:
            self.remove_piece(self._promotion_move.position_from)
            self.set_piece(self.chess_engine.board.piece_at(self._promotion_move.position_to))
        elif self._promotion_move.type == MoveType.PROMOTION_WITH_CAPTURING:
            self.remove_piece(self._promotion_move.position_to)
            self.remove_piece(self._promotion_move.position_from)
            self.set_piece(self.chess_engine.board.piece_at(self._promotion_move.position_to))

        self._promotion_move = None
        self.table.tkraise()

    def process_move(self, move: AbstractMove):
        if not self.chess_engine.validate_move(move):
            return

        if move.type == MoveType.PROMOTION or move.type == MoveType.PROMOTION_WITH_CAPTURING:
            self._promotion_move = move
            self.display_promotion_menu()
            return

        self.chess_engine.process_move(move)
        self.clear_available_moves()

        if move.type == MoveType.CAPTURING:
            self.remove_piece(move.position_to)
        elif move.type == MoveType.CASTLING:
            self.move_piece(move.rook_from, move.rook_to)
        elif move.type == MoveType.EN_PASSANT:
            self.remove_piece(move.captured_position)

        self.move_piece(move.position_from, move.position_to)

    def set_piece(self, piece: Piece):
        self._fields[piece.position] = self.canvas.create_image(
            self.field_padding + piece.position.x * self.field_size,
            self.field_padding + self.board_size - (piece.position.y + 1) * self.field_size,
            image=self.pieces[piece.team][piece.type], anchor=NW
        )

    def set_field(self, row, column, color):
        self.canvas.create_rectangle(
            column * self.field_size,
            self.board_size - row * self.field_size,
            (column + 1) * self.field_size,
            self.board_size - (row + 1) * self.field_size,
            fill=color
        )

    def set_available_move(self, x, y, radius):
        self._currently_available_moves.append(
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="wheat4", width=0)
        )

    def remove_piece(self, position: Vector2d):
        self.canvas.delete(self._fields[position])
        self._fields[position] = None

    def move_piece(self, pos_from: Vector2d, pos_to: Vector2d):
        piece = self.chess_engine.board.piece_at(pos_to)
        self.remove_piece(pos_from)
        self.set_piece(piece)
