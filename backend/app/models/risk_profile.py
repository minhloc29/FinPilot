from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class RiskProfile(BaseModel):
    __tablename__ = "risk_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    risk_level = Column(String, nullable=True)
    max_drawdown = Column(Float, nullable=True)
    investment_horizon_years = Column(Integer, nullable=True)

    user = relationship("User", back_populates="risk_profile")