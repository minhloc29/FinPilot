"""
User model
"""
from sqlalchemy import Column, String, Boolean, Integer, Float, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    username = Column(String, unique=True, index=True)
    phone_number = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    risk_profile = relationship(
        "RiskProfile", back_populates="user", uselist=False)


class UserProfile(BaseModel):
    __tablename__ = "user_profiles"

    user_id = Column(Integer, ForeignKey("users.id"),
                     nullable=False, unique=True)

    # Personal Profile
    age = Column(Integer)
    country = Column(String)
    investment_experience = Column(String)  # beginner, intermediate, advanced
    annual_income = Column(Float)
    monthly_savings = Column(Float)
    financial_goal = Column(String)

    # Relationship
    user = relationship("User", back_populates="profile")
