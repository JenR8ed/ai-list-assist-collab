"""Application settings loaded from environment / .env file."""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Google AI
    google_api_key: str = ""
    google_cloud_project: str = ""
    vertex_ai_location: str = "us-central1"

    # eBay
    ebay_app_id: str = ""
    ebay_cert_id: str = ""
    ebay_dev_id: str = ""
    ebay_user_token: str = ""
    ebay_sandbox: bool = True

    # Telegram
    telegram_bot_token: str = ""
    telegram_webhook_url: str = ""

    # Database
    database_url: str = "sqlite+aiosqlite:///./ai_list_assist.db"
    redis_url: str = "redis://localhost:6379/0"

    # Ollama
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llava:7b"

    # App
    secret_key: str
    debug: bool = True
    log_level: str = "info"
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]


settings = Settings()
