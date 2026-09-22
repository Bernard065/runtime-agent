"""Memory entry entity — a unit of agent memory across the four tiers."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
import uuid

from agent_runtime.domain.value_objects import (
    AgentId,
    MemoryId,
    MemoryType,
    SessionId,
    new_memory_id,
    utc_now,
)


@dataclass
class MemoryEntry:
    """A single memory record in any of the four memory tiers."""

    id: MemoryId = field(default_factory=new_memory_id)
    agent_id: AgentId = field(default_factory=lambda: AgentId(uuid.uuid4()))
    session_id: SessionId | None = None
    memory_type: MemoryType = MemoryType.EPISODIC
    content: str = ""
    embedding: list[float] | None = None
    importance_score: float = 0.5
    metadata: dict[str, Any] = field(default_factory=dict)
    version: int = 1
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
    expires_at: datetime | None = None

    @property
    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return utc_now() >= self.expires_at

    def bump_importance(self, delta: float = 0.1) -> None:
        self.importance_score = min(1.0, self.importance_score + delta)
        self.updated_at = utc_now()

    def increment_version(self) -> None:
        self.version += 1
        self.updated_at = utc_now()
