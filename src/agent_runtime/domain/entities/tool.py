"""Tool definition — schema and metadata for an executable tool."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from agent_runtime.domain.value_objects import ToolCallId, ToolCallStatus, new_tool_call_id, utc_now


@dataclass(frozen=True)
class ToolDefinition:
    """Describes a tool that an agent can invoke."""

    name: str
    description: str
    parameters_schema: dict[str, Any] = field(default_factory=dict)
    required_parameters: list[str] = field(default_factory=list)
    enabled: bool = True

    def to_llm_format(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": self.parameters_schema,
                    "required": self.required_parameters,
                },
            },
        }


@dataclass
class ToolCallRecord:
    """Records the execution of a single tool call."""

    id: ToolCallId = field(default_factory=new_tool_call_id)
    tool_name: str = ""
    arguments: dict[str, Any] = field(default_factory=dict)
    result: Any = None
    status: ToolCallStatus = ToolCallStatus.PENDING
    error: str | None = None
    duration_ms: int = 0
    created_at: datetime = field(default_factory=utc_now)

    def mark_success(self, result: Any, duration_ms: int) -> None:
        self.result = result
        self.status = ToolCallStatus.SUCCESS
        self.duration_ms = duration_ms

    def mark_failure(self, error: str, duration_ms: int) -> None:
        self.error = error
        self.status = ToolCallStatus.FAILURE
        self.duration_ms = duration_ms
