"""Unit tests for domain entities."""

import pytest
from datetime import datetime, timezone, timedelta

from agent_runtime.domain.entities.agent import Agent
from agent_runtime.domain.entities.session import Session
from agent_runtime.domain.entities.message import Message, ToolCallRequest
from agent_runtime.domain.entities.memory import MemoryEntry
from agent_runtime.domain.entities.tool import ToolDefinition, ToolCallRecord
from agent_runtime.domain.value_objects import (
    AgentState,
    MessageRole,
    SessionStatus,
    ToolCallStatus,
)


@pytest.mark.unit
class TestAgent:
    def test_create_defaults(self):
        agent = Agent()
        assert agent.name == "default-agent"
        assert agent.model == "gpt-4o"
        assert agent.id is not None

    def test_update_fields(self):
        agent = Agent(name="old")
        agent.update(name="new", temperature=0.9)
        assert agent.name == "new"
        assert agent.temperature == 0.9

    def test_update_ignores_id(self):
        agent = Agent()
        original_id = agent.id
        agent.update(id="nope")
        assert agent.id == original_id


@pytest.mark.unit
class TestSession:
    def test_create_defaults(self):
        session = Session()
        assert session.status == SessionStatus.ACTIVE
        assert session.current_state == AgentState.IDLE

    def test_is_active(self):
        session = Session()
        assert session.is_active is True
        session.close()
        assert session.is_active is False

    def test_advance_step(self):
        session = Session()
        session.advance_step()
        session.advance_step()
        assert session.step_number == 2

    def test_pause_and_resume(self):
        session = Session()
        session.pause()
        assert session.status == SessionStatus.PAUSED
        session.resume()
        assert session.status == SessionStatus.ACTIVE


@pytest.mark.unit
class TestMessage:
    def test_create_user_message(self):
        msg = Message(role=MessageRole.USER, content="Hello")
        assert msg.role == MessageRole.USER
        assert msg.tool_calls == []

    def test_message_is_frozen(self):
        msg = Message(content="test")
        with pytest.raises(AttributeError):
            msg.content = "changed"  # type: ignore[misc]

    def test_to_llm_format_simple(self):
        msg = Message(role=MessageRole.USER, content="Hi")
        assert msg.to_llm_format() == {"role": "user", "content": "Hi"}

    def test_to_llm_format_with_tool_calls(self):
        tc = ToolCallRequest(id="tc-1", name="calc", arguments={"expr": "1+1"})
        msg = Message(role=MessageRole.ASSISTANT, content="", tool_calls=[tc])
        fmt = msg.to_llm_format()
        assert len(fmt["tool_calls"]) == 1
        assert fmt["tool_calls"][0]["function"]["name"] == "calc"


@pytest.mark.unit
class TestMemoryEntry:
    def test_is_expired_true(self):
        entry = MemoryEntry(expires_at=datetime.now(timezone.utc) - timedelta(hours=1))
        assert entry.is_expired is True

    def test_is_expired_false(self):
        entry = MemoryEntry(expires_at=datetime.now(timezone.utc) + timedelta(hours=1))
        assert entry.is_expired is False

    def test_no_expiry(self):
        entry = MemoryEntry(expires_at=None)
        assert entry.is_expired is False

    def test_bump_importance_capped(self):
        entry = MemoryEntry(importance_score=0.9)
        entry.bump_importance(0.5)
        assert entry.importance_score == 1.0


@pytest.mark.unit
class TestToolDefinition:
    def test_to_llm_format(self):
        tool = ToolDefinition(
            name="calc",
            description="Math",
            parameters_schema={"expression": {"type": "string"}},
            required_parameters=["expression"],
        )
        fmt = tool.to_llm_format()
        assert fmt["type"] == "function"
        assert fmt["function"]["name"] == "calc"

    def test_tool_call_record_success(self):
        record = ToolCallRecord(tool_name="calc")
        record.mark_success(result=42, duration_ms=15)
        assert record.status == ToolCallStatus.SUCCESS
        assert record.result == 42

    def test_tool_call_record_failure(self):
        record = ToolCallRecord(tool_name="calc")
        record.mark_failure(error="oops", duration_ms=5)
        assert record.status == ToolCallStatus.FAILURE
