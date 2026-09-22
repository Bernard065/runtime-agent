# Runtime Agent Framework

A production-grade AI agent runtime with state management, session persistence, multi-tier memory, and tool orchestration.

## Features

- **Stateful Execution** — Finite state machine with checkpointing and resume
- **Session Management** — Create, persist, and resume agent sessions
- **4-Tier Memory** — Working, Episodic, Semantic (vector), and Procedural memory
- **Tool System** — Pluggable tools with schema validation and sandboxed execution
- **Streaming** — Real-time WebSocket streaming of tokens and events
- **Observability** — Structured logging, OpenTelemetry tracing, Prometheus metrics

## Tech Stack

| Layer | Technology |
|:---|:---|
| Runtime | Python 3.12+ |
| API | FastAPI + Pydantic v2 |
| Database | PostgreSQL 16 + pgvector |
| Cache | Redis 7 |
| LLM | OpenAI, Anthropic (pluggable) |
| Deploy | Docker Compose |

## Quick Start

```bash
# 1. Clone and install
git clone <repo-url>
cd runtime-agent
pip install -e ".[dev]"

# 2. Copy env and configure
cp .env.example .env

# 3. Start infrastructure
make docker-up

# 4. Run migrations
make db-migrate

# 5. Start the server
make run
```

API docs at `http://localhost:8000/docs`.

## Development

```bash
make dev           # Install dev dependencies
make lint          # Run linter
make format        # Auto-format code
make test          # Run all tests
make test-unit     # Run only unit tests
```

## Project Structure

```
src/agent_runtime/
├── api/            # FastAPI routes, middleware, WebSocket
├── application/    # Use cases, runtime engine, managers
├── domain/         # Entities, state machine, events (pure Python)
├── infrastructure/ # DB, Redis, LLM adapters, tools
└── core/           # Config, logging, telemetry
```
