"""
Risk metrics calculations
"""
from typing import List
import numpy as np


def calculate_sharpe_ratio(returns: List[float], risk_free_rate: float = 0.02) -> float:
    """
    Calculate Sharpe ratio
    """
    if len(returns) < 2:
        return 0.0

    returns_np = np.array(returns)
    excess_returns = returns_np - \
        (risk_free_rate / 252)  # Daily risk-free rate

    if np.std(excess_returns) == 0:
        return 0.0

    sharpe = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)
    return round(sharpe, 2)


def calculate_var(returns: List[float], confidence: float = 0.95) -> float:
    """
    Calculate Value at Risk (VaR)
    """
    if len(returns) < 2:
        return 0.0

    returns_np = np.array(returns)
    var = np.percentile(returns_np, (1 - confidence) * 100)
    return round(var, 4)


def calculate_beta(asset_returns: List[float], market_returns: List[float]) -> float:
    """
    Calculate beta coefficient
    """
    if len(asset_returns) != len(market_returns) or len(asset_returns) < 2:
        return 1.0

    asset_np = np.array(asset_returns)
    market_np = np.array(market_returns)

    covariance = np.cov(asset_np, market_np)[0][1]
    market_variance = np.var(market_np)

    if market_variance == 0:
        return 1.0

    beta = covariance / market_variance
    return round(beta, 2)


def calculate_sortino_ratio(returns: List[float], target_return: float = 0.0) -> float:
    """
    Calculate Sortino ratio (focuses on downside deviation)
    """
    if len(returns) < 2:
        return 0.0

    returns_np = np.array(returns)
    excess_returns = returns_np - target_return

    downside_returns = excess_returns[excess_returns < 0]

    if len(downside_returns) == 0 or np.std(downside_returns) == 0:
        return 0.0

    sortino = np.mean(excess_returns) / np.std(downside_returns) * np.sqrt(252)
    return round(sortino, 2)
