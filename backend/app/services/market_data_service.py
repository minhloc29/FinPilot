"""
Market data service - integrates VNStock API
"""

import asyncio
from typing import Dict, Any, List

from vnstock import Quote, Listing

from app.core.logger import logger


class MarketDataService:

    def _get_quote_sync(
        self,
        symbol: str,    
        start: str,
        end: str,
        interval: str
    ) -> Dict[str, Any] | None:

        quote = Quote(symbol=symbol, source="VCI")

        df = quote.history(
            start=start,
            end=end,
            interval=interval
        )

        if df.empty:
            return None

        latest = df.iloc[-1]

        return {
            "symbol": symbol,
            "price": float(latest["close"]),
            "open": float(latest["open"]),
            "high": float(latest["high"]),
            "low": float(latest["low"]),
            "volume": int(latest["volume"]),
        }

    def _get_history_sync(
        self,
        symbol: str,
        start: str,
        end: str,
        interval: str
    ) -> Dict[str, Any] | None:

        quote = Quote(symbol=symbol, source="VCI")

        df = quote.history(
            start=start,
            end=end,
            interval=interval
        )

        if df.empty:
            return None

        return {
            "symbol": symbol,
            "prices": df["close"].tolist(),
            "opens": df["open"].tolist(),
            "highs": df["high"].tolist(),
            "lows": df["low"].tolist(),
            "volumes": df["volume"].tolist(),
            "dates": df["time"].astype(str).tolist()
        }

    def _get_indices_sync(self) -> Dict[str, float]:

        indices = ["VNINDEX", "HNXINDEX", "UPCOMINDEX"]
        result: Dict[str, float] = {}

        for symbol in indices:

            quote = Quote(symbol=symbol, source="VCI")
            df = quote.history(length=1, interval="d")

            if not df.empty:

                latest = df.iloc[-1]

                result[symbol] = float(latest["close"])

        return result

    def _get_listing_sync(self) -> List[str]:

        listing = Listing(source="VCI")

        df = listing.all_symbols()

        return df["symbol"].tolist()

    async def get_quote(
        self,
        symbol: str,
        start: str = "2024-01-01",
        end: str = "2026-01-01",
        interval: str = "1d",
    ) -> Dict[str, Any]:

        try:

            data = await asyncio.to_thread(
                self._get_quote_sync,
                symbol,
                start,
                end,
                interval,
            )

            if data is None:
                return {"error": "No data"}

            return data

        except Exception as e:

            logger.error(f"Market data error: {e}")

            return {"error": str(e)}

    async def get_price_history(
        self,
        symbol: str,
        start: str,
        end: str,
        interval: str = "1d",
    ) -> Dict[str, Any]:

        try:

            data = await asyncio.to_thread(
                self._get_history_sync,
                symbol,
                start,
                end,
                interval,
            )

            if data is None:
                return {"error": "No data"}

            return data

        except Exception as e:

            logger.error(f"History fetch error: {e}")

            return {"error": str(e)}

    async def get_market_indices(self) -> Dict[str, float]:

        try:

            data = await asyncio.to_thread(self._get_indices_sync)

            return data

        except Exception as e:

            logger.error(f"Index fetch error: {e}")

            return {"error": str(e)}

    async def get_all_symbols(self) -> List[str]:

        try:

            symbols = await asyncio.to_thread(self._get_listing_sync)

            return symbols

        except Exception as e:

            logger.error(f"Listing error: {e}")

            return []