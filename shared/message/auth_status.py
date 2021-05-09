from enum import Enum


class AuthStatus(Enum):
    SUCCESS = 1
    EMAIL_NOT_EXIST = 2
    WRONG_PASSWORD = 3
    EMAIL_EXIST = 4
    NICK_EXIST = 5
