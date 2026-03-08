"""
Authentication service for user management
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.logger import logger
from datetime import timedelta


class AuthService:

    @staticmethod
    def create_user(db: Session, email: str, password: str, username: str,
                    full_name: str = None, phone_number: str = None) -> User:

        print("HIHI")
        try:
            # Check if user already exists
            existing_user = db.query(User).filter(
                (User.email == email) | (User.username == username)
            ).first()

            print(f"Check existing: {existing_user}")
            if existing_user:
                if existing_user.email == email:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email already registered"
                    )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Username already taken"
                    )

            # Create new user
            hashed_password = get_password_hash(password)
            print(f"Check hash: {hashed_password}")
            user = User(
                email=email,
                hashed_password=hashed_password,
                username=username,
                full_name=full_name,
                phone_number=phone_number,
                is_active=True,
                is_superuser=False
            )

            db.add(user)
            db.commit()
            db.refresh(user)

            logger.info(f"New user created: {email}")
            return user

        except IntegrityError as e:
            db.rollback()
            logger.error(f"Database integrity error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email or username already exists"
            )
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating user: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:

        user = db.query(User).filter(User.email == email).first()

        if not user:
            logger.warning(f"Login attempt with non-existent email: {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not verify_password(password, user.hashed_password):
            logger.warning(f"Failed login attempt for user: {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            logger.warning(f"Inactive user login attempt: {email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )

        logger.info(f"User authenticated successfully: {email}")
        return user

    @staticmethod
    def create_user_token(user: User) -> str:

        access_token_expires = timedelta(minutes=60 * 24 * 7)  # 7 days
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=access_token_expires
        )
        return access_token

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        return db.query(User).filter(User.id == user_id).first()
