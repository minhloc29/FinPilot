"""
API dependencies and middleware
"""
from fastapi import Header, HTTPException
from typing import Optional


async def verify_api_key(x_api_key: Optional[str] = Header(None)) -> str:
    """
    Verify API key from request header
    """
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required")

    # TODO: Implement actual API key verification
    return x_api_key


async def get_current_user(token: str = Header(...)):
    """
    Get current user from JWT token
    """
    # TODO: Implement JWT token verification
    return {"user_id": "user_123", "email": "user@example.com"}
