from tkinter import Tk, Misc, Frame
from typing import Callable

from client.connection.auth_service import AuthService
from client.connection.game_room_service import GameRoomService
from client.gui.game.chessboard_visualizer import ChessboardVisualizer
from client.gui.game.game_menu import game_menu
from client.gui.menu.player_component import PlayerComponent
from client.gui.shared import DisplayBoundary
from client.gui.view import View, ViewName


class RankedGameView(View):
    def __init__(self, root: Tk, display: DisplayBoundary, navigate: Callable[[ViewName], None],
                 auth_service: AuthService, game_room_service: GameRoomService):
        super().__init__(root, display, navigate, auth_service)

        self.chessboard_visualizer = ChessboardVisualizer(root, display)
        self.game_room_service = game_room_service
        self.game_menu = game_menu(root, display)

    def reset(self):
        pass

    def show(self):
        self.chessboard_visualizer.table.tkraise()
        self.game_menu.tkraise()
