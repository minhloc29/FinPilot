"""
Market data service - integrates VNStock API
"""

import asyncio
from typing import Dict, Any, List

from vnstock import Quote, Listing

from app.core.logger import logger

from datetime import date, timedelta
import time
class MarketDataService:

    def _get_quote_sync(
        self,
        symbol: str,
    ) -> Dict[str, Any] | None:

        quote = Quote(symbol=symbol, source="VCI")

        df = quote.history(
            length=1,
            interval="1d"
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
            df = quote.history(length=1, interval="1d")

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
    ) -> Dict[str, Any]:

        try:

            data = await asyncio.to_thread(
                self._get_quote_sync,
                symbol,
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
    async def get_market_snapshot(self):

        loop = asyncio.get_event_loop()

        def _get_snapshot_sync():

            listing = Listing()

            df = listing.symbols_by_exchange()

            return df.to_dict("records")

        data = await loop.run_in_executor(
            None,
            _get_snapshot_sync
        )

        return data
class SymbolDataLoader:

    def __init__(self, market_service, snapshot_ttl=30, history_ttl=86400):

        self.market_service = market_service

        self.snapshot_cache = None
        self.snapshot_timestamp = 0
        self.snapshot_ttl = snapshot_ttl

        self.history_cache = {}
        self.history_timestamp = {}
        self.history_ttl = history_ttl

        self.lock = asyncio.Lock()

    async def get_snapshot(self):

        async with self.lock:

            now = time.time()

            if (
                self.snapshot_cache
                and now - self.snapshot_timestamp < self.snapshot_ttl
            ):
                return self.snapshot_cache

            raw = await self.market_service.get_market_snapshot()

            snapshot = {}

            for item in raw:

                symbol = item.get("symbol")

                if symbol:
                    snapshot[symbol] = item

            self.snapshot_cache = snapshot
            self.snapshot_timestamp = now

            return snapshot

    async def get_history(self, symbol, days):

        key = (symbol, days)
        now = time.time()
        if key in self.history_cache and now - self.history_timestamp[key] < self.history_ttl:
            return self.history_cache[key]

        today = date.today()
        start = (today - timedelta(days=days)).isoformat()

        history = await self.market_service.get_price_history(
            symbol,
            start=start,
            end=today.isoformat()
        )

        self.history_cache[key] = history

        return history