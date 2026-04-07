from pydantic import BaseModel
from typing import Optional, List


class PortfolioItemBase(BaseModel):
    ticker: str
    shares: float
    avg_price: float


class UserProfileUpdate(BaseModel):
    age: Optional[int] = None
    country: Optional[str] = None
    investment_experience: Optional[str] = None
    annual_income: Optional[float] = None
    monthly_savings: Optional[float] = None
    financial_goal: Optional[str] = None
    risk_profile: Optional[str] = None
    max_drawdown_tolerance: Optional[float] = None
    investment_horizon_years: Optional[int] = None
    portfolio: Optional[List[PortfolioItemBase]] = None


class UserProfileResponse(BaseModel):
    id: int
    user_id: int
    age: Optional[int] = None
    country: Optional[str] = None
    investment_experience: Optional[str] = None
    annual_income: Optional[float] = None
    monthly_savings: Optional[float] = None
    financial_goal: Optional[str] = None
    risk_profile: Optional[str] = None
    max_drawdown_tolerance: Optional[float] = None
    investment_horizon_years: Optional[int] = None

    class Config:
        from_attributes = True
