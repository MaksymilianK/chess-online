from typing import Optional

from tkinter import *
from PIL import Image, ImageTk
import os
import platform

if platform.system() == "Darwin":
    from tkmacosx import Button

from shared.position import Vector2d
from shared.piece import Team, PieceType, Piece
from shared.move import AbstractMove, MoveType
from shared.chess_engine import ChessEngine


class ChessboardVisualizer:
    def __init__(self, root):
        self.margin = 20
        self.field_margin = 10

        self.piece_size = 80
        self.field_size = self.piece_size + 2 * self.field_margin
        self.board_size = 8 * self.field_size

        self.width = self.board_size + 2 * self.margin
        self.height = self.board_size + 2 * self.margin

        self.root = root
        self.root.title("Chessboard")
        self.root.geometry(f"{self.width}x{self.height}")

        self.pieces: dict[Team, dict[PieceType, ImageTk.PhotoImage]] = {Team.WHITE: {}, Team.BLACK: {}}

        self._fields: dict[Vector2d, int] = {Vector2d(i, j): None for i in range(8) for j in range(8)}
        self._currently_available_moves: [int] = []
        self._selected_piece: Optional[Vector2d] = None
        self._promotion_piece: Optional[PieceType] = None

        self.menu = None

        self.canvas_size = self.board_size + 2 * self.margin

        self.canvas = Canvas(root, width=self.canvas_size, height=self.canvas_size)
        self.canvas.place(x=0, y=0)

        self.chess_engine = ChessEngine()
        self.init_board()
        self.canvas.bind("<Button-1>", self.handle_canvas_click_event)

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
        path_to_team = {"./img/white/": Team.WHITE, "./img/black/": Team.BLACK}

        for path in ["./img/white/", "./img/black/"]:
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
            x = self.margin + field_center + available_move.position_to.x * self.field_size
            y = self.margin + field_center + self.board_size - (available_move.position_to.y + 1) * self.field_size
            self.set_available_move(x, y, radius)

    def display_promotion_menu(self, team: Team):
        """
        Shows up the menu to choose what piece to promote the pawn to
        :param team:
        :return:
        """

        self.menu = Toplevel()
        self.menu.title("Choose what to promote your pawn to")

        canvas = Canvas(self.menu, width=420, height=140)
        canvas.pack()

        canvas.create_image(20, 20, image=self.pieces[team][PieceType.BISHOP], anchor=NW)
        canvas.create_image(120, 20, image=self.pieces[team][PieceType.KNIGHT], anchor=NW)
        canvas.create_image(220, 20, image=self.pieces[team][PieceType.ROOK], anchor=NW)
        canvas.create_image(320, 20, image=self.pieces[team][PieceType.QUEEN], anchor=NW)

        canvas.bind("<Button-1>", self.handle_promotion_menu_click_event)

        self.menu.mainloop()

    def field_coords(self, pos: Vector2d) -> Optional[Vector2d]:
        if self.margin < pos.x < self.margin + self.board_size and self.margin < pos.y < self.margin + self.board_size:
            coords = (pos - Vector2d(self.margin, self.margin)) // self.field_size
            return Vector2d(coords.x, 7 - coords.y)
        return None

    def handle_promotion_menu_click_event(self, event: EventType):
        if 20 < event.x < 100 and 20 < event.y < 100:
            self._promotion_piece = PieceType.BISHOP
            self.menu.destroy()
        elif 120 < event.x < 200 and 20 < event.y < 100:
            self._promotion_piece = PieceType.KNIGHT
            self.menu.destroy()
        elif 220 < event.x < 300 and 20 < event.y < 100:
            self._promotion_piece = PieceType.ROOK
            self.menu.destroy()
        elif 320 < event.x < 400 and 20 < event.y < 100:
            self._promotion_piece = PieceType.QUEEN
            self.menu.destroy()

    def handle_canvas_click_event(self, event: EventType):
        position = self.field_coords(Vector2d(event.x, event.y))

        if not position:
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

    def process_move(self, move: AbstractMove):
        if not self.chess_engine.validate_move(move):
            return

        if move.type == MoveType.PROMOTION or move.type == MoveType.PROMOTION_WITH_CAPTURING:
            self.display_promotion_menu(self.chess_engine.board.piece_at(move.position_from).team)
            move.piece_type = self._promotion_piece
        self.chess_engine.process_move(move)

        self.clear_available_moves()

        if move.type == MoveType.CAPTURING:
            self.remove_piece(move.position_to)
        elif move.type == MoveType.CASTLING:
            self.move_piece(move.rook_from, move.rook_to)
        elif move.type == MoveType.EN_PASSANT:
            self.remove_piece(move.captured_position)

        if move.type == MoveType.PROMOTION:
            self.remove_piece(move.position_from)
            self.set_piece(self.chess_engine.board.piece_at(move.position_to))
        elif move.type == MoveType.PROMOTION_WITH_CAPTURING:
            self.remove_piece(move.position_to)
            self.remove_piece(move.position_from)
            self.set_piece(self.chess_engine.board.piece_at(move.position_to))
        else:
            self.move_piece(move.position_from, move.position_to)

    def set_piece(self, piece: Piece):
        self._fields[piece.position] = self.canvas.create_image(
            self.margin + self.field_margin + piece.position.x * self.field_size,
            self.margin + self.field_margin + self.board_size - (piece.position.y + 1) * self.field_size,
            image=self.pieces[piece.team][piece.type], anchor=NW
        )

    def set_field(self, row, column, color):
        self.canvas.create_rectangle(
            self.margin + column * self.field_size,
            self.margin + self.board_size - row * self.field_size,
            self.margin + (column + 1) * self.field_size,
            self.margin + self.board_size - (row + 1) * self.field_size,
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
