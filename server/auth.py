import re
from typing import Optional

from argon2 import PasswordHasher

from server.player_repo import PlayerRepository, PlayerModel

DEFAULT_ELO = 1000
NICK_REGEX = re.compile("\\w{3,16}")
EMAIL_REGEX = re.compile(".{1,50}@.{1,25}")


class NickConflictException(Exception):
    pass


class EmailConflictException(Exception):
    pass


class ValidationException(Exception):
    pass


class FormStructureException(Exception):
    pass


class NotFoundException(Exception):
    pass


class AuthenticationException(Exception):
    pass


class Player:
    def __init__(self, nick: str, elo: int):
        self.nick = nick
        self.elo = elo


class AuthService:
    def __init__(self, player_repo: PlayerRepository, password_hasher: PasswordHasher):
        self._player_repo = player_repo
        self._password_hasher = password_hasher

    def create_account(self, player_form: dict) -> Optional[Player]:
        try:
            nick = player_form["nick"]
            email = player_form["email"]
            password = player_form["password"]
        except KeyError:
            raise FormStructureException("Missing form fields")

        if not nick_valid(nick) or not email_valid(email) or not password_valid(password):
            raise ValidationException("Nick or email is invalid")

        if await self._player_repo.exists_with_nick(nick):
            raise NickConflictException("Given nick is already taken")
        elif await self._player_repo.exists_with_email(email):
            raise EmailConflictException("Given email is already taken")

        self._player_repo.insert_one(
            PlayerModel(
                nick,
                DEFAULT_ELO,
                email,
                self._password_hasher.hash(password)
            )
        )

        return Player(nick, DEFAULT_ELO)

    def authenticate(self, email: str, password: str) -> Player:
        model = await self._player_repo.find_one_by_email(email)
        if model is None:
            raise NotFoundException("A player with the given email does not exist")

        if not self._password_hasher.verify(model.password_hash, password):
            raise AuthenticationException("Password is wrong")

        return Player(model.nick, model.elo)


def nick_valid(nick: str) -> bool:
    return NICK_REGEX.fullmatch(nick) is not None


def email_valid(email: str) -> bool:
    return EMAIL_REGEX.fullmatch(email) is not None


def password_valid(password: str) -> bool:
    return 7 <= len(password) <= 75
