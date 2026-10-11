from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str = "sqlite:///./local.db"
    jwt_secret: str = ""
    openrouter_api_key: str = ""
    openrouter_model: str = "openai/gpt-4o-mini"
    openrouter_base_url: str = "https://openrouter.ai/api/v1/chat/completions"
    app_origin: str = ""
    openrouter_timeout_seconds: float = 20.0


@lru_cache
def get_settings() -> Settings:
    return Settings()
