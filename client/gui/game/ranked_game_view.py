from tkinter import Tk, Misc
from typing import Callable

from client.connection.auth_service import AuthService
from client.connection.game_room_service import GameRoomService
from client.gui.game.chessboard_visualizer import ChessboardVisualizer
from client.gui.menu.player_component import PlayerComponent
from client.gui.shared import DisplayBoundary
from client.gui.view import View, ViewName


class RankedGameView(View):
    def __init__(self, root: Tk, display: DisplayBoundary, navigate: Callable[[ViewName], None],
                 auth_service: AuthService, player_component: PlayerComponent, game_room_service: GameRoomService):
        super().__init__(root, display, navigate, auth_service, player_component)

        self.chessboard_visualizer = ChessboardVisualizer(root, display)

    def reset(self):
        pass

    def show(self):
        Misc.tkraise(self.chessboard_visualizer.canvas)
