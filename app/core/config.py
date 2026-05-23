"""Application settings loaded from environment / .env file."""
import secrets
import json
from typing import List, Any
from pydantic import Field, field_validator
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
    secret_key: str = Field(default_factory=lambda: secrets.token_hex(32))
    debug: bool = False
    log_level: str = "info"

    @field_validator("secret_key")
    @classmethod
    def secret_key_must_be_secure(cls, v: str) -> str:
        if v == "changeme":
            raise ValueError(
                "Insecure SECRET_KEY detected. Please set a secure SECRET_KEY "
                "in your environment or .env file."
            )
        return v

    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v: Any) -> List[str]:
        if isinstance(v, str):
            v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    pass
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v


settings = Settings()
