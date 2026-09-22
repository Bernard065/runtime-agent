"""Domain events — immutable records of things that happened."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
import uuid

from agent_runtime.domain.value_objects import AgentState, utc_now


@dataclass(frozen=True)
class DomainEvent:
    """Base class for all domain events."""

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=utc_now)

    @property
    def event_type(self) -> str:
        return self.__class__.__name__


@dataclass(frozen=True)
class StateChanged(DomainEvent):
    session_id: str = ""
    previous_state: AgentState = AgentState.IDLE
    new_state: AgentState = AgentState.IDLE
    trigger: str = ""


@dataclass(frozen=True)
class MessageReceived(DomainEvent):
    session_id: str = ""
    message_id: str = ""
    content_preview: str = ""


@dataclass(frozen=True)
class ResponseGenerated(DomainEvent):
    session_id: str = ""
    message_id: str = ""
    token_count: int = 0


@dataclass(frozen=True)
class ToolCallStarted(DomainEvent):
    session_id: str = ""
    tool_name: str = ""
    arguments: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ToolCallCompleted(DomainEvent):
    session_id: str = ""
    tool_name: str = ""
    status: str = "success"
    duration_ms: int = 0


@dataclass(frozen=True)
class SessionCreated(DomainEvent):
    session_id: str = ""
    agent_id: str = ""


@dataclass(frozen=True)
class SessionClosed(DomainEvent):
    session_id: str = ""
    reason: str = ""
    total_messages: int = 0


@dataclass(frozen=True)
class MemoryStored(DomainEvent):
    memory_id: str = ""
    memory_type: str = ""
    agent_id: str = ""


@dataclass(frozen=True)
class ErrorOccurred(DomainEvent):
    session_id: str = ""
    error_code: str = ""
    error_message: str = ""
    step_number: int = 0
