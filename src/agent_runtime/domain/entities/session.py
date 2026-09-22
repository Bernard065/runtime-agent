"""Session entity — a conversation context between a user and an agent."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
import uuid

from agent_runtime.domain.value_objects import (
    AgentId,
    AgentState,
    SessionId,
    SessionStatus,
    new_session_id,
    utc_now,
)


@dataclass
class Session:
    """A session tracks the lifecycle and state of one agent conversation."""

    id: SessionId = field(default_factory=new_session_id)
    agent_id: AgentId = field(default_factory=lambda: AgentId(uuid.uuid4()))
    status: SessionStatus = SessionStatus.ACTIVE
    current_state: AgentState = AgentState.IDLE
    step_number: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    @property
    def is_active(self) -> bool:
        return self.status == SessionStatus.ACTIVE

    def advance_step(self) -> None:
        self.step_number += 1
        self.updated_at = utc_now()

    def transition_state(self, new_state: AgentState) -> None:
        self.current_state = new_state
        self.updated_at = utc_now()

    def close(self, status: SessionStatus = SessionStatus.COMPLETED) -> None:
        self.status = status
        self.current_state = AgentState.IDLE
        self.updated_at = utc_now()

    def pause(self) -> None:
        self.status = SessionStatus.PAUSED
        self.updated_at = utc_now()

    def resume(self) -> None:
        self.status = SessionStatus.ACTIVE
        self.updated_at = utc_now()
