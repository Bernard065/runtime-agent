.PHONY: install dev lint format typecheck test test-unit test-integration test-e2e run clean

# ─── Setup ───────────────────────────────────────────
install:
	pip install -e .

dev:
	pip install -e ".[dev]"

# ─── Code Quality ────────────────────────────────────
lint:
	ruff check src/ tests/
	ruff format --check src/ tests/

format:
	ruff check --fix src/ tests/
	ruff format src/ tests/

typecheck:
	mypy src/

# ─── Testing ─────────────────────────────────────────
test:
	pytest -v --tb=short

test-unit:
	pytest -v --tb=short -m unit

test-integration:
	pytest -v --tb=short -m integration

test-e2e:
	pytest -v --tb=short -m e2e

test-cov:
	pytest --cov=agent_runtime --cov-report=html --cov-report=term-missing

# ─── Run ─────────────────────────────────────────────
run:
	uvicorn agent_runtime.main:app --host 0.0.0.0 --port 8000 --reload

# ─── Docker ──────────────────────────────────────────
docker-up:
	docker compose -f docker/docker-compose.yml up -d

docker-down:
	docker compose -f docker/docker-compose.yml down -v

docker-build:
	docker compose -f docker/docker-compose.yml build

# ─── Database ────────────────────────────────────────
db-migrate:
	alembic upgrade head

db-rollback:
	alembic downgrade -1

db-revision:
	alembic revision --autogenerate -m "$(msg)"

# ─── Cleanup ─────────────────────────────────────────
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	rm -rf htmlcov .coverage
