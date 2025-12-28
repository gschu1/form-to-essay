"""Application settings and configuration."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env file explicitly (works on Windows)
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o-mini"
    openai_max_output_tokens: Optional[int] = None  # Optional override for max output tokens
    provider: str = "mock"  # "mock" or "openai"
    output_base_dir: Path = Path("outputs")
    policy_path: Path = Path("config/policy.yaml")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    def get_provider_type(self) -> str:
        """Determine which provider to use based on PROVIDER env var or credentials."""
        provider = self.provider.lower()
        if provider == "openai":
            if not self.openai_api_key:
                raise ValueError(
                    "PROVIDER=openai requires OPENAI_API_KEY to be set. "
                    "Please set it in your .env file or environment."
                )
            return "openai"
        return "mock"


def get_settings() -> Settings:
    """Get application settings singleton."""
    return Settings()

