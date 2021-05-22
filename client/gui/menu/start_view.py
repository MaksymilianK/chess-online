from tkinter import Tk
from typing import Callable

from client.gui.menu.menu import menu_frame, menu_title
from client.gui.menu.player_component import PlayerComponent
from client.gui.view import View, ViewName
from client.connection.auth_service import AuthService
from client.gui.shared import DisplayBoundary, PrimaryButton, SecondaryButton


class StartView(View):
    def __init__(self, root: Tk, display: DisplayBoundary, navigate: Callable[[ViewName], None],
                 auth_service: AuthService, player_component: PlayerComponent):
        super().__init__(root, display, navigate, auth_service)

        self.player_component = player_component

        self.frame = menu_frame(root, display)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)

        self.title = menu_title(self.frame, "Start")

        self.quit_btn = SecondaryButton(self.frame, text="Quit", command=lambda: root.quit())
        self.quit_btn.grid(row=0, column=1, sticky="EN")

        self.join_ranked_btn = PrimaryButton(self.frame, text="Join ranked", command=self.join_ranked)
        self.join_ranked_btn.grid(row=1, column=0, columnspan=2, ipadx=10, ipady=5)

        self.private_room_btn = PrimaryButton(self.frame, text="Private room", command=self.create_private_room)
        self.private_room_btn.grid(row=2, column=0, columnspan=2, ipadx=10, ipady=5)

    def join_ranked(self):
        self.navigate(ViewName.JOIN_RANKED)

    def create_private_room(self):
        pass

    def reset(self):
        pass

    def show(self):
        self.player_component.button.tkraise()
        self.frame.tkraise()
