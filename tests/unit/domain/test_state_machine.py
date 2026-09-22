"""Unit tests for the agent FSM."""

import pytest

from agent_runtime.domain.state_machine import StateMachine
from agent_runtime.domain.value_objects import AgentState
from agent_runtime.domain.errors import InvalidStateTransition


@pytest.mark.unit
class TestStateMachine:
    def test_initial_state_is_idle(self):
        sm = StateMachine()
        assert sm.current_state == AgentState.IDLE

    def test_full_direct_response_cycle(self):
        sm = StateMachine(session_id="test-session")
        e1 = sm.transition("user_message")
        assert sm.current_state == AgentState.RECEIVING
        assert e1.previous_state == AgentState.IDLE

        sm.transition("message_parsed")
        assert sm.current_state == AgentState.THINKING

        sm.transition("direct_response")
        assert sm.current_state == AgentState.RESPONDING

        sm.transition("response_sent")
        assert sm.current_state == AgentState.IDLE

    def test_tool_use_cycle(self):
        sm = StateMachine()
        sm.transition("user_message")
        sm.transition("message_parsed")
        sm.transition("needs_tool_use")
        assert sm.current_state == AgentState.PLANNING

        sm.transition("tool_selected")
        assert sm.current_state == AgentState.EXECUTING

        sm.transition("tool_result")
        assert sm.current_state == AgentState.THINKING

        sm.transition("direct_response")
        sm.transition("response_sent")
        assert sm.current_state == AgentState.IDLE

    def test_error_and_retry(self):
        sm = StateMachine()
        sm.transition("user_message")
        sm.transition("message_parsed")
        sm.transition("needs_tool_use")
        sm.transition("tool_selected")
        sm.transition("tool_failure")
        assert sm.current_state == AgentState.ERROR

        sm.transition("retry")
        assert sm.current_state == AgentState.THINKING

    def test_error_max_retries(self):
        sm = StateMachine()
        sm.transition("user_message")
        sm.transition("message_parsed")
        sm.transition("needs_tool_use")
        sm.transition("tool_selected")
        sm.transition("tool_failure")
        sm.transition("max_retries")
        assert sm.current_state == AgentState.RESPONDING

    def test_invalid_transition_raises(self):
        sm = StateMachine()
        with pytest.raises(InvalidStateTransition) as exc_info:
            sm.transition("tool_result")
        assert exc_info.value.current_state == AgentState.IDLE

    def test_valid_triggers(self):
        sm = StateMachine()
        assert sm.valid_triggers == ["user_message"]
        sm.transition("user_message")
        assert sm.valid_triggers == ["message_parsed"]

    def test_can_transition(self):
        sm = StateMachine()
        assert sm.can_transition("user_message") is True
        assert sm.can_transition("tool_result") is False

    def test_history_tracking(self):
        sm = StateMachine(session_id="sess-1")
        sm.transition("user_message")
        sm.transition("message_parsed")
        sm.transition("direct_response")
        assert len(sm.history) == 3
        assert sm.history[0].session_id == "sess-1"

    def test_reset(self):
        sm = StateMachine()
        sm.transition("user_message")
        sm.transition("message_parsed")
        sm.reset()
        assert sm.current_state == AgentState.IDLE
        assert sm.history == []
