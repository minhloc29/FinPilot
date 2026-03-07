"""
Portfolio model
"""
from sqlalchemy import Column, String, Integer, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Portfolio(BaseModel):
    __tablename__ = "portfolios"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    total_value = Column(Float, default=0.0)

    # Relationship
    holdings = relationship("Holding", back_populates="portfolio")


class Holding(BaseModel):
    __tablename__ = "holdings"

    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    symbol = Column(String, nullable=False)
    shares = Column(Float, nullable=False)
    average_cost = Column(Float)
    current_value = Column(Float)
    message_metadata = Column(JSON)

    # Relationship
    portfolio = relationship("Portfolio", back_populates="holdings")
