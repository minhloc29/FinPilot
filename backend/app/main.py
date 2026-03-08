"""
Main FastAPI application entry point for AI Financial Copilot
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logger import logger
from app.api.routes import chat, portfolio, health, auth

app = FastAPI(
    title="AI Financial Copilot API",
    description="Multi-agent system for financial analysis and portfolio management",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(portfolio.router, prefix="/api/v1", tags=["portfolio"])


@app.on_event("startup")
async def startup_event():
    logger.info("Starting AI Financial Copilot API...")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down AI Financial Copilot API...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
