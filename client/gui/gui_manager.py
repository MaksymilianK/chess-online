import json
import platform
import tkinter as tk
from queue import Queue

from PIL import ImageTk, Image

from client.connection.game_room_service import GameRoomService
from client.gui.game.ranked_game_view import RankedGameView
from client.gui.menu.join_ranked_view import JoinRankedView
from client.gui.menu.player_component import PlayerComponent
from client.gui.menu.start_view import StartView
from client.gui.shared import DisplayBoundary
from client.gui.view import ViewName
from client.connection.auth_service import AuthService
from client.gui.auth.sign_in_view import SignInView
from client.gui.auth.sign_up_view import SignUpView
from shared.message.message_code import MessageCode


class GuiManager:
    def __init__(self, auth_service: AuthService, game_room_service: GameRoomService):
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

        display = DisplayBoundary(x, y, width, height)

        img = Image.open("client/img/bg3.jpg")
        img = img.resize((screen_width, screen_height), Image.ANTIALIAS)
        self.bg_img = ImageTk.PhotoImage(img)

        player_component = PlayerComponent(self.root, display, auth_service)

        self.views = {
            ViewName.SIGN_IN: SignInView(self.root, display, self.navigate, auth_service, player_component),
            ViewName.SIGN_UP: SignUpView(self.root, display, self.navigate, auth_service, player_component),
            ViewName.START: StartView(self.root, display, self.navigate, auth_service, player_component),
            ViewName.JOIN_RANKED: JoinRankedView(self.root, display, self.navigate, auth_service, player_component,
                                                 game_room_service),
            ViewName.RANKED_GAME: RankedGameView(self.root, display, self.navigate, auth_service, player_component,
                                                 game_room_service)
        }

        self.bg = tk.Label(self.root, image=self.bg_img)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)

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

        if code == MessageCode.SIGN_UP.value:
            self.views[ViewName.SIGN_UP].on_sign_up(message)
        elif code == MessageCode.SIGN_IN.value:
            self.views[ViewName.SIGN_IN].on_sign_in(message)
        elif code == MessageCode.JOIN_RANKED_QUEUE.value:
            self.views[ViewName.JOIN_RANKED].on_join_ranked_queue()


