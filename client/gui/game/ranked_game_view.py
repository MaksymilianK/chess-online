from typing import Callable, Optional

from tkinter import Tk, NORMAL, DISABLED

from client.connection.auth_service import AuthService
from client.connection.game_room_service import GameRoomService, RankedGameRoom
from client.gui.game.chessboard_visualizer import ChessboardVisualizer
from client.gui.game.game_menu import game_menu
from client.gui.game.player import PlayerTeam
from client.gui.shared import DisplayBoundary, PrimaryButton
from client.gui.view import View, ViewName
from shared.chess_engine.piece import Team


class RankedGameView(View):
    def __init__(self, root: Tk, display: DisplayBoundary, navigate: Callable[[ViewName], None],
                 auth_service: AuthService, game_room_service: GameRoomService):
        super().__init__(root, display, navigate, auth_service)

        self.chessboard_visualizer = ChessboardVisualizer(root, display, game_room_service)
        self.game_room_service = game_room_service

        self.game_menu = game_menu(root, display)
        for col in range(6):
            self.game_menu.columnconfigure(col, weight=1)
        for row in range(4):
            self.game_menu.rowconfigure(row, weight=1)

        self.room: Optional[RankedGameRoom] = None

        self.player2 = PlayerTeam(self.game_menu)
        self.player2.frame.grid(column=0, row=0, columnspan=3, sticky="N")

        self.player1 = PlayerTeam(self.game_menu)
        self.player1.frame.grid(column=3, row=0, columnspan=3, sticky="N")

        self.surrender_btn = PrimaryButton(self.game_menu, text="Surrender", command=self.surrender)
        self.surrender_btn.grid(column=0, row=1, columnspan=3)

        self.claim_draw_btn = PrimaryButton(self.game_menu, text="Claim draw", command=self.claim_draw)
        self.claim_draw_btn.grid(column=3, row=1, columnspan=3)

        self.offer_draw_btn = PrimaryButton(self.game_menu, text="Offer draw", command=self.offer_draw)
        self.offer_draw_btn.grid(column=0, row=2, columnspan=6)

        self.accept_draw_btn = PrimaryButton(self.game_menu, text="Accept draw",
                                             command=lambda: self.respond_to_draw_offer(True))
        self.accept_draw_btn.grid(column=0, row=3, columnspan=3)
        self.reject_draw_btn = PrimaryButton(self.game_menu, text="Reject draw",
                                             command=lambda: self.respond_to_draw_offer(False))
        self.reject_draw_btn.grid(column=3, row=3, columnspan=3)

        self.reset()

    def update_menu(self):
        self.surrender_btn["state"] = NORMAL if self.game_room_service.can_surrender() else DISABLED
        self.claim_draw_btn["state"] = NORMAL if self.game_room_service.can_claim_draw() else DISABLED
        self.offer_draw_btn["state"] = NORMAL if self.game_room_service.can_offer_draw() else DISABLED
        respond_to_draw_offer_state = NORMAL if self.game_room_service.can_respond_to_draw_offer() else DISABLED
        self.accept_draw_btn["state"] = respond_to_draw_offer_state
        self.reject_draw_btn["state"] = respond_to_draw_offer_state

    def surrender(self):
        self.game_room_service.game_surrender()

    def claim_draw(self):
        self.game_room_service.game_claim_draw()

    def offer_draw(self):
        self.game_room_service.game_offer_draw()

    def respond_to_draw_offer(self, accepted: bool):
        self.game_room_service.game_respond_to_draw_offer(accepted)

    def on_game_surrender(self):
        self.game_room_service.on_game_surrender()
        self.navigate(ViewName.JOIN_RANKED)

    def on_game_offer_draw(self):
        self.game_room_service.on_game_offer_draw()
        self.update_menu()

    def on_game_respond_to_draw_offer(self, message: dict):
        self.game_room_service.on_game_respond_to_draw_offer(message)
        self.update_menu()
        if not self.room.running:
            self.navigate(ViewName.JOIN_RANKED)

    def on_game_claim_draw(self):
        self.game_room_service.on_game_claim_draw()
        self.navigate(ViewName.JOIN_RANKED)

    def on_game_move(self, message: dict):
        move = self.game_room_service.on_game_move(message)
        self.update_menu()
        self.chessboard_visualizer.process_move(move)
        if self.room.engine.currently_moving_team == self.room.teams[self.room.players[0]]:
            self.player2.update_time(self.room.times[self.room.teams[self.room.players[1]]])
            self.player2.update_timer_lbl()
            self.player1.start_counting()
        else:
            self.player1.update_time(self.room.times[self.room.teams[self.room.players[0]]])
            self.player1.update_timer_lbl()
            self.player2.start_counting()

    def on_game_time_end(self):
        self.game_room_service.on_game_time_end()
        self.update_menu()
        self.navigate(ViewName.JOIN_RANKED)

    def reset(self):
        self.room = None
        self.player1.reset()
        self.player2.reset()
        self.surrender_btn["state"] = DISABLED
        self.claim_draw_btn["state"] = DISABLED
        self.offer_draw_btn["state"] = DISABLED
        self.accept_draw_btn["state"] = DISABLED
        self.reject_draw_btn["state"] = DISABLED
        self.chessboard_visualizer.reset()

    def show(self):
        self.room = self.game_room_service.room
        self.player1.nick_lbl["text"] = self.room.players[0].nick
        self.player2.nick_lbl["text"] = self.room.players[1].nick

        self.update_menu()
        self.chessboard_visualizer.start()

        if self.room.teams[self.room.players[0]] == Team.WHITE:
            self.player1.team_lbl["image"] = self.player1.white_img
            self.player2.team_lbl["image"] = self.player2.black_img
        else:
            self.player1.team_lbl["image"] = self.player1.black_img
            self.player2.team_lbl["image"] = self.player2.white_img

        self.player1.update_time(self.room.times[self.room.teams[self.room.players[0]]])
        self.player2.update_time(self.room.times[self.room.teams[self.room.players[1]]])
        if self.room.engine.currently_moving_team == self.room.teams[self.room.players[0]]:
            self.player1.update_time(30 * 1000)
            self.player1.start_counting()
        else:
            self.player2.update_time(30 * 1000)
            self.player2.start_counting()

        self.chessboard_visualizer.table.tkraise()
        self.game_menu.tkraise()
