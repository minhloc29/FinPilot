"""
Health check routes
"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "AI Financial Copilot API"
    }


@router.get("/ready")
async def readiness_check():
    """
    Readiness check endpoint
    """
    # TODO: Add checks for database, redis, etc.
    return {
        "ready": True,
        "checks": {
            "database": "ok",
            "redis": "ok",
            "llm_service": "ok"
        }
    }
