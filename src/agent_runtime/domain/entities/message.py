"""Message value object — a single message in the conversation."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
import uuid

from agent_runtime.domain.value_objects import (
    MessageId,
    MessageRole,
    SessionId,
    new_message_id,
    utc_now,
)


@dataclass(frozen=True)
class ToolCallRequest:
    """A request from the LLM to invoke a tool."""

    id: str
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class Message:
    """An immutable message in the conversation history."""

    id: MessageId = field(default_factory=new_message_id)
    session_id: SessionId = field(
        default_factory=lambda: SessionId(uuid.uuid4())
    )
    role: MessageRole = MessageRole.USER
    content: str = ""
    tool_calls: list[ToolCallRequest] = field(default_factory=list)
    tool_call_id: str | None = None
    token_count: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=utc_now)

    def to_llm_format(self) -> dict[str, Any]:
        msg: dict[str, Any] = {"role": self.role.value, "content": self.content}
        if self.tool_calls:
            msg["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.name, "arguments": str(tc.arguments)},
                }
                for tc in self.tool_calls
            ]
        if self.tool_call_id:
            msg["tool_call_id"] = self.tool_call_id
        return msg
