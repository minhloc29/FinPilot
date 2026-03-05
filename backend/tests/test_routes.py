"""
Tests for API routes
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_readiness_check():
    """Test readiness check endpoint"""
    response = client.get("/api/v1/ready")
    assert response.status_code == 200
    assert response.json()["ready"] is True


def test_chat_endpoint():
    """Test chat endpoint"""
    payload = {
        "message": "What's the stock market doing today?",
        "user_id": "test_user"
    }
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    assert "message" in response.json()


def test_portfolio_creation():
    """Test portfolio creation"""
    payload = {
        "user_id": "test_user",
        "name": "My Portfolio",
        "holdings": [
            {"symbol": "AAPL", "shares": 10}
        ]
    }
    response = client.post("/api/v1/portfolio", json=payload)
    assert response.status_code == 200
    assert "id" in response.json()
