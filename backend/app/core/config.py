"""
Application configuration settings
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "AI Financial Copilot"
    DEBUG: bool = False

    # API Keys
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    ANTHROPIC_API_KEY: str = ""
    ALPHA_VANTAGE_API_KEY: str = ""

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/financial_copilot"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000", "http://localhost:8000"]

    # LLM Configuration
    DEFAULT_MODEL: str = "gpt-4"
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 2000

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
