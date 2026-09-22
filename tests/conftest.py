"""Shared test fixtures."""

import pytest

from agent_runtime.domain.entities.agent import Agent
from agent_runtime.domain.entities.session import Session
from agent_runtime.domain.entities.message import Message
from agent_runtime.domain.value_objects import (
    AgentId,
    SessionId,
    MessageRole,
    new_agent_id,
    new_session_id,
)


@pytest.fixture
def agent_id() -> AgentId:
    return new_agent_id()


@pytest.fixture
def session_id() -> SessionId:
    return new_session_id()


@pytest.fixture
def sample_agent(agent_id: AgentId) -> Agent:
    return Agent(
        id=agent_id,
        name="test-agent",
        description="A test agent",
        system_prompt="You are a test assistant.",
    )


@pytest.fixture
def sample_session(session_id: SessionId, agent_id: AgentId) -> Session:
    return Session(id=session_id, agent_id=agent_id)


@pytest.fixture
def sample_user_message(session_id: SessionId) -> Message:
    return Message(session_id=session_id, role=MessageRole.USER, content="Hello, agent!")
