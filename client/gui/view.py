from abc import ABC, abstractmethod
from enum import Enum, auto
from tkinter import Tk
from typing import Callable

from client.connection.auth_service import AuthService
from client.gui.menu.player_component import PlayerComponent
from client.gui.shared import DisplayBoundary


class ViewName(Enum):
    START = auto()
    SIGN_IN = auto()
    SIGN_UP = auto()
    JOIN_RANKED = auto()
    RANKED_GAME = auto()


class View(ABC):
    def __init__(self, root: Tk, display: DisplayBoundary, navigate: Callable[[ViewName], None],
                 auth_service: AuthService, player_component: PlayerComponent):
        self.root = root
        self.display = display
        self.navigate = navigate
        self.auth_service = auth_service
        self.player_component = player_component

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def show(self):
        pass
