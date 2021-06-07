from typing import Optional
import os

from tkinter import Tk, Label, LEFT, EventType
from PIL import Image, ImageTk

from shared.game.game_type import GameType
from client.connection.auth_service import AuthService
from client.gui.shared import DisplayBoundary, PrimaryButton


class PlayerComponent:
    def __init__(self, root: Tk, display: DisplayBoundary, auth_service: AuthService):
        self.root = root
        self.display = display
        self.auth_service = auth_service

        img = Image.open(os.path.join(os.getcwd(), "client/img/player.png"))
        img = img.resize((36, 36), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(img)
        self.button = PrimaryButton(root, text="", image=self.image, compound=LEFT,
                                    font=("Times New Roman", 14, "bold"))
        self.button.place(
            x=display.x + display.width - 0.2 * display.width,
            y=display.y + 0.05 * display.width,
            width=0.15 * display.width,
            height=0.05 * display.height
        )
        self.button.bind("<Button-1>", self.show_hide_ranking)

        self._ranking_label: Optional[Label] = None
        self._ranking_title_label: Optional[Label] = None

    def update(self):
        if self.auth_service.current:
            self.button["text"] = self.auth_service.current.nick
        else:
            self.button["text"] = ""

    def show_hide_ranking(self, event: EventType):
        if self._ranking_label is None:
            ranking_info = f"Classic: {self.auth_service.current.elo[GameType.CLASSIC]}\n" + \
                           f"Rapid: {self.auth_service.current.elo[GameType.RAPID]}\n" + \
                           f"Blitz: {self.auth_service.current.elo[GameType.BLITZ]}"

            self._ranking_title_label = Label(self.root, text="♔ Your Ranking ♔", font=("Times New Roman", 14, "bold"),
                                              fg="gray", bg="white", anchor="s")
            self._ranking_title_label.place(
                x=self.display.x + self.display.width - 0.2 * self.display.width,
                y=self.display.y + 0.05 * self.display.width + 0.05 * self.display.height,
                width=0.15 * self.display.width,
                height=0.05 * self.display.height
            )

            self._ranking_label = Label(self.root, text=ranking_info, font=("Times New Roman", 14, "bold"),
                                        fg="gray", bg="white", justify=LEFT)
            self._ranking_label.place(
                x=self.display.x + self.display.width - 0.2 * self.display.width,
                y=self.display.y + 0.05 * self.display.width + 2 * 0.05 * self.display.height,
                width=0.15 * self.display.width,
                height=0.1 * self.display.height
            )
            self._ranking_label.tkraise()
        else:
            self._ranking_label.destroy()
            self._ranking_label = None
            self._ranking_title_label.destroy()
            self._ranking_title_label = None
