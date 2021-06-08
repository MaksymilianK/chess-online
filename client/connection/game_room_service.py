import json
import logging
import re
from abc import ABC, abstractmethod
from enum import auto, Enum
from typing import Optional

from client.connection.connection_manager import ConnectionManager
from client.connection.auth_service import AuthService

from client.connection.player import Player, player_from_dict
from shared.chess_engine.chess_engine import ChessEngine
from shared.chess_engine.move import AbstractMove, MoveType, Move, Capturing, Castling, EnPassant, Promotion, \
    PromotionWithCapturing, MOVE_TYPES_BY_CODE
from shared.chess_engine.piece import Team, PIECE_TYPES_FROM_CODE, TEAMS_BY_NAME
from shared.chess_engine.position import Vector2d
from shared.game.game_type import GameType, TIMES, GAME_TYPES_BY_NAME
from shared.game.ranking import elo_change, PlayerScore, reverse_score
from shared.message.message_code import MessageCode


ACCESS_KEY_REGEX = re.compile("^[A-Z]{5}$")


def parse_vector(coords: [int, int]) -> Vector2d:
    return Vector2d(coords[0], coords[1])


class GameRoomType(Enum):
    RANKED = auto()
    PRIVATE = auto()


class GameResult:
    def __init__(self, current_score: PlayerScore, current_elo_change: int = 0):
        self.current_score = current_score
        self.current_elo_change = current_elo_change


class GameRoom(ABC):
    def __init__(self):
        self.engine: Optional[ChessEngine] = None
        self.game_type: Optional[GameType] = None
        self.teams: dict[Player, Team] = {}
        self.times: dict[Team, int] = {}
        self.draw_offer: Optional[Team] = None
        self.game_result: Optional[GameResult] = None
        self._players: [Player] = []

    @property
    def running(self) -> bool:
        return self.game_result is None and self.engine is not None

    @property
    def players(self) -> [Player]:
        if self._players:
            return self._players
        else:
            self._players = [p for p in self.teams]
            return self._players

    @property
    @abstractmethod
    def type(self) -> GameRoomType:
        pass


class RankedGameRoom(GameRoom):
    def __init__(self, game_type: GameType, teams: dict[Player, Team]):
        super().__init__()
        self.game_type = game_type
        self.teams = teams
        self.times = {team: TIMES[game_type] for _, team in teams.items()}
        self.engine = ChessEngine()

    @property
    def type(self):
        return GameRoomType.RANKED


class PrivateGameRoom(GameRoom):
    def __init__(self, access_key: str, host: Player, guest: Player = None):
        super().__init__()
        self.access_key = access_key
        self.host = host
        self.guest = guest

    @property
    def type(self):
        return GameRoomType.PRIVATE


class GameRoomService:
    def __init__(self, connection_manager: ConnectionManager, auth_service: AuthService):
        self.room: Optional[GameRoom] = None
        self._auth_service = auth_service
        self._connection_manager = connection_manager

    @property
    def current_team(self) -> Team:
        return self.room.teams[self._auth_service.current]

    def is_current_moving(self) -> bool:
        return self.room.running and \
               self.room.teams[self._auth_service.current] == self.room.engine.currently_moving_team

    def can_start_private_game(self):
        return not self.room.running and self._auth_service.current == self.room.host and self.room.guest is not None

    def can_kick_guest(self):
        return self.room.guest is not None and self._auth_service.current == self.room.host

    def can_surrender(self):
        return self.room.running

    def can_claim_draw(self):
        return self.is_current_moving() and self.room.engine.can_claim_draw()

    def can_offer_draw(self):
        return self.is_current_moving() and self.room.draw_offer is None

    def can_respond_to_draw_offer(self):
        return self.room.draw_offer is not None and self.room.draw_offer != self.room.teams[self._auth_service.current]

    def on_player_disconnected(self):
        if self.room.type == GameRoomType.RANKED:
            players = self.room.players
            if self._auth_service.current == players[0]:
                self._on_ranked_end(players, PlayerScore.WIN)
            else:
                self._on_ranked_end(players, PlayerScore.LOSS)
        else:
            self.room.game_result = GameResult(PlayerScore.WIN)

    def on_create_private_room(self, message: dict):
        self.room = PrivateGameRoom(message["accessKey"], self._auth_service.current)

    def on_join_private_room(self, message: dict):
        self.room = PrivateGameRoom(
            message["accessKey"],
            player_from_dict(message["host"]),
            self._auth_service.current
        )

    def on_join_ranked_room(self, message: dict):
        self.room = RankedGameRoom(
            GAME_TYPES_BY_NAME[message["gameType"]],
            {player_from_dict(p): TEAMS_BY_NAME[t] for t, p in message["teams"].items()}
        )
        logging.fatal(self.room)

    def on_guest_joined_private_room(self, message: dict):
        self.room.guest = player_from_dict(message["guest"])

    def on_leave_private_room(self, message: dict):
        player = player_from_dict(message["player"])

        if player == self._auth_service.current:
            self.room = None
        elif player == self.room.host:
            self.room.host = None
        else:
            self.room.guest = None

    def on_kick_from_private_room(self):
        if self.room.guest == self._auth_service.current:
            self.room = None
        else:
            self.room.guest = None

    def on_start_private_game(self, message: dict):
        self.room.game_result = None
        self.room.engine = ChessEngine()
        self.room.game_type = GAME_TYPES_BY_NAME[message["gameType"]]
        self.room.teams = {player_from_dict(p): TEAMS_BY_NAME[t] for t, p in message["teams"].items()}
        self.room.times = {
            Team.WHITE: TIMES[self.room.game_type],
            Team.BLACK: TIMES[self.room.game_type]
        }

    def on_game_surrender(self, message: dict):
        player = player_from_dict(message["player"])

        if self.room.type == GameRoomType.RANKED:
            players = self.room.players
            if player == players[0]:
                self._on_ranked_end(self.room.players, PlayerScore.LOSS)
            else:
                self._on_ranked_end(self.room.players, PlayerScore.WIN)
        else:
            if player == self._auth_service.current:
                self.room.game_result = GameResult(PlayerScore.LOSS)
            else:
                self.room.game_result = GameResult(PlayerScore.WIN)

    def on_game_offer_draw(self):
        self.room.draw_offer = self.room.engine.currently_moving_team

    def on_game_respond_to_draw_offer(self, message: dict):
        self.room.draw_offer = None
        if message["accepted"]:
            if self.room.game_type == GameRoomType.RANKED:
                self._on_ranked_end(self.room.players, PlayerScore.DRAW)
            else:
                self.room.game_result = GameResult(PlayerScore.DRAW)

    def on_game_claim_draw(self):
        self.room.engine = None
        if self.room.type == GameRoomType.RANKED:
            self._on_ranked_end(self.room.players, PlayerScore.DRAW)
        else:
            self.room.game_result = GameResult(PlayerScore.DRAW)

    def on_game_move(self, message: dict):
        move_dict = message["move"]
        move_type = MOVE_TYPES_BY_CODE[move_dict["type"]]
        position_from, position_to = parse_vector(move_dict["positionFrom"]), parse_vector(move_dict["positionTo"])

        move: AbstractMove
        if move_type == MoveType.MOVE:
            move = Move(position_from, position_to)
        elif move_type == MoveType.CAPTURING:
            move = Capturing(position_from, position_to)
        elif move_type == MoveType.CASTLING:
            move = Castling(
                position_from,
                position_to,
                parse_vector(move_dict["rookFrom"]),
                parse_vector(move_dict["rookTo"])
            )
        elif move_type == MoveType.EN_PASSANT:
            move = EnPassant(position_from, position_to, parse_vector(move_dict["capturedPosition"]))
        elif move_type == MoveType.PROMOTION:
            move = Promotion(position_from, position_to, PIECE_TYPES_FROM_CODE[move_dict["pieceType"]])
        else:
            move = PromotionWithCapturing(position_from, position_to, PIECE_TYPES_FROM_CODE[move_dict["pieceType"]])

        if self.room.draw_offer:
            if self.room.draw_offer != self.room.engine.currently_moving_team:
                self.room.draw_offer = None

        self.room.times[self.room.engine.currently_moving_team] = message["timeLeft"]
        self.room.engine.process_move(move)
        if self.room.engine.is_checkmate():
            if self.room.type == GameRoomType.RANKED:
                players = self.room.players
                if self.room.teams[players[0]] == self.room.engine.currently_moving_team:
                    self._on_ranked_end(self.room.players, PlayerScore.LOSS)
                else:
                    self._on_ranked_end(self.room.players, PlayerScore.WIN)
            else:
                if self.room.teams[self._auth_service.current] == self.room.engine.currently_moving_team:
                    self.room.game_result = GameResult(PlayerScore.LOSS)
                else:
                    self.room.game_result = GameResult(PlayerScore.WIN)
        elif self.room.engine.is_tie():
            if self.room.type == GameRoomType.RANKED:
                self._on_ranked_end(self.room.players, PlayerScore.DRAW)
            else:
                self.room.game_result = GameResult(PlayerScore.DRAW)

        return move

    def on_game_time_end(self):
        if self.room.type == GameRoomType.RANKED:
            logging.fatal("game end service ranked")
            if self.room.engine.has_sufficient_material(self.room.engine.currently_opposite_team()):
                players = self.room.players
                if self.room.teams[players[0]] == self.room.engine.currently_moving_team:
                    self._on_ranked_end(self.room.players, PlayerScore.LOSS)
                else:
                    self._on_ranked_end(self.room.players, PlayerScore.WIN)
            else:
                self._on_ranked_end(self.room.players, PlayerScore.DRAW)
        else:
            logging.fatal("game end service private")
            if self.room.engine.has_sufficient_material(self.room.engine.currently_opposite_team()):
                if self.room.teams[self._auth_service.current] == self.room.engine.currently_moving_team:
                    self.room.game_result = GameResult(PlayerScore.LOSS)
                else:
                    self.room.game_result = GameResult(PlayerScore.WIN)
            else:
                self.room.game_result = GameResult(PlayerScore.DRAW)

    def join_ranked_queue(self, game_type: GameType):
        self._connection_manager.send(json.dumps({
            "code": MessageCode.JOIN_RANKED_QUEUE.value,
            "gameType": game_type.value
        }))

    def cancel_joining_ranked(self):
        self._connection_manager.send(json.dumps({
            "code": MessageCode.CANCEL_JOINING_RANKED.value
        }))

    def create_private_room(self):
        self._connection_manager.send(json.dumps({
            "code": MessageCode.CREATE_PRIVATE_ROOM.value
        }))

    def join_private_room(self, access_key: str) -> bool:
        if ACCESS_KEY_REGEX.match(access_key) is None:
            return False

        self._connection_manager.send(json.dumps({
            "code": MessageCode.JOIN_PRIVATE_ROOM.value,
            "accessKey": access_key
        }))
        return True

    def leave_private_room(self):
        self._connection_manager.send(json.dumps({
            "code": MessageCode.LEAVE_PRIVATE_ROOM.value
        }))

    def kick_from_private_room(self):
        self._connection_manager.send(json.dumps({
            "code": MessageCode.KICK_FROM_PRIVATE_ROOM.value
        }))

    def start_private_game(self, game_type: GameType):
        self._connection_manager.send(json.dumps({
            "code": MessageCode.START_PRIVATE_GAME.value,
            "gameType": game_type.value
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
            "type": move.type.value,
            "positionFrom": move.position_from.coords,
            "positionTo": move.position_to.coords
        }

        if move.type == MoveType.CASTLING:
            move_dict["rookFrom"] = move.rook_from.coords
            move_dict["rookTo"] = move.rook_to.coords
        elif move.type == MoveType.EN_PASSANT:
            move_dict["capturedPosition"] = move.captured_position.coords
        elif move.type == MoveType.PROMOTION or move.type == MoveType.PROMOTION_WITH_CAPTURING:
            move_dict["pieceType"] = move.piece_type.value

        self._connection_manager.send(json.dumps({
            "code": MessageCode.GAME_MOVE.value,
            "move": move_dict
        }))

    def _on_ranked_end(self, players: [Player], score: PlayerScore):
        current_elo_change = elo_change(
            players[0].elo[self.room.game_type],
            players[1].elo[self.room.game_type],
            score
        )
        logging.fatal(players[0].elo[self.room.game_type])
        logging.fatal(players[1].elo[self.room.game_type])
        logging.fatal(current_elo_change)

        if players[0] != self._auth_service.current:
            current_elo_change = -current_elo_change
            score = reverse_score(score)

        self._auth_service.current.elo[self.room.game_type] += current_elo_change

        self.room.game_result = GameResult(score, current_elo_change)
