"""Application configuration via Pydantic Settings."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Global application settings, loaded from environment variables / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ─── Application ───
    app_name: str = "runtime-agent"
    app_env: str = "development"
    app_debug: bool = False
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    # ─── Database ───
    database_url: str = "postgresql+asyncpg://agent:agent@localhost:5432/agent_runtime"
    database_pool_size: int = 20
    database_echo: bool = False

    # ─── Redis ───
    redis_url: str = "redis://localhost:6379/0"
    redis_session_ttl: int = 3600

    # ─── LLM ───
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    default_llm_provider: str = "openai"
    default_llm_model: str = "gpt-4o"

    # ─── Memory ───
    memory_working_window_size: int = 20
    memory_semantic_embedding_model: str = "text-embedding-3-small"
    memory_semantic_top_k: int = 5
    memory_episodic_max_recall: int = 10

    # ─── Security ───
    api_key_header: str = "X-API-Key"
    api_keys: list[str] = Field(default_factory=lambda: ["dev-key-1"])

    # ─── Observability ───
    log_level: str = "INFO"
    log_format: str = "json"
    otel_enabled: bool = False
    otel_exporter_endpoint: str = "http://localhost:4317"

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
