"""
Authentication routes - Register, Login, Get Current User
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.auth_schema import UserRegister, UserLogin, AuthResponse, UserResponse
from app.services.auth_service import AuthService
from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.core.logger import logger

router = APIRouter()


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user

    - **email**: Valid email address (must be unique)
    - **password**: Minimum 8 characters
    - **username**: 3-50 characters (must be unique)
    - **full_name**: Optional full name
    - **phone_number**: Optional phone number
    """
    try:
        logger.info(f"Registration attempt for email: {user_data.email}")

        # Create user
        user = AuthService.create_user(
            db=db,
            email=user_data.email,
            password=user_data.password,
            username=user_data.username,
            full_name=user_data.full_name,
            phone_number=user_data.phone_number
        )

        # Generate access token
        access_token = AuthService.create_user_token(user)

        logger.info(f"User registered successfully: {user.email}")

        return AuthResponse(
            user=UserResponse.model_validate(user),
            access_token=access_token,
            token_type="bearer"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/login", response_model=AuthResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login with email and password

    - **email**: Registered email address
    - **password**: User password

    Returns user information and JWT access token
    """
    try:
        logger.info(f"Login attempt for email: {credentials.email}")

        # Authenticate user
        user = AuthService.authenticate_user(
            db=db,
            email=credentials.email,
            password=credentials.password
        )

        # Generate access token
        access_token = AuthService.create_user_token(user)

        logger.info(f"User logged in successfully: {user.email}")

        return AuthResponse(
            user=UserResponse.model_validate(user),
            access_token=access_token,
            token_type="bearer"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information

    Requires valid JWT token in Authorization header
    """
    return UserResponse.model_validate(current_user)


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout current user

    Note: Since we're using JWT, actual logout is handled client-side by removing the token.
    This endpoint is for logging purposes and can be extended for token blacklisting.
    """
    logger.info(f"User logged out: {current_user.email}")
    return {"message": "Successfully logged out"}
