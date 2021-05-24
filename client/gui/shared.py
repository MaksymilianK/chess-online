import platform
from tkinter import Button, Label, Entry, Message

from client.connection.auth_service import PlayerValidationStatus

if platform.system() == "Darwin":
    from tkmacosx import Button as Button


class DisplayBoundary:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class FormLabel(Label):
    def __init__(self, master, **kw):
        args = {
            "font": ("Times New Roman", 14, "bold"),
            "fg": "gray",
            "bg": "white"
        }

        for key, value in kw.items():
            args[key] = value

        super().__init__(master, args)


class FormEntry(Entry):
    def __init__(self, master, **kw):
        args = {
            "font": ("Times New Roman", 12),
            "bg": "#eeeeee"
        }

        for key, value in kw.items():
            args[key] = value

        super().__init__(master, args)


class ErrorMessage(Message):
    def __init__(self, master, **kw):
        args = {
            "font": ("Times New Roman", 12, "bold"),
            "fg": "#ff0000",
            "bg": "#ffffff",
            "width": master.winfo_width() - 150,
            "anchor": "w"
        }
        
        for key, value in kw.items():
            args[key] = value

        super(ErrorMessage, self).__init__(master, args)


class PrimaryButton(Button):
    def __init__(self, master, **kw):
        args = {
            "font": ("Times New Roman", 12, "bold"),
            "fg": "#ffffff",
            "bg": "#d77337",
            "activeforeground": "#ffffff",
            "activebackground": "#c56328",
            "cursor": "hand2",
            "padx": 10
        }
        if platform.system() == "Darwin":
            args["borderless"] = 1

        for key, value in kw.items():
            args[key] = value

        super().__init__(master, args)


class SecondaryButton(Button):
    def __init__(self, master, **kw):
        args = {
            "font": ("Times New Roman", 12, "bold"),
            "fg": "#ffffff",
            "bg": "#7a7a7a",
            "activeforeground": "#ffffff",
            "activebackground": "#636363",
            "cursor": "hand2",
            "padx": 10
        }
        if platform.system() == "Darwin":
            args["borderless"] = 1

        for key, value in kw.items():
            args[key] = value

        super().__init__(master, args)


class TextButton(Button):
    def __init__(self, master, **kw):
        args = {
            "font": ("Times New Roman", 12, "bold"),
            "fg": "#d77337",
            "bg": "#ffffff",
            "activeforeground": "#c56328",
            "activebackground": "#ffffff",
            "cursor": "hand2",
            "bd": 0
        }
        if platform.system() == "Darwin":
            args["borderless"] = 1

        for key, value in kw.items():
            args[key] = value

        super().__init__(master, args)
