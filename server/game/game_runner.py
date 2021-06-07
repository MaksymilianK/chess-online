import random
from typing import Optional, Coroutine, Callable

from server.game.game_timer import GameTimer
from server.player.player import Player
from shared.chess_engine.chess_engine import ChessEngine
from shared.chess_engine.move import AbstractMove
from shared.chess_engine.piece import Team, opposite_team
from shared.game.game_type import TIMES, GameType


class GameEndStatus:
    def __init__(self, draw: bool, winner: Player, loser: Player, game_type: GameType):
        self.draw = draw
        self.winner = winner
        self.loser = loser
        self.game_type = game_type


class MoveStatus:
    def __init__(self, successful: bool, player_time_left: int, game_end_status: GameEndStatus = None):
        self.successful = successful
        self.player_time_left = player_time_left
        self.game_end_status = game_end_status


class GameRunner:
    def __init__(self):
        self.teams: dict[Player, Team] = {}
        self.game_type: Optional[GameType] = None
        self.timer: Optional[GameTimer] = None
        self._engine: Optional[ChessEngine] = None
        self._draw_offer: Optional[Player] = None
        self._on_time_end: Optional[Callable[[GameEndStatus], Coroutine]] = None

    @property
    def running(self) -> bool:
        return self._engine is not None

    def start(self, player1: Player, player2: Player, game_type: GameType, on_time_end: Callable):
        if self.running:
            return

        self.game_type = game_type
        self._on_time_end = on_time_end

        team = random.randint(0, 1)
        if team == 0:
            self.teams[player1] = Team.WHITE
            self.teams[player2] = Team.BLACK
        else:
            self.teams[player1] = Team.BLACK
            self.teams[player2] = Team.WHITE

        self._engine = ChessEngine()
        self.timer = GameTimer(TIMES[game_type], self._on_team_time_end)

    def clean(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None

        self._engine = None
        self._draw_offer = None
        self.game_type = None
        self.teams = {}

    def on_surrender(self, player: Player) -> Optional[GameEndStatus]:
        if not self.running:
            return None

        winner = self._player_by_team(opposite_team(self.teams[player]))
        game_type = self.game_type
        self.clean()
        return GameEndStatus(False, winner, player, game_type)

    def on_draw_offer(self, player: Player) -> bool:
        if not self.running or self._draw_offer or self.teams[player] != self._engine.currently_moving_team:
            return False

        self._draw_offer = player
        return True

    def on_draw_offer_accepted(self, player: Player) -> Optional[GameEndStatus]:
        if not self.running or not self._draw_offer or player == self._draw_offer:
            return None

        players = list(self.teams.keys())
        game_type = self.game_type
        self.clean()
        return GameEndStatus(True, players[0], players[1], game_type)

    def on_draw_offer_rejected(self, player: Player) -> bool:
        if not self.running or not self._draw_offer or player == self._draw_offer:
            return False

        self._draw_offer = None
        return True

    def on_draw_claim(self, player: Player) -> Optional[GameEndStatus]:
        if not self.running or self.teams[player] != self._engine.currently_moving_team \
                or not self._engine.can_claim_draw():
            return None

        players = list(self.teams.keys())
        game_type = self.game_type
        self.clean()
        return GameEndStatus(True, players[0], players[1], game_type)

    def on_move(self, move: AbstractMove, player: Player) -> MoveStatus:
        if not self.running or self.teams[player] != self._engine.currently_moving_team \
                or not self._engine.validate_move(move):
            return MoveStatus(False, -1)

        self._engine.process_move(move)

        game_type = self.game_type
        opposite_player = self._opposite_player(player)

        time_left = self.timer.next()

        if self._engine.is_checkmate():
            self.clean()
            return MoveStatus(True, time_left, GameEndStatus(False, player, opposite_player, game_type))
        elif self._engine.is_tie():
            self.clean()
            return MoveStatus(True, time_left, GameEndStatus(True, player, opposite_player, game_type))

        if self._draw_offer and self._draw_offer != player:
            self._draw_offer = None

        return MoveStatus(True, time_left)

    async def _on_team_time_end(self, team: Team):
        if not self.running:
            return

        player = self._player_by_team(self.timer.current_team)
        opposite = self._opposite_player(player)
        game_type = self.game_type

        self._draw_offer = None
        self.game_type = None

        if self._engine.has_sufficient_material(self.teams[opposite]):
            await self._on_time_end(GameEndStatus(False, opposite, player, game_type))
        else:
            await self._on_time_end(GameEndStatus(True, opposite, player, game_type))

        self.timer.cancel()
        self.teams = {}
        self._engine = None
        self.timer = None

    def _opposite_player(self, player: Player) -> Player:
        return self._player_by_team(opposite_team(self.teams[player]))

    def _player_by_team(self, team: Team) -> Player:
        for p, t in self.teams.items():
            if team == t:
                return p
