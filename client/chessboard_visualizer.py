from tkinter import *
from PIL import Image, ImageTk
import os

from shared.piece import Team, PieceType
from shared.chess_engine import ChessEngine


class ChessboardVisualizer:
    def __init__(self, master):
        self.board_size = 800
        self.field_size = 100
        self.piece_size = 80

        self.width = 840
        self.height = 840

        self.margin = 20
        self.field_margin = 10

        self.pieces: dict[Team, dict[PieceType, ImageTk.PhotoImage]] = {Team.WHITE: {}, Team.BLACK: {}}

        self.root = Canvas(master, width=self.width, height=self.height)
        self.root.pack()

        self.chess_engine = ChessEngine()

        self.import_pieces()
        self.set_fields()
        self.set_pieces()

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

    def set_fields(self):
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

                self.root.create_rectangle(self.margin + column * self.field_size,
                                           self.margin + self.board_size - row * self.field_size,
                                           self.margin + (column + 1) * self.field_size,
                                           self.margin + self.board_size - (row + 1) * self.field_size,
                                           fill=square_color)

    def set_pieces(self):
        """
        Places pieces on the chessboard in their initial positions for both teams
        :return:
        """

        for team in [Team.WHITE, Team.BLACK]:
            for piece in self.chess_engine.board.pieces[team].all:
                self.root.create_image(self.margin + self.field_margin + piece.position.x * 100,
                                       self.margin + self.field_margin + self.board_size - (piece.position.y + 1) * 100,
                                       image=self.pieces[team][piece.type], anchor=NW)
