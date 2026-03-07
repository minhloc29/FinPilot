"""
User model
"""
from sqlalchemy import Column, String, Boolean, Integer, Float, ForeignKey
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

    # Relationship
    profile = relationship("UserProfile", back_populates="user", uselist=False)


class UserProfile(BaseModel):
    __tablename__ = "user_profiles"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    risk_profile = Column(String)  # conservative, moderate, aggressive
    capital = Column(Float)
    time_horizon = Column(String)  # short, medium, long
    income_needed = Column(Float)

    # Relationship
    user = relationship("User", back_populates="profile")



    