from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional


class SessionState(str, Enum):
    WORK = "work"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"


@dataclass
class TimerEvent:
    event_type: str
    from_state: SessionState
    to_state: SessionState
    cycle_count: int


class TimerEngine:
    def __init__(
        self,
        work_minutes: int,
        short_break_minutes: int,
        long_break_minutes: int,
        auto_start_break: bool = True,
        auto_start_work: bool = True,
        on_transition: Optional[Callable[[TimerEvent], None]] = None,
    ) -> None:
        self.work_minutes = work_minutes
        self.short_break_minutes = short_break_minutes
        self.long_break_minutes = long_break_minutes
        self.auto_start_break = auto_start_break
        self.auto_start_work = auto_start_work
        self.on_transition = on_transition

        self.state = SessionState.WORK
        self.is_running = False
        self.cycle_count = 0
        self.remaining_seconds = self._minutes_to_seconds(self.work_minutes)

    def start(self) -> None:
        self.is_running = True

    def pause(self) -> None:
        self.is_running = False

    def reset(self) -> None:
        self.state = SessionState.WORK
        self.is_running = False
        self.cycle_count = 0
        self.remaining_seconds = self._minutes_to_seconds(self.work_minutes)

    def skip_break(self) -> Optional[TimerEvent]:
        if self.state not in (SessionState.SHORT_BREAK, SessionState.LONG_BREAK):
            return None
        return self._transition_to(SessionState.WORK, auto_start=self.auto_start_work)

    def start_break(self) -> Optional[TimerEvent]:
        if self.state != SessionState.WORK:
            return None
        return self._transition_to(SessionState.SHORT_BREAK, auto_start=True)

    def tick(self) -> Optional[TimerEvent]:
        if not self.is_running:
            return None
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
        if self.remaining_seconds <= 0:
            return self._handle_session_complete()
        return None

    def update_settings(
        self,
        work_minutes: int,
        short_break_minutes: int,
        long_break_minutes: int,
        auto_start_break: bool,
        auto_start_work: bool,
    ) -> None:
        self.work_minutes = work_minutes
        self.short_break_minutes = short_break_minutes
        self.long_break_minutes = long_break_minutes
        self.auto_start_break = auto_start_break
        self.auto_start_work = auto_start_work
        if self.state == SessionState.WORK:
            self.remaining_seconds = self._minutes_to_seconds(self.work_minutes)
        elif self.state == SessionState.SHORT_BREAK:
            self.remaining_seconds = self._minutes_to_seconds(self.short_break_minutes)
        elif self.state == SessionState.LONG_BREAK:
            self.remaining_seconds = self._minutes_to_seconds(self.long_break_minutes)

    def _handle_session_complete(self) -> Optional[TimerEvent]:
        if self.state == SessionState.WORK:
            self.cycle_count += 1
            next_state = self._next_break_state()
            auto_start = self.auto_start_break
        else:
            next_state = SessionState.WORK
            auto_start = self.auto_start_work
        return self._transition_to(next_state, auto_start=auto_start)

    def _next_break_state(self) -> SessionState:
        if self.cycle_count % 10 == 0:
            return SessionState.LONG_BREAK
        if self.cycle_count % 5 == 0:
            return SessionState.SHORT_BREAK
        return SessionState.WORK

    def _transition_to(self, next_state: SessionState, auto_start: bool) -> TimerEvent:
        previous_state = self.state
        self.state = next_state
        self.is_running = auto_start
        self.remaining_seconds = self._duration_for_state(next_state)
        event = TimerEvent(
            event_type="transition",
            from_state=previous_state,
            to_state=next_state,
            cycle_count=self.cycle_count,
        )
        if self.on_transition:
            self.on_transition(event)
        return event

    def _duration_for_state(self, state: SessionState) -> int:
        if state == SessionState.WORK:
            return self._minutes_to_seconds(self.work_minutes)
        if state == SessionState.SHORT_BREAK:
            return self._minutes_to_seconds(self.short_break_minutes)
        return self._minutes_to_seconds(self.long_break_minutes)

    @staticmethod
    def _minutes_to_seconds(value: int) -> int:
        return max(1, int(value)) * 60
