"""
Risk agent - assesses investment risk and provides risk metrics
"""
from typing import Dict, Any
from app.agents.base_agent import BaseAgent
from app.utils.risk_metrics import calculate_sharpe_ratio, calculate_var
from app.core.logger import logger


class RiskAgent(BaseAgent):
    """
    Assesses portfolio risk and provides risk metrics
    """

    def __init__(self):
        super().__init__(
            name="Risk",
            description="Calculates risk metrics, VaR, volatility, and risk-adjusted returns"
        )

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process risk assessment requests
        """
        logger.info("Processing risk assessment")

        # TODO: Fetch actual portfolio data
        mock_returns = [0.02, -0.01, 0.03, -0.02, 0.04, 0.01, -0.03]

        risk_metrics = {
            "volatility": self._calculate_volatility(mock_returns),
            "sharpe_ratio": calculate_sharpe_ratio(mock_returns),
            "value_at_risk": calculate_var(mock_returns, confidence=0.95),
            "max_drawdown": -0.15,
            "risk_score": 6.5,  # 1-10 scale
            "risk_level": "Moderate"
        }

        return risk_metrics

    def _calculate_volatility(self, returns: list) -> float:
        """
        Calculate historical volatility
        """
        import statistics
        if len(returns) < 2:
            return 0.0
        return round(statistics.stdev(returns), 4)

    def get_system_prompt(self) -> str:
        return """You are a risk management expert. Assess portfolio risk, calculate risk metrics, 
        and provide risk mitigation recommendations."""
