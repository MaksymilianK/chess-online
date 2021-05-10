import json
from typing import Optional

from websockets import WebSocketServerProtocol

from server.exception import InvalidRequestException
from server.player.auth_service import AuthService
from server.player.player import Player
from shared.message.message_code import MessageCode


def _message_to_json(message_str: str):
    message: dict
    try:
        message = json.loads(message_str)
    except ValueError:
        raise InvalidRequestException("cannot parse JSON from message")

    if "code" not in message:
        raise InvalidRequestException("message does not contain code")

    return message


class MessageBroker:
    def __init__(self, auth_service: AuthService):
        self._auth_service = auth_service

        self._authenticated_actions = {
            MessageCode
        }

    async def on_anonymous_message(self, message_str: str, websocket: WebSocketServerProtocol) -> Optional[Player]:
        message = _message_to_json(message_str)
        code = message["code"]

        if code == MessageCode.SIGN_UP:
            return await self._auth_service.sign_up(message, websocket)
        elif code == MessageCode.SIGN_IN:
            return await self._auth_service.sign_in(message, websocket)
        else:
            raise InvalidRequestException("invalid message code")

    async def on_authenticated_message(self, message_str: str, websocket: WebSocketServerProtocol):
        message = _message_to_json(message_str)
        try:
            await self._authenticated_actions[message["code"]]()
        except KeyError:
            raise InvalidRequestException("invalid message code")
