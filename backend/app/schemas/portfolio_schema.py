"""
Portfolio schemas
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class HoldingBase(BaseModel):
    symbol: str
    shares: float
    average_cost: Optional[float] = None


class PortfolioCreate(BaseModel):
    user_id: str
    name: str
    description: Optional[str] = None
    holdings: List[HoldingBase] = []


class PortfolioResponse(BaseModel):
    id: str
    user_id: str
    name: str
    holdings: List[HoldingBase]
    created_at: str
    total_value: Optional[float] = None

    class Config:
        from_attributes = True


class PortfolioAnalysis(BaseModel):
    portfolio_id: str
    total_value: float
    asset_allocation: Dict[str, float]
    diversification_score: float
    recommendations: List[str]
