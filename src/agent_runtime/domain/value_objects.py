"""Domain value objects — enums, typed identifiers, and constants."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import StrEnum
from typing import NewType

# ─── Typed Identifiers ──────────────────────────────
AgentId = NewType("AgentId", uuid.UUID)
SessionId = NewType("SessionId", uuid.UUID)
MessageId = NewType("MessageId", uuid.UUID)
MemoryId = NewType("MemoryId", uuid.UUID)
ToolCallId = NewType("ToolCallId", uuid.UUID)


def new_agent_id() -> AgentId:
    return AgentId(uuid.uuid4())


def new_session_id() -> SessionId:
    return SessionId(uuid.uuid4())


def new_message_id() -> MessageId:
    return MessageId(uuid.uuid4())


def new_memory_id() -> MemoryId:
    return MemoryId(uuid.uuid4())


def new_tool_call_id() -> ToolCallId:
    return ToolCallId(uuid.uuid4())


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


# ─── Enums ───────────────────────────────────────────
class AgentState(StrEnum):
    """States in the agent execution FSM."""

    IDLE = "idle"
    RECEIVING = "receiving"
    THINKING = "thinking"
    PLANNING = "planning"
    EXECUTING = "executing"
    RESPONDING = "responding"
    ERROR = "error"


class SessionStatus(StrEnum):
    """Lifecycle status of a session."""

    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"


class MessageRole(StrEnum):
    """Role of a message in the conversation."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class MemoryType(StrEnum):
    """Categories of agent memory."""

    WORKING = "working"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"


class ToolCallStatus(StrEnum):
    """Execution status of a tool call."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"
    TIMEOUT = "timeout"
