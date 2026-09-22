"""FastAPI application entrypoint."""

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agent_runtime.core.config import settings
from agent_runtime.core.logging import setup_logging, get_logger
from agent_runtime.core.telemetry import setup_telemetry

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan — startup and shutdown hooks."""
    setup_logging(log_level=settings.log_level, log_format=settings.log_format)
    setup_telemetry(
        service_name=settings.app_name,
        enabled=settings.otel_enabled,
        exporter_endpoint=settings.otel_exporter_endpoint,
    )
    logger.info("application_starting", app_name=settings.app_name, env=settings.app_env)
    yield
    logger.info("application_stopped")


def create_app() -> FastAPI:
    """Application factory."""
    application = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="AI Agent Runtime with state, session, and memory management",
        lifespan=lifespan,
        docs_url="/docs" if settings.app_debug else None,
        redoc_url="/redoc" if settings.app_debug else None,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if not settings.is_production else [],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Stub health route (available immediately) ──
    from agent_runtime.api.v1.health import router as health_router

    application.include_router(health_router, tags=["Health"])

    return application


app = create_app()
