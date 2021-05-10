class InvalidRequestException(Exception):
    def __init__(self, message: str):
        self.message = message


def assert_in(message: dict, *fields: str):
    for field in fields:
        if field not in message:
            raise InvalidRequestException("invalid message format")
