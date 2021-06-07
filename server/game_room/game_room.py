from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Optional

from server.game.game_runner import GameRunner
from server.player.player import Player


class GameRoomType(Enum):
    RANKED = auto()
    PRIVATE = auto()


class GameRoom(ABC):
    def __init__(self, game_runner: GameRunner):
        self.runner = game_runner

    async def send(self, message: str):
        await asyncio.gather(*[p.send(message) for p in self.players])

    @property
    @abstractmethod
    def players(self) -> list[Player]:
        pass

    @property
    @abstractmethod
    def type(self):
        pass


class RankedGameRoom(GameRoom):
    def __init__(self, player1: Player, player2: Player, game_runner: GameRunner):
        super().__init__(game_runner)
        self._players = (player1, player2)

    @property
    def players(self) -> list[Player]:
        return list(self._players)

    @property
    def type(self) -> GameRoomType:
        return GameRoomType.RANKED


class PrivateGameRoom(GameRoom):
    def __init__(self, host: Player, game_runner: GameRunner, access_key: str):
        super().__init__(game_runner)
        self.host = host
        self.guest: Optional[Player] = None
        self.access_key = access_key
        self.kicked: set[Player] = set()

    @property
    def players(self) -> list[Player]:
        players = [self.host]
        if self.guest:
            players.append(self.guest)

        return players

    @property
    def type(self) -> GameRoomType:
        return GameRoomType.PRIVATE

    @property
    def full(self) -> bool:
        return self.guest is not None
