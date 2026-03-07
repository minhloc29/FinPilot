"""
Market data agent - fetches and analyzes market data
"""
from typing import Dict, Any
from app.agents.base_agent import BaseAgent
from app.services.market_data_service import MarketDataService
from app.core.logger import logger
from app.core.config import settings


class MarketDataAgent(BaseAgent):
    """
    Fetches and analyzes real-time market data
    """

    def __init__(self):
        super().__init__(
            api_key=settings.API_KEY,
            base_url=settings.API_ENDPOINT,
            model=settings.DEFAULT_MODEL,
            system_prompt="You are a market data analyst. Provide real-time stock prices, market trends, and technical analysis based on the latest market data.",
            max_iterations=1
        )
        self.market_service = MarketDataService()

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process market data requests
        """
        message = input_data.get("message", "")
        action = input_data.get("action", "fetch")

        logger.info(f"Processing market data request: {action}")

        # Extract symbols from message
        symbols = self._extract_symbols(message)

        if not symbols:
            symbols = ["SPY", "QQQ"]  # Default to major indices

        # Fetch market data
        market_data = {}
        for symbol in symbols:
            data = await self.market_service.get_quote(symbol)
            market_data[symbol] = data

        return {
            "market_data": market_data,
            "symbols": symbols,
            "timestamp": "2026-03-02T00:00:00Z"
        }

    def _extract_symbols(self, message: str) -> list:
        """
        Extract stock symbols from message
        """
        # Simple extraction - in production, use NER or regex
        common_symbols = ["AAPL", "GOOGL",
                          "MSFT", "AMZN", "TSLA", "SPY", "QQQ"]
        found_symbols = [s for s in common_symbols if s.lower()
                         in message.lower()]
        return found_symbols
