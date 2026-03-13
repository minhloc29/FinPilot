"""
User schemas
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class PortfolioItemBase(BaseModel):
    ticker: str
    shares: float
    avg_price: float


class UserProfileUpdate(BaseModel):
    # Personal Profile
    age: Optional[int] = None
    country: Optional[str] = None
    # beginner, intermediate, advanced
    investment_experience: Optional[str] = None
    annual_income: Optional[float] = None
    monthly_savings: Optional[float] = None
    financial_goal: Optional[str] = None

    # Risk Profile
    risk_profile: Optional[str] = None  # conservative, moderate, aggressive
    max_drawdown_tolerance: Optional[float] = None
    investment_horizon_years: Optional[int] = None

    # Portfolio (handled separately, but included for onboarding)
    portfolio: Optional[List[PortfolioItemBase]] = None

    # Capital & Investment Plan
    capital: Optional[float] = None
    monthly_investment: Optional[float] = None
    rebalance_frequency: Optional[str] = None

    # Preferences
    preferred_sectors: Optional[List[str]] = None
    avoid_sectors: Optional[List[str]] = None
    dividend_preference: Optional[bool] = None
    esg_preference: Optional[bool] = None

    # Liquidity
    emergency_fund_months: Optional[int] = None


class UserProfileResponse(BaseModel):
    id: int
    user_id: int

    # Personal Profile
    age: Optional[int] = None
    country: Optional[str] = None
    investment_experience: Optional[str] = None
    annual_income: Optional[float] = None
    monthly_savings: Optional[float] = None
    financial_goal: Optional[str] = None

    # Risk Profile
    risk_profile: Optional[str] = None
    max_drawdown_tolerance: Optional[float] = None
    investment_horizon_years: Optional[int] = None

    # Capital & Investment Plan
    capital: Optional[float] = None
    monthly_investment: Optional[float] = None
    rebalance_frequency: Optional[str] = None

    # Preferences
    preferred_sectors: Optional[List[str]] = None
    avoid_sectors: Optional[List[str]] = None
    dividend_preference: Optional[bool] = None
    esg_preference: Optional[bool] = None

    # Liquidity
    emergency_fund_months: Optional[int] = None

    class Config:
        from_attributes = True
