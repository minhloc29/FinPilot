"""User profile routes aligned with current database design."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.logger import logger
from app.db.session import get_db
from app.models.user import User, UserProfile
from app.models.risk_profile import RiskProfile
from app.schemas.user_schema import UserProfileResponse, UserProfileUpdate
from app.services.user_profile_service import UserProfileService

router = APIRouter()


def _to_response(profile: UserProfile, risk: RiskProfile | None) -> UserProfileResponse:
    return UserProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        age=profile.age,
        country=profile.country,
        investment_experience=profile.investment_experience,
        annual_income=profile.annual_income,
        monthly_savings=profile.monthly_savings,
        financial_goal=profile.financial_goal,
        risk_profile=risk.risk_level if risk else None,
        max_drawdown_tolerance=risk.max_drawdown if risk else None,
        investment_horizon_years=risk.investment_horizon_years if risk else None,
        # These fields are not persisted in the current ERD and therefore returned as null.
        capital=None,
        monthly_investment=None,
        rebalance_frequency=None,
        preferred_sectors=None,
        avoid_sectors=None,
        dividend_preference=None,
        esg_preference=None,
        emergency_fund_months=None,
    )


@router.post("/user-profile", response_model=UserProfileResponse, status_code=status.HTTP_200_OK)
async def upsert_user_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    
    try:
        profile, risk = UserProfileService.create_or_update_profile(
            db=db,
            user_id=current_user.id,
            profile_data=profile_data,
        )
        return _to_response(profile=profile, risk=risk)
    except Exception as exc:
        logger.error(
            "Failed to upsert user profile for user_id=%s: %s", current_user.id, str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile",
        )


@router.get("/user-profile", response_model=UserProfileResponse)
async def get_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = UserProfileService.get_user_profile(
        db=db, user_id=current_user.id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User profile not found")

    risk = UserProfileService.get_risk_profile(db=db, user_id=current_user.id)
    return _to_response(profile=profile, risk=risk)


@router.delete("/user-profile", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        deleted = UserProfileService.delete_profile(
            db=db, user_id=current_user.id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found")
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(
            "Failed to delete user profile for user_id=%s: %s", current_user.id, str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete profile",
        )
