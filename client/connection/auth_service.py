import json
from enum import Enum
from typing import Optional

from client.connection.connection_manager import ConnectionManager
from client.connection.player import Player, player_from_dict
from shared.message.message_code import MessageCode
from shared.validators.player_validators import nick_valid, email_valid, password_valid


class PlayerValidationStatus(Enum):
    VALID = 1
    INVALID_NICK = 2
    INVALID_EMAIL = 3
    INVALID_PASSWORD = 4


class AuthService:
    def __init__(self, connection_manager: ConnectionManager):
        self._current: Optional[Player] = None
        self._connection_manager = connection_manager

    def sign_up(self, nick: str, email: str, password: str) -> PlayerValidationStatus:
        if not nick_valid(nick):
            return PlayerValidationStatus.INVALID_NICK
        elif not email_valid(email):
            return PlayerValidationStatus.INVALID_EMAIL
        elif not password_valid(password):
            return PlayerValidationStatus.INVALID_PASSWORD

        self._connection_manager.connect(json.dumps({
            "code": MessageCode.SIGN_UP.value,
            "nick": nick,
            "email": email,
            "password": password
        }))

        return PlayerValidationStatus.VALID

    def sign_in(self, email: str, password: str) -> PlayerValidationStatus:
        if not email_valid(email):
            return PlayerValidationStatus.INVALID_EMAIL
        elif not password_valid(password):
            return PlayerValidationStatus.INVALID_PASSWORD

        self._connection_manager.connect(json.dumps({
            "code": MessageCode.SIGN_IN.value,
            "email": email,
            "password": password
        }))

        return PlayerValidationStatus.VALID

    @property
    def current(self) -> Optional[Player]:
        return self._current

    @current.setter
    def current(self, player_dict: dict):
        self._current = player_from_dict(player_dict)
