"""Domain-specific exceptions."""

from __future__ import annotations

from agent_runtime.domain.value_objects import AgentState


class DomainError(Exception):
    """Base class for all domain errors."""

    def __init__(self, message: str, code: str = "DOMAIN_ERROR") -> None:
        self.message = message
        self.code = code
        super().__init__(message)


class InvalidStateTransition(DomainError):
    def __init__(self, current: AgentState, target: AgentState, trigger: str) -> None:
        self.current_state = current
        self.target_state = target
        self.trigger = trigger
        super().__init__(
            f"Invalid transition: {current} → {target} (trigger: {trigger})",
            code="INVALID_STATE_TRANSITION",
        )


class AgentNotFoundError(DomainError):
    def __init__(self, agent_id: str) -> None:
        super().__init__(f"Agent not found: {agent_id}", code="AGENT_NOT_FOUND")


class SessionNotFoundError(DomainError):
    def __init__(self, session_id: str) -> None:
        super().__init__(f"Session not found: {session_id}", code="SESSION_NOT_FOUND")


class SessionClosedError(DomainError):
    def __init__(self, session_id: str) -> None:
        super().__init__(
            f"Session is closed and cannot accept messages: {session_id}",
            code="SESSION_CLOSED",
        )


class MessageNotFoundError(DomainError):
    def __init__(self, message_id: str) -> None:
        super().__init__(f"Message not found: {message_id}", code="MESSAGE_NOT_FOUND")


class ToolNotFoundError(DomainError):
    def __init__(self, tool_name: str) -> None:
        super().__init__(f"Tool not found: {tool_name}", code="TOOL_NOT_FOUND")


class ToolExecutionError(DomainError):
    def __init__(self, tool_name: str, reason: str) -> None:
        super().__init__(
            f"Tool execution failed '{tool_name}': {reason}",
            code="TOOL_EXECUTION_ERROR",
        )


class ToolValidationError(DomainError):
    def __init__(self, tool_name: str, errors: str) -> None:
        super().__init__(
            f"Invalid arguments for tool '{tool_name}': {errors}",
            code="TOOL_VALIDATION_ERROR",
        )


class MaxIterationsExceededError(DomainError):
    def __init__(self, max_iterations: int) -> None:
        super().__init__(
            f"Agent exceeded maximum iterations ({max_iterations})",
            code="MAX_ITERATIONS_EXCEEDED",
        )


class MemoryNotFoundError(DomainError):
    def __init__(self, memory_id: str) -> None:
        super().__init__(f"Memory entry not found: {memory_id}", code="MEMORY_NOT_FOUND")
