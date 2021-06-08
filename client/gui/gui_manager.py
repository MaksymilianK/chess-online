import json
import os
from queue import Queue

import tkinter as tk
from PIL import ImageTk, Image

from client.connection.game_room_service import GameRoomService
from client.gui.game.private_game_view import PrivateGameView
from client.gui.game.ranked_game_view import RankedGameView
from client.gui.menu.join_private_view import JoinPrivateView
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

        self.root.attributes("-fullscreen", True)
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")

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

        img = Image.open(os.path.join(os.getcwd(), "client/img/bg.jpg"))
        img = img.resize((screen_width, screen_height), Image.ANTIALIAS)
        self.bg_img = ImageTk.PhotoImage(img)

        player_component = PlayerComponent(self.root, display, auth_service)

        self.views = {
            ViewName.SIGN_IN: SignInView(self.root, display, self.navigate, auth_service, player_component),
            ViewName.SIGN_UP: SignUpView(self.root, display, self.navigate, auth_service, player_component),
            ViewName.START: StartView(self.root, display, self.navigate, auth_service, player_component),
            ViewName.JOIN_RANKED: JoinRankedView(self.root, display, self.navigate, auth_service, player_component,
                                                 game_room_service),
            ViewName.JOIN_PRIVATE: JoinPrivateView(self.root, display, self.navigate, auth_service, player_component,
                                                   game_room_service),
            ViewName.RANKED_GAME: RankedGameView(self.root, display, self.navigate, auth_service, game_room_service),
            ViewName.PRIVATE_GAME: PrivateGameView(self.root, display, self.navigate, auth_service, game_room_service)
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
        elif code == MessageCode.JOINED_RANKED_ROOM.value:
            self.views[ViewName.JOIN_RANKED].on_joined_ranked_room(message)
        elif code == MessageCode.CANCEL_JOINING_RANKED.value:
            self.views[ViewName.JOIN_RANKED].on_cancel_joining_ranked()
        elif code == MessageCode.CREATE_PRIVATE_ROOM.value:
            self.views[ViewName.JOIN_PRIVATE].on_create_private_room(message)
        elif code == MessageCode.JOIN_PRIVATE_ROOM.value:
            self.views[ViewName.JOIN_PRIVATE].on_join_by_access_key(message)
        elif code == MessageCode.GUEST_JOINED_PRIVATE_ROOM.value:
            self.views[ViewName.PRIVATE_GAME].on_guest_joined_private_room(message)
        elif code == MessageCode.LEAVE_PRIVATE_ROOM.value:
            self.views[ViewName.PRIVATE_GAME].on_leave_private_room(message)
        elif code == MessageCode.KICK_FROM_PRIVATE_ROOM.value:
            self.views[ViewName.PRIVATE_GAME].on_kick_from_private_room()
        elif code == MessageCode.START_PRIVATE_GAME.value:
            self.views[ViewName.PRIVATE_GAME].on_start_private_game(message)
        elif code == MessageCode.GAME_SURRENDER.value:
            if self.current_view is self.views[ViewName.PRIVATE_GAME]:
                self.views[ViewName.PRIVATE_GAME].on_game_surrender(message)
            else:
                self.views[ViewName.RANKED_GAME].on_game_surrender(message)
        elif code == MessageCode.GAME_OFFER_DRAW.value:
            if self.current_view is self.views[ViewName.PRIVATE_GAME]:
                self.views[ViewName.PRIVATE_GAME].on_game_offer_draw(message)
            else:
                self.views[ViewName.RANKED_GAME].on_game_offer_draw(message)
        elif code == MessageCode.GAME_RESPOND_TO_DRAW_OFFER.value:
            if self.current_view is self.views[ViewName.PRIVATE_GAME]:
                self.views[ViewName.PRIVATE_GAME].on_game_respond_to_draw_offer(message)
            else:
                self.views[ViewName.RANKED_GAME].on_game_respond_to_draw_offer(message)
        elif code == MessageCode.GAME_CLAIM_DRAW.value:
            if self.current_view is self.views[ViewName.PRIVATE_GAME]:
                self.views[ViewName.PRIVATE_GAME].on_game_claim_draw()
            else:
                self.views[ViewName.RANKED_GAME].on_game_claim_draw()
        elif code == MessageCode.GAME_MOVE.value:
            if self.current_view is self.views[ViewName.PRIVATE_GAME]:
                self.views[ViewName.PRIVATE_GAME].on_game_move(message)
            else:
                self.views[ViewName.RANKED_GAME].on_game_move(message)
        elif code == MessageCode.GAME_TIME_END.value:
            if self.current_view is self.views[ViewName.PRIVATE_GAME]:
                self.views[ViewName.PRIVATE_GAME].on_game_time_end()
            else:
                self.views[ViewName.RANKED_GAME].on_game_time_end()
        elif code == MessageCode.PLAYER_DISCONNECTED.value:
            if self.current_view is self.views[ViewName.PRIVATE_GAME]:
                self.views[ViewName.PRIVATE_GAME].on_player_disconnected(message)
            else:
                self.views[ViewName.RANKED_GAME].on_player_disconnected(message)
