import tkinter as tk
from typing import Callable

from client.gui.menu.menu import menu_frame, menu_title
from client.gui.view import View, ViewName
from client.connection.auth_service import AuthService
from client.gui.shared import DisplayBoundary, PrimaryButton, SecondaryButton
from shared.game.game_type import GameType


class JoinRankedView(View):
    def __init__(self, root: tk.Tk, display: DisplayBoundary, navigate: Callable[[ViewName], None],
                 auth_service: AuthService):
        super().__init__(root, display, navigate, auth_service)

        self.frame = menu_frame(root, display)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=1)
        self.frame.rowconfigure(4, weight=1)
        self.frame.rowconfigure(5, weight=1)

        self.title = menu_title(self.frame, "Ranked game")

        self.game_type = tk.IntVar(self.frame, GameType.CLASSIC.value)

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

        self.join_btn = PrimaryButton(self.frame, text="Join")
        self.join_btn.grid(column=0, row=4)

        self.join_btn["state"] = tk.DISABLED
        self.join_btn["text"] = "Cancel"

        self.back_btn = SecondaryButton(self.frame, text="🠔 Back", command=lambda: navigate(ViewName.START))
        self.back_btn.grid(column=0, row=5, sticky="WS")

    def reset(self):
        pass

    def show(self):
        self.frame.tkraise()
