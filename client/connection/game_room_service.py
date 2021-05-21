import json

from client import ConnectionManager
from shared.chess_engine.move import AbstractMove, MoveType
from shared.message.message_code import MessageCode


class GameRoomService:
    def __init__(self, connection_manager: ConnectionManager):
        self._connection_manager = connection_manager

    def join_ranked_queue(self, game_type: str):
        self._connection_manager.send(json.dumps({
            "code": MessageCode.JOIN_RANKED_QUEUE.value,
            "gameType": game_type
        }))

    def cancel_joining_ranked(self):
        self._connection_manager.send(json.dumps({
            "code": MessageCode.CANCEL_JOINING_RANKED.value
        }))

    def create_private_room(self):
        self._connection_manager.send(json.dumps({
            "code": MessageCode.CREATE_PRIVATE_ROOM.value
        }))

    def join_private_room(self, access_key: str):
        self._connection_manager.send(json.dumps({
            "code": MessageCode.JOIN_PRIVATE_ROOM.value,
            "accessKey": access_key
        }))

    def leave_private_room(self):
        self._connection_manager.send(json.dumps({
            "code": MessageCode.LEAVE_PRIVATE_ROOM.value
        }))

    def kick_from_private_room(self):
        self._connection_manager.send(json.dumps({
            "code": MessageCode.KICK_FROM_PRIVATE_ROOM.value
        }))

    def start_private_game(self, game_type: str):
        self._connection_manager.send(json.dumps({
            "code": MessageCode.START_PRIVATE_GAME.value,
            "gameType": game_type
        }))

    def game_surrender(self):
        self._connection_manager.send(json.dumps({
            "code": MessageCode.GAME_SURRENDER.value
        }))

    def game_offer_draw(self):
        self._connection_manager.send(json.dumps({
            "code": MessageCode.GAME_OFFER_DRAW.value
        }))

    def game_respond_to_draw_offer(self, accepted: bool):
        self._connection_manager.send(json.dumps({
            "code": MessageCode.GAME_RESPOND_TO_DRAW_OFFER.value,
            "accepted": accepted
        }))

    def game_claim_draw(self):
        self._connection_manager.send(json.dumps({
            "code": MessageCode.GAME_CLAIM_DRAW.value
        }))

    def game_move(self, move: AbstractMove):
        move_dict = {
            "moveType": move.type.value,
            "positionFrom": move.position_from.coords,
            "positionTo": move.position_to.coords
        }

        if move.type == MoveType.CASTLING:
            move_dict["rookFrom"] = move.rook_from
            move_dict["rookTo"] = move.rook_to
        elif move.type == MoveType.EN_PASSANT:
            move_dict["capturedPosition"] = move.captured_position
        elif move.type == MoveType.PROMOTION or move.type == MoveType.PROMOTION_WITH_CAPTURING:
            move_dict["pieceType"] = move.piece_type.value

        self._connection_manager.send(json.dumps({
            "code": MessageCode.GAME_MOVE.value,
            "move": move_dict
        }))
