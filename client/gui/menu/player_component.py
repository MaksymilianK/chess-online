from tkinter import Tk, LEFT

from PIL import Image, ImageTk

from client.connection.auth_service import AuthService
from client.gui.shared import DisplayBoundary, PrimaryButton


class PlayerComponent:
    def __init__(self, root: Tk, display: DisplayBoundary, auth_service: AuthService):
        self.auth_service = auth_service

        img = Image.open("client/img/player.png")
        img = img.resize((36, 36), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(img)
        self.button = PrimaryButton(root, text="", image=self.image, compound=LEFT,
                                    font=("Times New Roman", 14, "bold"))
        self.button.place(
            x=display.x + display.width - 0.2*display.width,
            y=display.y + 0.05*display.width,
            width=0.15*display.width,
            height=0.05*display.height
        )

    def update(self):
        if self.auth_service.current:
            self.button["text"] = self.auth_service.current.nick
        else:
            self.button["text"] = ""
