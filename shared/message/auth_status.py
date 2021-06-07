from enum import Enum


class AuthStatus(Enum):
    SUCCESS = 1
    EMAIL_NOT_EXIST = 2
    WRONG_PASSWORD = 3
    EMAIL_EXIST = 4
    NICK_EXIST = 5


STATUS_BY_CODE = {
    1: AuthStatus.SUCCESS,
    2: AuthStatus.EMAIL_NOT_EXIST,
    3: AuthStatus.WRONG_PASSWORD,
    4: AuthStatus.EMAIL_EXIST,
    5: AuthStatus.NICK_EXIST
}
