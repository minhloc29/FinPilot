"""
Tests for services
"""
import pytest
from app.services.llm_service import LLMService
from app.services.cache_service import CacheService
from app.services.market_data_service import MarketDataService


@pytest.mark.asyncio
async def test_llm_service():
    """Test LLM service"""
    service = LLMService()
    # Mock test - in production, use actual API or mock
    assert service.model is not None


@pytest.mark.asyncio
async def test_cache_service():
    """Test cache service"""
    cache = CacheService()
    await cache.set("test_key", {"data": "test"})
    result = await cache.get("test_key")
    assert result["data"] == "test"
    await cache.delete("test_key")


@pytest.mark.asyncio
async def test_market_data_service():
    """Test market data service"""
    service = MarketDataService()
    result = await service.get_quote("AAPL")
    assert "symbol" in result
    assert "price" in result
