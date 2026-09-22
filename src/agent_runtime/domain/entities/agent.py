"""Agent entity — the core identity and configuration of an agent."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from agent_runtime.domain.value_objects import AgentId, new_agent_id, utc_now


@dataclass
class Agent:
    """An agent: a configured AI persona with a system prompt, model, and tools."""

    id: AgentId = field(default_factory=new_agent_id)
    name: str = "default-agent"
    description: str = ""
    system_prompt: str = "You are a helpful AI assistant."
    model: str = "gpt-4o"
    provider: str = "openai"
    config: dict[str, Any] = field(default_factory=dict)
    tool_names: list[str] = field(default_factory=list)
    max_iterations: int = 10
    temperature: float = 0.7
    max_tokens: int = 4096
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def update(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ("id", "created_at"):
                setattr(self, key, value)
        self.updated_at = utc_now()
