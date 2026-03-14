"""User profile service aligned with existing database design."""
from typing import Optional, Tuple
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.models.user import UserProfile
from app.models.risk_profile import RiskProfile
from app.models.portfolio import Portfolio, Holding
from app.schemas.user_schema import UserProfileUpdate


class UserProfileService:
    """Service for user profile and onboarding persistence."""

    @staticmethod
    def get_user_profile(db: Session, user_id: int) -> Optional[UserProfile]:
        print(f"Start query")
        return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    @staticmethod
    def get_risk_profile(db: Session, user_id: int) -> Optional[RiskProfile]:
        return db.query(RiskProfile).filter(RiskProfile.user_id == user_id).first()

    @staticmethod
    def create_or_update_profile(
        db: Session,
        user_id: int,
        profile_data: UserProfileUpdate,
    ) -> Tuple[UserProfile, Optional[RiskProfile]]:
        print(profile_data)
        """Upsert user profile, risk profile, and onboarding portfolio holdings."""
        try:
            payload = profile_data.model_dump(exclude_unset=True)

            profile = UserProfileService.get_user_profile(
                db=db, user_id=user_id)
            
            if not profile:
                profile = UserProfile(user_id=user_id)
                db.add(profile)

            # Persist only fields that exist in user_profiles table.
            profile_fields = [
                "age",
                "country",
                "investment_experience",
                "annual_income",
                "monthly_savings",
                "financial_goal",
            ]
            for field in profile_fields:
                if field in payload:
                    setattr(profile, field, payload[field])

            risk = UserProfileService.get_risk_profile(db=db, user_id=user_id)
            risk_keys = {"risk_profile", "max_drawdown_tolerance",
                         "investment_horizon_years"}
            
            if any(key in payload for key in risk_keys):
                if not risk:
                    risk = RiskProfile(
                        user_id=user_id,
                        risk_level=payload.get("risk_profile") or "moderate",
                        max_drawdown=payload.get(
                            "max_drawdown_tolerance") or 20.0,
                        investment_horizon_years=payload.get(
                            "investment_horizon_years") or 5,
                    )
                    db.add(risk)
                    
                else:
                    if "risk_profile" in payload:
                        risk.risk_level = payload["risk_profile"]
                    if "max_drawdown_tolerance" in payload:
                        risk.max_drawdown = payload["max_drawdown_tolerance"]
                    if "investment_horizon_years" in payload:
                        risk.investment_horizon_years = payload["investment_horizon_years"]

            if "portfolio" in payload:
                print("In here")
                UserProfileService._sync_onboarding_portfolio(
                    db=db,
                    user_id=user_id,
                    portfolio_items=payload.get("portfolio") or [],
                )
                print("Get here")

            db.commit()
            db.refresh(profile)
            if risk:
                db.refresh(risk)

            logger.info("Updated onboarding profile for user_id=%s", user_id)
            return profile, risk
        except Exception as exc:
            db.rollback()
            logger.error(
                "Error updating onboarding profile for user_id=%s: %s", user_id, str(exc))
            raise

    @staticmethod
    def delete_profile(db: Session, user_id: int) -> bool:
        """Delete user profile and risk profile only."""
        try:
            profile = UserProfileService.get_user_profile(
                db=db, user_id=user_id)
            risk = UserProfileService.get_risk_profile(db=db, user_id=user_id)

            deleted = False
            if profile:
                db.delete(profile)
                deleted = True
            if risk:
                db.delete(risk)
                deleted = True

            if deleted:
                db.commit()
            return deleted
        except Exception as exc:
            db.rollback()
            logger.error(
                "Error deleting profile for user_id=%s: %s", user_id, str(exc))
            raise

    @staticmethod
    def _sync_onboarding_portfolio(db: Session, user_id: int, portfolio_items: list) -> None:
        """Create or replace holdings in the user's default onboarding portfolio."""
        portfolio = (
            db.query(Portfolio)
            .filter(Portfolio.user_id == user_id)
            .order_by(Portfolio.created_at.asc())
            .first()
        )

        print(f"See portfolio: {portfolio}")
        if not portfolio:
            portfolio = Portfolio(
                user_id=user_id,
                name="My Portfolio",
                description="Onboarding portfolio",
                total_value=0.0,
            )
            db.add(portfolio)
            db.flush()

        db.query(Holding).filter(Holding.portfolio_id ==
                                 portfolio.id).delete(synchronize_session=False)

        total_value = 0.0
        for item in portfolio_items:
            ticker = str(item.get("ticker", "")).upper().strip()
            shares = float(item.get("shares", 0) or 0)
            avg_price = float(item.get("avg_price", 0) or 0)

            if not ticker or shares <= 0:
                continue

            current_value = shares * avg_price
            total_value += current_value

            db.add(
                Holding(
                    portfolio_id=portfolio.id,
                    ticker=ticker,
                    shares=shares,
                    average_cost=avg_price,
                    current_value=current_value,
                )
            )

        portfolio.total_value = total_value
