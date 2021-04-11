from typing import Optional

from server.player import PlayerRepository, Player


class AuthService:
    def __init__(self, player_repo: PlayerRepository):
        self._player_repo = player_repo

    def create_account(self, email: str, nick: str, password: str):
        pass

    def authenticate(self, email: str, password: str) -> Optional[Player]:
        pass
