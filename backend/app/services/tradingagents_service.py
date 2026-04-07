import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional

from app.core.config import settings
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG


_effective_openai_key = settings.effective_openai_api_key
if _effective_openai_key:
    os.environ["OPENAI_API_KEY"] = _effective_openai_key


class TradingAgentsService:

    def __init__(self):
        os.makedirs(settings.TRADINGAGENTS_RESULTS_DIR, exist_ok=True)
        self.config = self._build_config()

    def _build_config(self) -> Dict[str, Any]:
        # Resolve project_dir: use setting if set, otherwise use tradingagents package default
        project_dir = settings.TRADINGAGENTS_PROJECT_DIR or DEFAULT_CONFIG["project_dir"]

        # Parse vendor string "vnstock,yfinance" into DEFAULT_CONFIG data_vendors format
        vendors = settings.TRADINGAGENTS_DATA_VENDORS
        data_vendors = {
            "core_stock_apis": vendors,
            "technical_indicators": vendors,
            "fundamental_data": vendors,
            "news_data": vendors,
        }

        config = {
            "llm_provider": settings.TRADINGAGENTS_LLM_PROVIDER,
            "deep_think_llm": settings.TRADINGAGENTS_DEEP_MODEL,
            "quick_think_llm": settings.TRADINGAGENTS_QUICK_MODEL,
            "backend_url": settings.effective_trading_backend_url,
            "max_debate_rounds": settings.TRADINGAGENTS_MAX_DEBATE_ROUNDS,
            "max_risk_discuss_rounds": settings.TRADINGAGENTS_MAX_RISK_DISCUSS_ROUNDS,
            "project_dir": project_dir,
            "results_dir": settings.TRADINGAGENTS_RESULTS_DIR,
            "data_vendors": data_vendors,
        }

        # Provider-specific thinking configs - only add if set
        if settings.TRADINGAGENTS_OPENAI_REASONING_EFFORT:
            config["openai_reasoning_effort"] = settings.TRADINGAGENTS_OPENAI_REASONING_EFFORT
        if settings.TRADINGAGENTS_GOOGLE_THINKING_LEVEL:
            config["google_thinking_level"] = settings.TRADINGAGENTS_GOOGLE_THINKING_LEVEL
        if settings.TRADINGAGENTS_ANTHROPIC_EFFORT:
            config["anthropic_effort"] = settings.TRADINGAGENTS_ANTHROPIC_EFFORT

        return config

    def run_single_ticker(
        self,
        ticker: str,
        trade_date: Optional[str] = None,
        selected_analysts: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Run multi-agent graph with the analysts selected by the AI Orchestrator."""
        from datetime import datetime

        analysts = selected_analysts or ["market", "social", "news", "fundamentals"]
        dt = trade_date or datetime.now().strftime("%Y-%m-%d")

        graph = TradingAgentsGraph(
            selected_analysts=analysts,
            config=self.config,
        )

        final_state, signal = graph.propagate(ticker, dt)

        return {
            "ticker": ticker,
            "trade_date": dt,
            "signal": signal,
            "final_state": final_state,
            "analysts_active": analysts,
        }

    def run_many_tickers(
        self,
        tickers: List[str],
        trade_date: Optional[str] = None,
        selected_analysts: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Run single-ticker analysis for multiple stocks in parallel via threads."""
        from datetime import datetime

        dt = trade_date or datetime.now().strftime("%Y-%m-%d")
        results: List[Dict[str, Any]] = []
        failures: List[Dict[str, str]] = []

        with ThreadPoolExecutor(max_workers=min(len(tickers), 4)) as executor:
            future_to_ticker = {
                executor.submit(self.run_single_ticker, ticker, dt, selected_analysts): ticker
                for ticker in tickers
            }
            for future in as_completed(future_to_ticker):
                ticker = future_to_ticker[future]
                try:
                    results.append(future.result())
                except Exception as exc:
                    failures.append({"symbol": ticker, "error": str(exc)})

        return {
            "trade_date": dt,
            "analyses": results,
            "failures": failures,
            "analysts_active": selected_analysts,
        }

    def run_portfolio(
        self,
        holdings: List[Dict[str, Any]],
        trade_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Analyze all held tickers with full analysts for maximum accuracy."""
        tickers = [h["symbol"] for h in holdings if h.get("symbol")]
        return self.run_many_tickers(tickers, trade_date, ["market", "news", "fundamentals"])
