"""
Portfolio agent - analyzes and manages investment portfolios
"""
from typing import Dict, Any
from app.agents.base_agent import BaseAgent
from app.core.logger import logger
from app.core.config import settings


class PortfolioAgent(BaseAgent):
    """
    Analyzes portfolio composition, performance, and optimization
    """

    def __init__(self):
        super().__init__(
            api_key=settings.API_KEY,
            base_url=settings.API_ENDPOINT,
            model=settings.DEFAULT_MODEL,
            system_prompt="You are a portfolio management expert. Analyze portfolio composition, assess diversification, and provide optimization recommendations.",
            max_iterations=1
        )

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process portfolio analysis requests
        """
        action = input_data.get("action", "analyze")

        logger.info(f"Processing portfolio action: {action}")

        if action == "analyze":
            return await self.analyze(input_data.get("portfolio_id"))
        elif action == "optimize":
            return await self.optimize(input_data.get("portfolio_id"))

        return {"error": "Unknown action"}

    async def analyze(self, portfolio_id: str = None) -> Dict[str, Any]:
        """
        Analyze portfolio composition and performance
        """
        # TODO: Fetch actual portfolio data from database
        mock_portfolio = {
            "holdings": [
                {"symbol": "AAPL", "shares": 10, "value": 1750},
                {"symbol": "GOOGL", "shares": 5, "value": 750},
                {"symbol": "MSFT", "shares": 15, "value": 4500}
            ],
            "total_value": 7000
        }

        analysis = {
            "portfolio_id": portfolio_id,
            "total_value": mock_portfolio["total_value"],
            "asset_allocation": self._calculate_allocation(mock_portfolio),
            "diversification_score": 0.75,
            "recommendations": [
                "Consider adding bonds for diversification",
                "Tech sector concentration is high (85%)"
            ]
        }

        return analysis

    async def optimize(self, portfolio_id: str) -> Dict[str, Any]:
        """
        Suggest portfolio optimization strategies
        """
        return {
            "portfolio_id": portfolio_id,
            "optimizations": [
                {"action": "reduce", "symbol": "AAPL",
                    "reason": "Overweight position"},
                {"action": "add", "symbol": "BND",
                    "reason": "Increase diversification"}
            ]
        }

    def _calculate_allocation(self, portfolio: Dict) -> Dict[str, float]:
        """
        Calculate asset allocation percentages
        """
        total = portfolio["total_value"]
        allocation = {}

        for holding in portfolio["holdings"]:
            symbol = holding["symbol"]
            percentage = (holding["value"] / total) * 100
            allocation[symbol] = round(percentage, 2)

        return allocation
