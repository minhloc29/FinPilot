"""
Portfolio model
"""
from sqlalchemy import Column, String, Integer, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Portfolio(BaseModel):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    name = Column(String, nullable=True)
    holdings = relationship("Holding", back_populates="portfolio")


class Holding(BaseModel):
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=True)
    ticker = Column(String, nullable=True)
    shares = Column(Float, nullable=True)
    average_cost = Column(Float, nullable=True)
    current_value = Column(Float, nullable=True)
    message_metadata = Column(JSON, nullable=True)

    portfolio = relationship("Portfolio", back_populates="holdings")
