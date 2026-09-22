"""Finite State Machine for agent execution control flow."""

from __future__ import annotations

from dataclasses import dataclass, field

from agent_runtime.domain.errors import InvalidStateTransition
from agent_runtime.domain.events import StateChanged
from agent_runtime.domain.value_objects import AgentState


# ─── Transition Table ────────────────────────────────
_TRANSITIONS: dict[tuple[AgentState, str], AgentState] = {
    (AgentState.IDLE, "user_message"): AgentState.RECEIVING,
    (AgentState.RECEIVING, "message_parsed"): AgentState.THINKING,
    (AgentState.THINKING, "needs_tool_use"): AgentState.PLANNING,
    (AgentState.THINKING, "direct_response"): AgentState.RESPONDING,
    (AgentState.PLANNING, "tool_selected"): AgentState.EXECUTING,
    (AgentState.EXECUTING, "tool_result"): AgentState.THINKING,
    (AgentState.EXECUTING, "tool_failure"): AgentState.ERROR,
    (AgentState.ERROR, "retry"): AgentState.THINKING,
    (AgentState.ERROR, "max_retries"): AgentState.RESPONDING,
    (AgentState.RESPONDING, "response_sent"): AgentState.IDLE,
}


@dataclass
class StateMachine:
    """Deterministic FSM governing the agent execution lifecycle."""

    current_state: AgentState = AgentState.IDLE
    session_id: str = ""
    history: list[StateChanged] = field(default_factory=list)

    @property
    def valid_triggers(self) -> list[str]:
        return [trigger for (state, trigger) in _TRANSITIONS if state == self.current_state]

    def can_transition(self, trigger: str) -> bool:
        return (self.current_state, trigger) in _TRANSITIONS

    def transition(self, trigger: str) -> StateChanged:
        key = (self.current_state, trigger)
        if key not in _TRANSITIONS:
            raise InvalidStateTransition(
                current=self.current_state,
                target=AgentState.IDLE,
                trigger=trigger,
            )

        previous = self.current_state
        self.current_state = _TRANSITIONS[key]

        event = StateChanged(
            session_id=self.session_id,
            previous_state=previous,
            new_state=self.current_state,
            trigger=trigger,
        )
        self.history.append(event)
        return event

    def reset(self) -> None:
        self.current_state = AgentState.IDLE
        self.history.clear()
