import json
from typing import Optional, Callable

from websockets import WebSocketServerProtocol

from server.request import InvalidRequestException
from server.game_room.game_room_service import GameRoomService
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
    def __init__(self, auth_service: AuthService, game_room_service: GameRoomService):
        self._auth_service = auth_service
        self.game_room_service = game_room_service

        self._authenticated_actions: dict[int, Callable] = {
            MessageCode.JOIN_RANKED_QUEUE.value: game_room_service.join_ranked_queue,
            MessageCode.CANCEL_JOINING_RANKED.value: game_room_service.cancel_joining_ranked,
            MessageCode.CREATE_PRIVATE_ROOM.value: game_room_service.create_private_room,
            MessageCode.JOIN_PRIVATE_ROOM.value: game_room_service.join_private_room,
            MessageCode.LEAVE_PRIVATE_ROOM.value: game_room_service.leave_private_room,
            MessageCode.KICK_FROM_PRIVATE_ROOM.value: game_room_service.kick_from_private_room,
            MessageCode.START_PRIVATE_GAME.value: game_room_service.start_private_game,
            MessageCode.GAME_SURRENDER.value: game_room_service.surrender,
            MessageCode.GAME_OFFER_DRAW.value: game_room_service.offer_draw,
            MessageCode.GAME_RESPOND_TO_DRAW_OFFER.value: game_room_service.respond_to_draw_offer,
            MessageCode.GAME_CLAIM_DRAW.value: game_room_service.claim_draw,
            MessageCode.GAME_MOVE.value: game_room_service.move
        }

    async def on_anonymous_message(self, message_str: str, websocket: WebSocketServerProtocol) -> Optional[Player]:
        message = _message_to_json(message_str)
        code = message["code"]

        if code == MessageCode.SIGN_UP.value:
            return await self._auth_service.sign_up(message, websocket)
        elif code == MessageCode.SIGN_IN.value:
            return await self._auth_service.sign_in(message, websocket)
        else:
            raise InvalidRequestException("Invalid message code")

    async def on_authenticated_message(self, message_str: str, sender: Player):
        message = _message_to_json(message_str)
        try:
            await self._authenticated_actions[message["code"]](message, sender)
        except KeyError:
            raise InvalidRequestException("Invalid message code")

    async def on_connection_closed(self, player: Player):
        await self.game_room_service.disconnect(player)
