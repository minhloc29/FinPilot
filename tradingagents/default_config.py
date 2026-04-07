import os

DEFAULT_CONFIG = {
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results"),
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    # LLM settings
    "llm_provider": "openai",
    # gpt-oss-120b: for deep reasoning (Research Manager, Portfolio Manager)
    "deep_think_llm": "gpt-oss-120b",
    # gpt-oss-20b: for fast analysts (market, news, social, fundamentals)
    "quick_think_llm": "gpt-oss-20b",
    "backend_url": "https://mkp-api.fptcloud.com/v1",
    # Provider-specific thinking configuration
    "google_thinking_level": None,      # "high", "minimal", etc.
    "openai_reasoning_effort": None,    # "medium", "high", "low"
    "anthropic_effort": None,           # "high", "medium", "low"
    # Debate and discussion settings
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "max_recur_limit": 100,
    # Data vendor configuration
    # Category-level configuration (default for all tools in category)
    "data_vendors": {
        "core_stock_apis": "vnstock,yfinance",       # Options: vnstock, alpha_vantage, yfinance
        "technical_indicators": "vnstock,yfinance",  # Options: vnstock, alpha_vantage, yfinance
        "fundamental_data": "vnstock,yfinance",      # Options: vnstock, alpha_vantage, yfinance
        "news_data": "vnstock,yfinance",             # Options: vnstock, alpha_vantage, yfinance
    },
    # Tool-level configuration (takes precedence over category-level)
    "tool_vendors": {
        # Example: "get_stock_data": "alpha_vantage",  # Override category default
    },
}
