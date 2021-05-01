import json
import re
from typing import Optional

import argon2
from websockets import WebSocketServerProtocol

from server.errors import InvalidRequestError, NickTakenError, EmailTakenError, EmailNotFoundError, WrongPasswordError
from server.message_codes import LOGIN_SUCCESS
from server.player_repo import PlayerRepository, PlayerModel

DEFAULT_ELO = 1000
NICK_REGEX = re.compile("^\\w{3,16}$")
EMAIL_REGEX = re.compile("^.{1,50}@.{1,25}\\..{1,25}$")


class Player:
    def __init__(self, nick: str, elo: int):
        self.nick = nick
        self.elo = elo


class AuthService:
    def __init__(self, player_repo: PlayerRepository, password_hasher=argon2.PasswordHasher()):
        self._player_repo = player_repo
        self._password_hasher = password_hasher

    async def sign_up(self, data: dict, websocket: WebSocketServerProtocol) -> (dict, Optional[Player]):
        if "nick" not in data:
            raise InvalidRequestError("Missing nick")
        elif "email" not in data:
            raise InvalidRequestError("Missing email")
        elif "password" not in data:
            raise InvalidRequestError("Missing password")

        nick = data["nick"]
        email = data["email"]
        password = data["password"]

        if not nick_valid(nick):
            raise InvalidRequestError("Nick is invalid")
        elif not email_valid(email):
            raise InvalidRequestError("Email is invalid")

        if await self._player_repo.exists_with_nick(nick):
            raise NickTakenError("Nick is already taken")
        elif await self._player_repo.exists_with_email(email):
            raise EmailTakenError("Email is already taken")

        await self._player_repo.insert_one(
            PlayerModel(
                nick,
                DEFAULT_ELO,
                email,
                self._password_hasher.hash(password)
            )
        )

        await websocket.send(json.dumps({
                "code": LOGIN_SUCCESS,
                "nick": nick,
                "elo": DEFAULT_ELO
        }))
        return Player(nick, DEFAULT_ELO),

    async def sign_in(self, data: dict, websocket: WebSocketServerProtocol) -> Player:
        if "email" not in data:
            raise InvalidRequestError("Missing email")
        elif "password" not in data:
            raise InvalidRequestError("Missing password")

        email = data["email"]
        password = data["password"]

        if not email_valid(email):
            raise InvalidRequestError("Email is invalid")

        model = await self._player_repo.find_one_by_email(email)
        if model is None:
            raise EmailNotFoundError("Player with the given email does not exist")

        if not self._password_hasher.verify(model.password_hash, password):
            raise WrongPasswordError("Password is wrong")

        await websocket.send(json.dumps({
            "code": LOGIN_SUCCESS,
            "nick": model.nick,
            "elo": model.elo
        }))
        return Player(model.nick, model.elo)


def nick_valid(nick: str) -> bool:
    return NICK_REGEX.match(nick) is not None


def email_valid(email: str) -> bool:
    return EMAIL_REGEX.match(email) is not None


def password_valid(password: str) -> bool:
    return 7 <= len(password) <= 75
