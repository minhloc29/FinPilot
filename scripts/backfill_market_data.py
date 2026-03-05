"""
Script to backfill historical market data
"""
from app.services.market_data_service import MarketDataService
from datetime import datetime, timedelta
import asyncio
import sys
sys.path.append('../backend')


async def backfill_market_data():
    """
    Backfill historical market data for common symbols
    """
    service = MarketDataService()

    symbols = [
        "AAPL", "GOOGL", "MSFT", "AMZN", "TSLA",
        "JPM", "BAC", "WMT", "JNJ", "V",
        "SPY", "QQQ", "DIA"
    ]

    print(f"Backfilling data for {len(symbols)} symbols...")

    for symbol in symbols:
        print(f"\nFetching data for {symbol}...")
        try:
            # Fetch current quote
            quote = await service.get_quote(symbol)
            print(f"  Current price: ${quote['price']}")

            # TODO: Fetch and store historical data
            # historical = await service.get_historical_data(symbol, interval="daily")
            # Store in database or cache

        except Exception as e:
            print(f"  Error: {str(e)}")

    print("\nBackfill completed!")


if __name__ == "__main__":
    asyncio.run(backfill_market_data())
