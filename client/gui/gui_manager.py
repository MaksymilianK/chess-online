import json
import logging
import platform
import tkinter as tk
from queue import Queue

from PIL import ImageTk, Image

from client.gui.menu.join_ranked_view import JoinRankedView
from client.gui.menu.start_view import StartView
from client.gui.shared import DisplayBoundary
from client.gui.view import ViewName
from client.connection.auth_service import AuthService
from client.gui.auth.sign_in_view import SignInView
from client.gui.auth.sign_up_view import SignUpView
from shared.message.message_code import MessageCode


class GuiManager:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
        self._messages: Queue[str] = Queue()
        self.root = tk.Tk()

        if platform.system() == "Windows":
            self.root.attributes("-fullscreen", True)
        else:
            self.root.attributes("-zoomed", True)

        self.root.resizable(False, False)
        self.root.title("Chess Online")
        screen_width = self.root.winfo_vrootwidth()
        screen_height = self.root.winfo_vrootheight()

        img = Image.open("client/img/bg3.jpg")
        img = img.resize((screen_width, screen_height), Image.ANTIALIAS)
        self.bg_img = ImageTk.PhotoImage(img)
        self.bg = tk.Label(self.root, image=self.bg_img)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)

        screen_ratio = screen_width / screen_height
        target_ratio = 16 / 9

        width = screen_width
        height = screen_height
        if screen_ratio - target_ratio > 0.05:
            width = round(16 / 9 * screen_height)
        elif screen_ratio - target_ratio < -0.05:
            height = round(9 / 16 * screen_width)

        x = round((screen_width - width) / 2)
        y = round((screen_height - height) / 2)

        display_size = DisplayBoundary(x, y, width, height)

        self.views = {
            ViewName.START: StartView(self.root, display_size, self.navigate, auth_service),
            ViewName.SIGN_UP: SignUpView(self.root, display_size, self.navigate, auth_service),
            ViewName.SIGN_IN: SignInView(self.root, display_size, self.navigate, auth_service),
            ViewName.JOIN_RANKED: JoinRankedView(self.root, display_size, self.navigate, auth_service)
        }

        self.current_view = self.views[ViewName.SIGN_IN]
        self.current_view.show()

        self.root.bind("<<message>>", self._on_message)

    def start(self):
        self.root.mainloop()

    def notify_message(self, message: str):
        self._messages.put(message)
        self.root.event_generate("<<message>>")

    def navigate(self, view: ViewName):
        self.bg.tkraise()
        self.views[view].show()
        self.current_view.reset()
        self.current_view = self.views[view]

    def _on_message(self, event):
        message = json.loads(self._messages.get())
        code: int = message["code"]
        logging.fatal("gui message")

        if code == MessageCode.SIGN_UP.value:
            self.views[ViewName.SIGN_UP].on_sign_up(message)
        elif code == MessageCode.SIGN_IN.value:
            self.views[ViewName.SIGN_IN].on_sign_in(message)



