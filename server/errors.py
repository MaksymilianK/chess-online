INVALID_REQUEST = 4001
LOGIN_REQUIRED = 4002
EMAIL_TAKEN = 4003
EMAIL_NOT_FOUND = 4004
WRONG_PASSWORD = 4005


class InvalidRequestError(Exception):
    pass


class EmailTakenError(Exception):
    pass


class NickTakenError(Exception):
    pass


class EmailNotFoundError(Exception):
    pass


class WrongPasswordError(Exception):
    pass
