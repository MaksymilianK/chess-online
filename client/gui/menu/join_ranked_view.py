import tkinter as tk
from typing import Callable

from client.connection.game_room_service import GameRoomService
from client.gui.menu.menu import menu_frame, menu_title
from client.gui.menu.player_component import PlayerComponent
from client.gui.view import View, ViewName
from client.connection.auth_service import AuthService
from client.gui.shared import DisplayBoundary, PrimaryButton, SecondaryButton
from shared.game.game_type import GameType, GAME_TYPES_BY_NAME


class JoinRankedView(View):
    def __init__(self, root: tk.Tk, display: DisplayBoundary, navigate: Callable[[ViewName], None],
                 auth_service: AuthService, player_component: PlayerComponent, game_room_service: GameRoomService):
        super().__init__(root, display, navigate, auth_service)

        self.player_component = player_component

        self.game_room_service = game_room_service
        self.joining = False

        self.frame = menu_frame(root, display)
        self.frame.columnconfigure(0, weight=1)

        for row in range(6):
            self.frame.rowconfigure(row, weight=1)

        self.title = menu_title(self.frame, "Ranked game")

        self.game_type = tk.StringVar(self.frame, GameType.CLASSIC.value)

        self.classic_select = tk.Radiobutton(self.frame, text="Classic", value=GameType.CLASSIC.value,
                                             variable=self.game_type, bg="#ffffff",
                                             font=("Times New Roman", 15, "bold"))
        self.classic_select.grid(column=0, row=1)

        self.rapid_select = tk.Radiobutton(self.frame, text="Rapid", value=GameType.RAPID.value,
                                           variable=self.game_type, bg="#ffffff", font=("Times New Roman", 15, "bold"))
        self.rapid_select.grid(column=0, row=2)

        self.blitz_select = tk.Radiobutton(self.frame, text="Blitz", value=GameType.BLITZ.value,
                                           variable=self.game_type, bg="#ffffff", font=("Times New Roman", 15, "bold"))
        self.blitz_select.grid(column=0, row=3)

        self.join_btn = PrimaryButton(self.frame, text="Join", command=self.join_ranked_queue)
        self.join_btn.grid(column=0, row=4)

        self.back_btn = SecondaryButton(self.frame, text="Back", command=self.back)
        self.back_btn.grid(column=0, row=5, sticky="WS")

    def join_ranked_queue(self):
        self.joining = True
        self.game_room_service.join_ranked_queue(GAME_TYPES_BY_NAME[self.game_type.get()])

    def back(self):
        if self.joining:
            self.game_room_service.cancel_joining_ranked()
        else:
            self.navigate(ViewName.START)

    def on_join_ranked_queue(self):
        self.join_btn["state"] = "disabled"
        self.join_btn["text"] = "In queue..."

    def on_cancel_joining_ranked(self):
        self.navigate(ViewName.START)

    def on_joined_ranked_room(self, message: dict):
        self.game_room_service.on_join_ranked_room(message)
        self.navigate(ViewName.RANKED_GAME)

    def reset(self):
        self.joining = False
        self.join_btn["state"] = "normal"
        self.join_btn["text"] = "Join"

    def show(self):
        self.player_component.button.tkraise()
        self.frame.tkraise()
