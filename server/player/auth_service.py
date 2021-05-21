import json
import re
from typing import Optional

import argon2
from argon2.exceptions import VerifyMismatchError
from websockets import WebSocketServerProtocol

from server.player.player_repo import PlayerRepository
from server.request import InvalidRequestException, assert_in
from server.player.player import Player, DEFAULT_ELO
from server.player.player_repo import PlayerModel
from shared.game.game_type import GameType
from shared.message.auth_status import AuthStatus
from shared.message.message_code import MessageCode


NICK_REGEX = re.compile("^\\w{3,16}$")
EMAIL_REGEX = re.compile("^.{1,50}@.{1,25}\\..{1,25}$")


class AuthService:
    def __init__(self, player_repo: PlayerRepository, password_hasher=argon2.PasswordHasher()):
        self._player_repo = player_repo
        self._password_hasher = password_hasher

    async def sign_up(self, message: dict, websocket: WebSocketServerProtocol) -> Optional[Player]:
        assert_in(message, ("nick", str), ("email", str), ("password", str))
        nick, email, password = message["nick"], message["email"], message["password"]

        if not nick_valid(nick) or not email_valid(email) or not password_valid(password):
            raise InvalidRequestException("invalid message field")

        if await self._player_repo.exists_with_nick(nick):
            await websocket.close(code=4000, reason=json.dumps({
                "code": MessageCode.SIGN_UP.value,
                "status": AuthStatus.NICK_EXIST.value
            }))
            return None
        elif await self._player_repo.exists_with_email(email):
            await websocket.close(code=4000, reason=json.dumps({
                "code": MessageCode.SIGN_UP.value,
                "status": AuthStatus.EMAIL_EXIST.value
            }))
            return None

        elo = {
            GameType.BLITZ: DEFAULT_ELO,
            GameType.RAPID: DEFAULT_ELO,
            GameType.CLASSIC: DEFAULT_ELO
        }
        await self._player_repo.insert_one(
            PlayerModel(
                nick,
                elo,
                email,
                self._password_hasher.hash(password)
            )
        )

        player = Player(nick, elo, websocket)
        await websocket.send(json.dumps({
            "code": MessageCode.SIGN_UP.value,
            "status": AuthStatus.SUCCESS.value,
            "player": player.as_response()
        }))
        return player

    async def sign_in(self, message: dict, websocket: WebSocketServerProtocol) -> Optional[Player]:
        assert_in(message, ("email", str), ("password", str))
        email, password = message["email"], message["password"]

        if not email_valid(email) or not password_valid(password):
            raise InvalidRequestException("invalid message field")

        model = await self._player_repo.find_one_by_email(email)
        if model is None:
            await websocket.close(code=4000, reason=json.dumps({
                "code": MessageCode.SIGN_IN.value,
                "status": AuthStatus.EMAIL_NOT_EXIST.value
            }))
            return None

        try:
            self._password_hasher.verify(model.password_hash, password)
        except VerifyMismatchError:
            await websocket.close(code=4000, reason=json.dumps({
                "code": MessageCode.SIGN_IN.value,
                "status": AuthStatus.WRONG_PASSWORD.value
            }))
            return None

        player = Player(model.nick, model.elo, websocket)
        await websocket.send(json.dumps({
            "code": MessageCode.SIGN_IN.value,
            "status": AuthStatus.SUCCESS.value,
            "player": player.as_response()
        }))
        return player


def nick_valid(nick: str) -> bool:
    return NICK_REGEX.match(nick) is not None


def email_valid(email: str) -> bool:
    return EMAIL_REGEX.match(email) is not None


def password_valid(password: str) -> bool:
    return 7 <= len(password) <= 75
