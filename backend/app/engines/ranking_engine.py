from typing import List
import asyncio


class RankingEngine:

    def __init__(self, market_service):
        self.market_service = market_service

    async def _safe_quote(self, symbol, sem):

        async with sem:
            return await self.market_service.get_quote(symbol)

    async def rank_by_price(
        self,
        symbols: List[str],
        limit: int = 5
    ) -> List[dict]:

        sem = asyncio.Semaphore(20)

        tasks = [
            self._safe_quote(symbol, sem)
            for symbol in symbols
        ]

        quotes = await asyncio.gather(
            *tasks,
            return_exceptions=True
        )

        results = []

        for quote in quotes:

            if isinstance(quote, Exception):
                continue

            if not quote or "error" in quote:
                continue

            results.append({
                "symbol": quote["symbol"],
                "price": quote["price"]
            })

        results.sort(
            key=lambda x: x["price"],
            reverse=True
        )

        return results[:limit]