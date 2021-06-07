import re

NICK_REGEX = re.compile("^\\w{3,16}$")
EMAIL_REGEX = re.compile("^.{1,50}@.{1,25}\\..{1,25}$")


def nick_valid(nick: str) -> bool:
    return NICK_REGEX.match(nick) is not None


def email_valid(email: str) -> bool:
    return EMAIL_REGEX.match(email) is not None


def password_valid(password: str) -> bool:
    return 7 <= len(password) <= 75
