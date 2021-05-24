from tkinter import Tk, Label, StringVar
from typing import Callable

from client.connection.auth_service import AuthService
from client.connection.game_room_service import GameRoomService
from client.gui.error_message import INVALID_ACCESS_KEY_MESSAGE, PRIVATE_ROOM_MESSAGES
from client.gui.menu.menu import menu_title, menu_frame
from client.gui.menu.player_component import PlayerComponent
from client.gui.shared import DisplayBoundary, SecondaryButton, PrimaryButton, FormEntry, ErrorMessage
from client.gui.view import View, ViewName
from shared.message.private_room_joining_status import PrivateRoomJoiningStatus


class JoinPrivateView(View):
    def __init__(self, root: Tk, display: DisplayBoundary, navigate: Callable[[ViewName], None],
                 auth_service: AuthService, player_component: PlayerComponent, game_room_service: GameRoomService):
        super().__init__(root, display, navigate, auth_service)

        self.player_component = player_component
        self.game_room_service = game_room_service

        self.frame = menu_frame(root, display)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=1)
        self.frame.rowconfigure(4, weight=1)
        self.frame.rowconfigure(5, weight=1)

        self.title = menu_title(self.frame, "Private room")

        self.create_btn = PrimaryButton(self.frame, text="Create room", command=self.create_private_room)
        self.create_btn.grid(column=0, row=1, columnspan=2)

        self.or_lbl = Label(self.frame, text="or", bg="#ffffff", font=("Times New Roman", 16, "bold"))
        self.or_lbl.grid(column=0, row=2, columnspan=2)

        self.access_key_entry = FormEntry(self.frame)
        self.access_key_entry.grid(column=0, row=3)

        self.join_btn = PrimaryButton(self.frame, text="Join by key", command=self.join_by_access_key)
        self.join_btn.grid(column=1, row=3)

        self.error_text = StringVar("")
        self.error_msg = ErrorMessage(self.frame, textvariable=self.error_text)
        self.error_msg.grid(column=0, row=4, columnspan=2)

        self.back_btn = SecondaryButton(self.frame, text="Back", command=lambda: self.navigate(ViewName.START))
        self.back_btn.grid(column=0, row=5, sticky="WS", columnspan=2)

    def create_private_room(self):
        self.game_room_service.create_private_room()

    def join_by_access_key(self):
        access_key: str = self.access_key_entry.get().upper()
        if self.game_room_service.join_private_room(access_key):
            self.error_text.set("")
        else:
            self.error_text.set(INVALID_ACCESS_KEY_MESSAGE)

    def on_create_private_room(self, message: dict):
        self.game_room_service.on_create_private_room(message)
        self.navigate(ViewName.PRIVATE_GAME)

    def on_join_by_access_key(self, message: dict):
        status: int = message["status"]
        if status == PrivateRoomJoiningStatus.SUCCESS.value:
            self.game_room_service.on_join_private_room(message)
            self.navigate(ViewName.PRIVATE_GAME)
        else:
            self.error_text.set(PRIVATE_ROOM_MESSAGES[status])

    def reset(self):
        self.error_text.set("")

    def show(self):
        self.player_component.button.tkraise()
        self.frame.tkraise()