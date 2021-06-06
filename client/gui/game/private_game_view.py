from typing import Callable, Optional

from tkinter import Tk, Label, messagebox, NORMAL, DISABLED

from client.connection.auth_service import AuthService
from client.connection.game_room_service import GameRoomService, PrivateGameRoom
from client.gui.game.chessboard_visualizer import ChessboardVisualizer
from client.gui.game.game_menu import game_menu
from client.gui.game.player import PlayerTeam
from client.gui.shared import DisplayBoundary, PrimaryButton, SecondaryButton
from client.gui.view import View, ViewName
from shared.chess_engine.piece import Team
from shared.game.game_type import GameType


class PrivateGameView(View):
    def __init__(self, root: Tk, display: DisplayBoundary, navigate: Callable[[ViewName], None],
                 auth_service: AuthService, game_room_service: GameRoomService):
        super().__init__(root, display, navigate, auth_service)

        self.chessboard_visualizer = ChessboardVisualizer(root, display, game_room_service)
        self.game_room_service = game_room_service

        self.game_menu = game_menu(root, display)
        for col in range(6):
            self.game_menu.columnconfigure(col, weight=1)
        for row in range(9):
            self.game_menu.rowconfigure(row, weight=1)

        self.room: Optional[PrivateGameRoom] = None

        self.host = PlayerTeam(self.game_menu)
        self.guest = PlayerTeam(self.game_menu)

        self.access_key_lbl = Label(self.game_menu, text="", font=("Times New Roman", 16, "bold"))
        self.access_key_lbl.grid(column=0, row=1, columnspan=6)

        self.start_game_lbl = Label(self.game_menu, text="Start game", font=("Times New Roman", 16, "bold"), pady=20)
        self.start_game_lbl.grid(column=0, row=2, columnspan=6, sticky="S")

        self.start_classic_btn = PrimaryButton(self.game_menu, text="Classic",
                                               command=lambda: self.start_game(GameType.CLASSIC))
        self.start_classic_btn.grid(column=0, row=3, columnspan=2, sticky="N")
        self.start_rapid_btn = PrimaryButton(self.game_menu, text="Rapid",
                                             command=lambda: self.start_game(GameType.RAPID))
        self.start_rapid_btn.grid(column=2, row=3, columnspan=2, sticky="N")
        self.start_blitz_btn = PrimaryButton(self.game_menu, text="Blitz",
                                             command=lambda: self.start_game(GameType.BLITZ))
        self.start_blitz_btn.grid(column=4, row=3, columnspan=2, sticky="N")

        self.kick_btn = PrimaryButton(self.game_menu, text="Kick guest", command=self.kick_guest)
        self.kick_btn.grid(column=0, row=4, columnspan=6)

        self.surrender_btn = PrimaryButton(self.game_menu, text="Surrender", command=self.surrender)
        self.surrender_btn.grid(column=0, row=5, columnspan=3)

        self.claim_draw_btn = PrimaryButton(self.game_menu, text="Claim draw", command=self.claim_draw)
        self.claim_draw_btn.grid(column=3, row=5, columnspan=3)

        self.offer_draw_btn = PrimaryButton(self.game_menu, text="Offer draw", command=self.offer_draw)
        self.offer_draw_btn.grid(column=0, row=6, columnspan=6)

        self.accept_draw_btn = PrimaryButton(self.game_menu, text="Accept draw",
                                             command=lambda: self.respond_to_draw_offer(True))
        self.accept_draw_btn.grid(column=0, row=7, columnspan=3)
        self.reject_draw_btn = PrimaryButton(self.game_menu, text="Reject draw",
                                             command=lambda: self.respond_to_draw_offer(False))
        self.reject_draw_btn.grid(column=3, row=7, columnspan=3)

        self.quit_btn = SecondaryButton(self.game_menu, text="Back", command=self.leave)
        self.quit_btn.grid(column=0, row=8, columnspan=6, sticky="WS")

        self.reset()

    def update_menu(self):
        start_btn_state = NORMAL if self.game_room_service.can_start_private_game() else DISABLED
        self.start_classic_btn["state"] = start_btn_state
        self.start_rapid_btn["state"] = start_btn_state
        self.start_blitz_btn["state"] = start_btn_state
        self.kick_btn["state"] = NORMAL if self.game_room_service.can_kick_guest() else DISABLED
        self.surrender_btn["state"] = NORMAL if self.game_room_service.can_surrender() else DISABLED
        self.claim_draw_btn["state"] = NORMAL if self.game_room_service.can_claim_draw() else DISABLED
        self.offer_draw_btn["state"] = NORMAL if self.game_room_service.can_offer_draw() else DISABLED
        respond_to_draw_offer_state = NORMAL if self.game_room_service.can_respond_to_draw_offer() else DISABLED
        self.accept_draw_btn["state"] = respond_to_draw_offer_state
        self.reject_draw_btn["state"] = respond_to_draw_offer_state

    def start_game(self, game_type: GameType):
        self.game_room_service.start_private_game(game_type)

    def kick_guest(self):
        self.game_room_service.kick_from_private_room()

    def surrender(self):
        self.game_room_service.game_surrender()

    def claim_draw(self):
        self.game_room_service.game_claim_draw()

    def offer_draw(self):
        self.game_room_service.game_offer_draw()

    def respond_to_draw_offer(self, accepted: bool):
        self.game_room_service.game_respond_to_draw_offer(accepted)

    def leave(self):
        self.game_room_service.leave_private_room()

    def on_guest_joined_private_room(self, message: dict):
        self.game_room_service.on_guest_joined_private_room(message)
        self.update_menu()
        self.guest.nick_lbl["text"] = self.room.guest.nick

    def on_leave_private_room(self, message: dict):
        self.game_room_service.on_leave_private_room(message)
        if self.game_room_service.room:
            self.update_menu()
            self.host.reset_all_except_nick()
            self.guest.reset()
        else:
            self.navigate(ViewName.JOIN_PRIVATE)
            if message["player"]["nick"] != self.auth_service.current.nick:
                messagebox.showinfo("Info", "The host left the room!")

    def on_kick_from_private_room(self):
        self.game_room_service.on_kick_from_private_room()
        if self.game_room_service.room:
            self.update_menu()
            self.host.reset_all_except_nick()
            self.guest.reset()
        else:
            self.navigate(ViewName.JOIN_PRIVATE)
            messagebox.showinfo("Info", "You was kicked out from the private room!")

    def on_start_private_game(self, message: dict):
        self.game_room_service.on_start_private_game(message)
        self.update_menu()
        self.chessboard_visualizer.start()

        if self.auth_service.current == self.room.host:
            self.host.frame.grid(column=0, row=0, columnspan=3, sticky="N")
            self.guest.frame.grid(column=3, row=0, columnspan=3, sticky="N")
        else:
            self.guest.frame.grid(column=0, row=0, columnspan=3, sticky="N")
            self.host.frame.grid(column=3, row=0, columnspan=3, sticky="N")

        if self.room.teams[self.room.host] == Team.WHITE:
            self.host.team_lbl["image"] = self.host.white_img
            self.guest.team_lbl["image"] = self.host.black_img
        else:
            self.host.team_lbl["image"] = self.host.black_img
            self.guest.team_lbl["image"] = self.host.white_img

        self.host.update_time(self.room.times[self.room.teams[self.room.host]])
        self.guest.update_time(self.room.times[self.room.teams[self.room.guest]])
        if self.room.engine.currently_moving_team == self.room.teams[self.room.host]:
            self.host.update_time(30 * 1000)
            self.host.start_counting()
        else:
            self.guest.update_time(30 * 1000)
            self.guest.start_counting()

    def on_game_surrender(self, message: dict):
        self.game_room_service.on_game_surrender()
        self.update_menu()
        self.host.stop_timer()
        self.guest.stop_timer()
        if message["player"]["nick"] != self.auth_service.current.nick:
            messagebox.showinfo("Info", "Your opponent surrendered! You win!")

    def on_game_offer_draw(self, message: dict):
        self.game_room_service.on_game_offer_draw()
        self.update_menu()

    def on_game_respond_to_draw_offer(self, message: dict):
        self.game_room_service.on_game_respond_to_draw_offer(message)
        self.update_menu()
        if not self.room.running:
            self.host.stop_timer()
            self.guest.stop_timer()
            messagebox.showinfo("Info", "It's a draw! Nobody wins, nobody loses!")

    def on_game_claim_draw(self):
        self.game_room_service.on_game_claim_draw()
        self.update_menu()
        self.host.stop_timer()
        self.guest.stop_timer()
        messagebox.showinfo("Info", "It's a draw! Nobody wins, nobody loses!")

    def on_game_move(self, message: dict):
        move = self.game_room_service.on_game_move(message)
        self.update_menu()
        self.chessboard_visualizer.process_move(move)
        if self.room.engine.currently_moving_team == self.room.teams[self.room.host]:
            self.guest.update_time(self.room.times[self.room.teams[self.room.guest]])
            self.guest.update_timer_lbl()
            self.host.start_counting()
        else:
            self.host.update_time(self.room.times[self.room.teams[self.room.host]])
            self.host.update_timer_lbl()
            self.guest.start_counting()

    def on_game_time_end(self):
        self.game_room_service.on_game_time_end()
        self.update_menu()
        self.host.stop_timer()
        self.guest.stop_timer()
        messagebox.showinfo("Info", "The time is up!")

    def reset(self):
        self.room = None
        self.host.reset()
        self.guest.reset()
        self.access_key_lbl["text"] = ""
        self.start_classic_btn["state"] = DISABLED
        self.start_rapid_btn["state"] = DISABLED
        self.start_blitz_btn["state"] = DISABLED
        self.kick_btn["state"] = DISABLED
        self.surrender_btn["state"] = DISABLED
        self.claim_draw_btn["state"] = DISABLED
        self.offer_draw_btn["state"] = DISABLED
        self.accept_draw_btn["state"] = DISABLED
        self.reject_draw_btn["state"] = DISABLED
        self.chessboard_visualizer.reset()

    def show(self):
        self.room = self.game_room_service.room
        self.access_key_lbl["text"] = f"Access key: {self.room.access_key}"
        if self.room.host:
            self.host.nick_lbl["text"] = self.room.host.nick
        if self.room.guest:
            self.guest.nick_lbl["text"] = self.room.guest.nick

        self.chessboard_visualizer.table.tkraise()
        self.game_menu.tkraise()
