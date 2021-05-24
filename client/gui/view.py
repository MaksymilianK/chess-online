from abc import ABC, abstractmethod
from enum import Enum, auto
from tkinter import Tk
from typing import Callable

from client.connection.auth_service import AuthService
from client.gui.shared import DisplayBoundary


class ViewName(Enum):
    START = auto()
    SIGN_IN = auto()
    SIGN_UP = auto()
    JOIN_RANKED = auto()
    JOIN_PRIVATE = auto()
    RANKED_GAME = auto()
    PRIVATE_GAME = auto()


class View(ABC):
    def __init__(self, root: Tk, display: DisplayBoundary, navigate: Callable[[ViewName], None],
                 auth_service: AuthService):
        self.root = root
        self.display = display
        self.navigate = navigate
        self.auth_service = auth_service

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def show(self):
        pass
