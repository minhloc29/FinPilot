from pydantic_settings import BaseSettings
from typing import Dict, List, Optional


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "AI Financial Copilot"
    DEBUG: bool = False

    API_ENDPOINT: str = ""
    API_KEY: str = ""

    # MODAS compatibility fields (OpenAI-compatible API)
    MODAS_API_ENDPOINT: Optional[str] = None
    MODAS_API_KEY: Optional[str] = None

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/financial_copilot"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000", "http://localhost:8000", "http://localhost:8080", "http://localhost:5173"
    ]

    # LLM Configuration (legacy, kept for compatibility)
    DEFAULT_MODEL: str = "gemma-3-27b-it"
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 2000

    # Provider keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    XAI_API_KEY: Optional[str] = None
    OPENROUTER_API_KEY: Optional[str] = None
    ALPHA_VANTAGE_API_KEY: Optional[str] = None

    # TradingAgents runtime
    TRADINGAGENTS_ENABLED: bool = True
    TRADINGAGENTS_LLM_PROVIDER: str = "openai"
    # gpt-oss-120b: deep reasoning - Research Manager, Portfolio Manager
    TRADINGAGENTS_DEEP_MODEL: str = "gpt-oss-120b"
    # gpt-oss-20b: fast - individual Analysts (market, news, fundamentals, social)
    TRADINGAGENTS_QUICK_MODEL: str = "gpt-oss-20b"
    TRADINGAGENTS_BACKEND_URL: str = "https://mkp-api.fptcloud.com/v1"
    TRADINGAGENTS_SELECTED_ANALYSTS: str = "market,social,news,fundamentals"
    TRADINGAGENTS_MAX_DEBATE_ROUNDS: int = 1
    TRADINGAGENTS_MAX_RISK_DISCUSS_ROUNDS: int = 1
    TRADINGAGENTS_RESULTS_DIR: str = "./results"
    TRADINGAGENTS_PROJECT_DIR: str = ""
    TRADINGAGENTS_DATA_VENDORS: str = "vnstock,yfinance"
    TRADINGAGENTS_OPENAI_REASONING_EFFORT: Optional[str] = None
    TRADINGAGENTS_GOOGLE_THINKING_LEVEL: Optional[str] = None
    TRADINGAGENTS_ANTHROPIC_EFFORT: Optional[str] = None

    # Small-model services for chat input/output normalization
    CHAT_INPUT_MODEL_ENABLED: bool = True
    CHAT_OUTPUT_MODEL_ENABLED: bool = True
    # Orchestrator: gpt-oss-120b for accurate intent classification
    CHAT_INPUT_MODEL_NAME: str = "gpt-oss-120b"
    # Formatter: gpt-oss-20b fast enough to clean output text
    CHAT_OUTPUT_MODEL_NAME: str = "gpt-oss-20b"
    CHAT_MODEL_BACKEND_URL: str = "https://mkp-api.fptcloud.com/v1"
    CHAT_MODEL_TIMEOUT_SECONDS: int = 30

    @property
    def effective_openai_api_key(self) -> Optional[str]:
        return self.MODAS_API_KEY or self.OPENAI_API_KEY

    @property
    def effective_trading_backend_url(self) -> str:
        return self._normalize_backend_url(
            self.MODAS_API_ENDPOINT or self.TRADINGAGENTS_BACKEND_URL or "https://api.openai.com/v1"
        )

    @property
    def effective_chat_backend_url(self) -> str:
        return self._normalize_backend_url(
            self.MODAS_API_ENDPOINT or self.CHAT_MODEL_BACKEND_URL or self.TRADINGAGENTS_BACKEND_URL
        )

    @staticmethod
    def _normalize_backend_url(url: Optional[str]) -> str:
        candidate = (url or "https://api.openai.com/v1").strip().rstrip("/")
        if candidate.endswith("/v1"):
            return candidate
        return f"{candidate}/v1"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
