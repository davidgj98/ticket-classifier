from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ollama_url: str = "http://localhost:11434"
    default_model: str = "qwen2.5:3b"
    database_url: str = "sqlite+aiosqlite:///data/history.db"
    app_title: str = "IT Ticket Classifier"
    app_version: str = "2.0.0"
    request_timeout: float = 60.0
    health_timeout: float = 5.0
    models_timeout: float = 10.0
    log_level: str = "INFO"

    model_config = {"env_prefix": "TICKET_", "env_file": ".env"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
