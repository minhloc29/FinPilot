"""Map TradingAgents outputs to API response payloads."""

from __future__ import annotations

from typing import Any, Dict, List

from app.services.chat_formatter import format_single_ticker, format_compare


_DEFAULT_SOURCES = [
    "market_report",
    "sentiment_report",
    "news_report",
    "fundamentals_report",
    "investment_debate_state",
    "risk_debate_state",
]


class TradingAgentsAdapter:

    def build_chat_payload(
        self,
        user_message: str,
        ticker: str,
        analysis: Dict[str, Any],
        response_mode: str = "standard",
    ) -> Dict[str, Any]:
        final_state = analysis.get("final_state", {})
        signal = str(analysis.get("signal", "HOLD")).upper()

        result = format_single_ticker(
            user_message=user_message,
            ticker=ticker,
            signal=signal,
            state=final_state,
            response_mode=response_mode,
        )

        metadata = {
            "engine": "tradingagents",
            "ticker": ticker,
            "trade_date": analysis.get("trade_date"),
            "signal": signal,
            "response_mode": response_mode,
            "output_source": result["source"],
            "user_message": user_message,
            "final_trade_decision": final_state.get("final_trade_decision", ""),
            "investment_plan": final_state.get("investment_plan", ""),
            "trader_investment_plan": final_state.get("trader_investment_plan", ""),
            "investment_debate_state": final_state.get("investment_debate_state", {}),
            "risk_debate_state": final_state.get("risk_debate_state", {}),
            "reports": {
                "market_report": final_state.get("market_report", ""),
                "sentiment_report": final_state.get("sentiment_report", ""),
                "news_report": final_state.get("news_report", ""),
                "fundamentals_report": final_state.get("fundamentals_report", ""),
            },
        }

        return {"message": result["text"], "sources": _DEFAULT_SOURCES, "metadata": metadata}

    def build_compare_chat_payload(
        self,
        user_message: str,
        multi_ticker_result: Dict[str, Any],
        response_mode: str = "compare",
    ) -> Dict[str, Any]:
        analyses = multi_ticker_result.get("analyses", [])
        failures = multi_ticker_result.get("failures", [])

        result = format_compare(
            user_message=user_message,
            analyses=analyses,
            failures=failures,
            response_mode=response_mode,
        )

        metadata = {
            "engine": "tradingagents",
            "response_mode": response_mode,
            "output_source": result["source"],
            "user_message": user_message,
            "trade_date": multi_ticker_result.get("trade_date"),
            "analyses": analyses,
            "failures": failures,
        }

        return {"message": result["text"], "sources": _DEFAULT_SOURCES, "metadata": metadata}

    @staticmethod
    def _holding_value(holding: Dict[str, Any]) -> float:
        current_value = holding.get("current_value")
        if current_value is not None:
            return float(current_value)
        shares = float(holding.get("shares") or 0.0)
        average_cost = float(holding.get("average_cost") or 0.0)
        return shares * average_cost

    def _asset_allocation(self, holdings: List[Dict[str, Any]]) -> Dict[str, float]:
        values = {
            str(h.get("symbol") or "").upper(): self._holding_value(h)
            for h in holdings
            if h.get("symbol")
        }
        total = sum(v for v in values.values() if v > 0)
        if total <= 0:
            return {symbol: 0.0 for symbol in values}
        return {symbol: round((value / total) * 100, 2) for symbol, value in values.items()}

    @staticmethod
    def _diversification_score(allocation: Dict[str, float]) -> float:
        weights = [v / 100.0 for v in allocation.values() if v > 0]
        n = len(weights)
        if n <= 1:
            return 0.0
        hhi = sum(w ** 2 for w in weights)
        normalized = (1.0 - hhi) / (1.0 - (1.0 / n))
        return round(max(0.0, min(1.0, normalized)) * 100.0, 2)

    @staticmethod
    def _signal_recommendation(symbol: str, signal: str) -> str:
        mapping = {
            "BUY": f"{symbol}: uu tien tang ty trong vi tin hieu BUY.",
            "OVERWEIGHT": f"{symbol}: co the tang ty trong theo lo trinh (OVERWEIGHT).",
            "HOLD": f"{symbol}: giu vi the hien tai (HOLD).",
            "UNDERWEIGHT": f"{symbol}: xem xet giam ty trong (UNDERWEIGHT).",
            "SELL": f"{symbol}: uu tien giam/thoat vi the (SELL).",
        }
        return mapping.get(signal, f"{symbol}: tin hieu chua ro, can theo doi them.")

    def build_portfolio_analysis(
        self,
        portfolio_id: str,
        holdings: List[Dict[str, Any]],
        portfolio_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        analyses = portfolio_result.get("analyses", [])
        failures = portfolio_result.get("failures", [])

        allocation = self._asset_allocation(holdings)
        total_value = round(sum(self._holding_value(h) for h in holdings), 2)
        diversification_score = self._diversification_score(allocation)

        recommendations: List[str] = []
        for item in analyses:
            symbol = str(item.get("ticker") or "").upper()
            signal = str(item.get("signal") or "HOLD").upper()
            if symbol:
                recommendations.append(self._signal_recommendation(symbol, signal))

        for item in failures:
            symbol = str(item.get("symbol") or "UNKNOWN")
            recommendations.append(
                f"{symbol}: khong the phan tich o lan chay nay, kiem tra API key va ket noi du lieu."
            )

        if not recommendations:
            recommendations.append("Khong co du lieu phu hop de dua ra khuyen nghi.")

        return {
            "portfolio_id": str(portfolio_id),
            "total_value": total_value,
            "asset_allocation": allocation,
            "diversification_score": diversification_score,
            "recommendations": recommendations,
        }
