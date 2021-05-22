from tkinter import *
from typing import Callable

import platform

from client.gui.error_message import VALIDATION_MESSAGES, AUTH_MESSAGES
from client.gui.menu.menu import menu_frame, menu_title
from client.gui.menu.player_component import PlayerComponent
from client.gui.view import View, ViewName
from client.connection.auth_service import AuthService, PlayerValidationStatus
from client.gui.shared import DisplayBoundary, PrimaryButton, TextButton, FormLabel, FormEntry, SecondaryButton
from shared.message.auth_status import STATUS_BY_CODE, AuthStatus

if platform.system() == "Darwin":
    from tkmacosx import Button


class SignUpView(View):
    def __init__(self, root: Tk, display: DisplayBoundary, navigate: Callable[[ViewName, ViewName], None],
                 auth_service: AuthService, player_component: PlayerComponent):
        super().__init__(root, display, navigate, auth_service)

        self.player_component = player_component
        self.frame = menu_frame(root, display)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=1)
        self.frame.rowconfigure(4, weight=1)
        self.frame.rowconfigure(5, weight=1)
        self.frame.rowconfigure(6, weight=1)
        self.frame.rowconfigure(7, weight=1)

        self.title = menu_title(self.frame, "Sign up")

        self.quit_btn = SecondaryButton(self.frame, text="Quit", command=lambda: root.quit())
        self.quit_btn.grid(row=0, column=1, sticky="EN")

        self.sign_in_lbl = Label(self.frame, text="Already a member?", font=("Times New Roman", 12, "bold"),
                                 fg="gray", bg="white")
        self.sign_in_lbl.grid(row=1, column=0, sticky="W")

        self.sign_in_btn = TextButton(self.frame, text="Sign in", command=lambda: self.navigate(ViewName.SIGN_IN))
        self.sign_in_btn.grid(row=1, column=1, sticky="W")

        self.nick_lbl = FormLabel(self.frame, text="Nick")
        self.nick_lbl.grid(row=2, column=0, sticky="WS")

        self.nick_entry = FormEntry(self.frame)
        self.nick_entry.grid(row=3, column=0, columnspan=2, sticky="WEN")

        self.email_lbl = FormLabel(self.frame, text="Email")
        self.email_lbl.grid(row=4, column=0, sticky="WS")

        self.email_entry = FormEntry(self.frame)
        self.email_entry.grid(row=5, column=0, columnspan=2, sticky="WEN")

        self.password_lbl = FormLabel(self.frame, text="Password")
        self.password_lbl.grid(row=6, column=0, sticky="WS")

        self.password_entry = FormEntry(self.frame, show="*")
        self.password_entry.grid(row=7, column=0, columnspan=2, sticky="WEN")

        self.sign_up_btn = PrimaryButton(self.frame, text="Sign up", command=self.sign_up)
        self.sign_up_btn.grid(row=8, column=1, sticky="WE")

        self.error_text = StringVar(self.frame, "")
        self.error_msg = Message(self.frame, textvariable=self.error_text, font=("Times New Roman", 12, "bold"),
                                 fg="#ff0000", bg="#ffffff", width=self.frame.winfo_width() - 150, anchor="w")
        self.error_msg.grid(row=9, column=0, columnspan=2, sticky="WS")

    def sign_up(self):
        validation_status = self.auth_service.sign_up(
            self.nick_entry.get(),
            self.email_entry.get(),
            self.password_entry.get()
        )
        if validation_status == PlayerValidationStatus.VALID:
            self.error_text.set("")
        else:
            self.error_text.set(VALIDATION_MESSAGES[validation_status])

    def on_sign_up(self, message: dict):
        status = STATUS_BY_CODE[message["status"]]
        if status == AuthStatus.SUCCESS:
            self.auth_service.current = message["player"]
            self.player_component.update()
            self.navigate(ViewName.START)
        else:
            self.error_text.set(AUTH_MESSAGES[status])

    def reset(self):
        self.nick_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.error_text.set("")
        self.email_entry.focus()

    def show(self):
        self.frame.tkraise()
