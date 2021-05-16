import asyncio
import time
from asyncio import Future
from typing import Optional, Coroutine, Callable

from shared.chess_engine.piece import Team, opposite_team

FIRST_MOVE_TIME_MS = 30


class GameTimer:
    def __init__(self, team_time: int, on_time_end: Callable[[Team], Coroutine]):
        self.times_left: dict[Team, int] = {Team.WHITE: team_time, Team.BLACK: team_time}
        self.current_team: Optional[Team] = None
        self._current_job: Optional[Future] = None
        self._move_start = 0
        self._is_first_move = False
        self._on_time_end = on_time_end

        self._start()

    def next(self) -> int:
        self._current_job.cancel()
        now = time.time_ns()

        if self._is_first_move:
            self._is_first_move = False
        else:
            time_passed = (now - self._move_start)
            self.times_left[self.current_team] -= time_passed

        time_left = self.times_left[self.current_team]

        self.current_team = opposite_team(self.current_team)
        self._move_start = now
        self._measure(self.times_left[self.current_team])

        return time_left

    def cancel(self):
        self._current_job.cancel()

    def _start(self):
        self._measure(FIRST_MOVE_TIME_MS)
        self._is_first_move = True
        self.current_team = Team.WHITE

    def _measure(self, delay_ms: int):
        self._current_job = asyncio.ensure_future(self._call_after_delay(delay_ms))

    async def _call_after_delay(self, delay_ms: int):
        await asyncio.sleep(delay_ms / 1000)
        await self._on_time_end(self.current_team)
