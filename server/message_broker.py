import json
from typing import Optional

from websockets import WebSocketServerProtocol

from server.auth import Player, AuthService
from server.errors import InvalidRequestError, EmailTakenError, EmailNotFoundError, WrongPasswordError, \
    NickTakenError, INVALID_REQUEST, EMAIL_TAKEN, EMAIL_NOT_FOUND, WRONG_PASSWORD


SIGN_UP: int = 1
SIGN_IN: int = 2
JOIN_RANKED: int = 3
CREATE_PRIVATE: int = 4
JOIN_PRIVATE: int = 5
GAME_INTERNAL: int = 6


def _parse_message(message_str: str):
    message: dict
    try:
        message = json.loads(message_str)
    except ValueError:
        raise InvalidRequestError("Cannot parse JSON from message")

    if "code" not in message:
        raise InvalidRequestError("Message does not contain code")

    return message


class MessageBroker:
    def __init__(self, auth_service: AuthService):
        self._auth_service = auth_service

    async def on_anonymous_message(self, message_str: str, websocket: WebSocketServerProtocol) -> Optional[Player]:
        try:
            message = _parse_message(message_str)
            code = message["code"]

            if code == SIGN_UP:
                return await self._auth_service.sign_up(message)
            elif code == SIGN_IN:
                return await self._auth_service.sign_in(message)
            else:
                raise InvalidRequestError("Message not allowed")

        except InvalidRequestError as e:
            await websocket.close(code=INVALID_REQUEST, reason=str(e))
        except EmailTakenError as e:
            await websocket.close(code=EMAIL_TAKEN, reason=str(e))
        except NickTakenError as e:
            await websocket.close(code=EMAIL_TAKEN, reason=str(e))
        except EmailNotFoundError as e:
            await websocket.close(code=EMAIL_NOT_FOUND, reason=str(e))
        except WrongPasswordError as e:
            await websocket.close(code=WRONG_PASSWORD, reason=str(e))

        return None

    async def on_authenticated_message(self, message_str: str, websocket: WebSocketServerProtocol):
        try:
            message = _parse_message(message_str)
            code = message["code"]

            # TODO

        except InvalidRequestError as e:
            await websocket.close(code=INVALID_REQUEST, reason=str(e))

        return None
