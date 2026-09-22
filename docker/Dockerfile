# ── Stage 1: Builder ──
FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir hatchling

COPY pyproject.toml README.md ./
COPY src/ src/

RUN pip install --no-cache-dir --prefix=/install .

# ── Stage 2: Runtime ──
FROM python:3.12-slim AS runtime

WORKDIR /app

# Security: non-root user
RUN groupadd -r agent && useradd -r -g agent agent

COPY --from=builder /install /usr/local
COPY alembic/ alembic/
COPY alembic.ini .
COPY src/ src/

RUN chown -R agent:agent /app
USER agent

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health').raise_for_status()"

CMD ["uvicorn", "agent_runtime.main:app", "--host", "0.0.0.0", "--port", "8000"]
