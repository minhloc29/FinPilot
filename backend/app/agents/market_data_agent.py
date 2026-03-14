import asyncio
import json
from typing import Dict, Any

from app.agents.base_agent import BaseAgent
from app.services.market_data_service import MarketDataService
from app.agents.query_parser_agent import QueryParserAgent
from app.agents.symbol_resolver import SymbolResolver

from app.engines.indicator_engine import IndicatorEngine
from app.engines.ranking_engine import RankingEngine

from app.cache.quote_cache import QuoteCache
from app.data.symbol_database import SymbolDatabase

from app.core.config import settings
from app.core.logger import logger
from app.utils.file_utils import read_txt

class MarketDataAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            api_key=settings.API_KEY,
            base_url=settings.API_ENDPOINT,
            model=settings.DEFAULT_MODEL,
            system_prompt="Vietnam stock market analyst",
            max_iterations=1
        )

        self.market_service = MarketDataService()

        self.symbol_db = None
        self.symbol_resolver = None

        self.query_parser = QueryParserAgent()

        self.indicators = IndicatorEngine()

        self.ranking_engine = RankingEngine(self.market_service)
        self.explanation_prompt = read_txt("./prompts/market_agent_explanation.txt")
        self.cache = QuoteCache()

    async def _ensure_symbol_db(self):

        if self.symbol_db is None:

            symbols = await self.market_service.get_all_symbols()

            self.symbol_db = SymbolDatabase(symbols)

            self.symbol_resolver = SymbolResolver(self.symbol_db)

    async def process(self, input_data: Dict[str, Any]):

        await self._ensure_symbol_db()

        message = input_data.get("message", "")

        logger.info(f"Market query: {message}")

        query = await self.query_parser.parse(message)

        intent = query.get("intent")

        symbol = query.get("symbol")

        if not symbol:

            symbol = self.symbol_resolver.resolve(message)

        if intent == "indices":

            return await self.market_service.get_market_indices()

        if intent == "history":

            return await self.market_service.get_price_history(
                symbol,
                start="2025-01-01",
                end="2026-01-01"
            )

        full_explanation_prompt = self.explanation_prompt.format(result = await self.handle_quote(symbol))
        natural_response = await self.complete(full_explanation_prompt)
        
        return natural_response

    async def handle_quote(self, symbol):

        cached = self.cache.get(("quote", symbol))

        if cached:
            return cached

        history = await self.market_service.get_price_history(
            symbol,
            start="2025-01-01",
            end="2026-01-01"
        )
        if "error" in history:
            return history
        prices = history.get("prices", [])
        if not prices:
            return {"error": "No price data"}
        opens = history.get("opens", [])
        highs = history.get("highs", [])
        lows = history.get("lows", [])
        volumes = history.get("volumes", [])

        price = prices[-1] if prices else None
        open_price = opens[-1] if opens else None
        high = highs[-1] if highs else None
        low = lows[-1] if lows else None
        volume = volumes[-1] if volumes else None

        rsi = self.indicators.rsi(prices)
        ma20 = self.indicators.ma(prices)
        vol = self.indicators.volatility(prices)

        change_pct = None

        if price and open_price and open_price != 0:
            change_pct = (
                (price - open_price) /
                open_price * 100
            )

        result = {
            "symbol": symbol,
            "price": price,
            "open": open_price,
            "high": high,
            "low": low,
            "volume": volume,
            "change_percent": change_pct,
            "rsi": rsi,
            "ma20": ma20,
            "volatility": vol
        }

        self.cache.set(symbol, result)

        return result


async def _run_local_test() -> None:
    agent = MarketDataAgent()

    print("=== MarketDataAgent Query Test ===")
    print("Type a natural query, for example:")
    print("- Gia hien tai cua FPT la bao nhieu?")
    print("- Cho toi chi so VNINDEX")
    print("- Lich su gia VNM")
    print("Type 'exit' to quit.\n")

    while True:

        message = input("Query> ").strip()

        if not message:
            continue

        if message.lower() in {"exit", "quit", "q"}:
            print("Bye")
            break

        try:
            result = await agent.process({"message": message})
            print(result)
        except Exception as e:
            logger.error(f"Query processing failed: {e}")
            result = {"error": str(e)}

        print(json.dumps(result, indent=2, ensure_ascii=False))
        print()


if __name__ == "__main__":
    asyncio.run(_run_local_test())
