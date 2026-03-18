import asyncio
import json
from typing import Dict, Any

from app.agents.base_agent import BaseAgent
from app.services.market_data_service import MarketDataService
from app.agents.query_parser_agent import QueryParserAgent

from app.engines.indicator_engine import IndicatorEngine
from app.engines.ranking_engine import RankingEngine

from app.cache.quote_cache import QuoteCache

from app.core.config import settings
from app.core.logger import logger
from app.utils.file_utils import read_txt

from typing import Dict, Any

from app.agents.base_agent import BaseAgent
from app.services.market_data_service import MarketDataService, SymbolDataLoader

from app.agents.query_parser_agent import QueryParserAgent

from app.engines.indicator_engine import IndicatorEngine
from app.engines.ranking_engine import RankingEngine

from app.core.config import settings
from app.core.logger import logger
from app.utils.string_utils import resolve_symbol

class MarketDataAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            api_key=settings.API_KEY,
            base_url=settings.API_ENDPOINT,
            model=settings.DEFAULT_MODEL,
            system_prompt="Vietnam stock market analyst",
            max_iterations=1
        )

        self.intent_handlers = {
            "quote": self._handle_quote_intent,
            "indices": self._handle_indices_intent,
            "ranking": self._handle_ranking_intent,
            "history": self._handle_history_intent,
            "indicator": self._handle_indicator_intent
        }

        self.default_indicators = [
            "rsi",
            "ma",
            "ema",
            "macd",
            "bollinger",
            "volatility"
        ]

        self.market_service = MarketDataService()
        self.data_loader = SymbolDataLoader(self.market_service)

        self.query_parser = QueryParserAgent()
        self.indicators = IndicatorEngine()
        self.ranking_engine = RankingEngine()

    

    async def process(self, input_data: Dict[str, Any]):

        message = input_data.get("message", "")

        logger.info(f"Market query: {message}")

        query = await self.query_parser.parse(message)

        tasks = query.get("tasks", [])

        results = []

        resolved_symbol = resolve_symbol(message, None)

        for task in tasks:

            intent = task.get("intent")

            symbol = task.get("symbol") or resolved_symbol

            handler = self.intent_handlers.get(intent)

            if not handler:
                continue

            result = await handler(task, symbol)

            if result:
                results.append(result)

        return {"results": results}

    async def _handle_quote_intent(self, task, symbol):
        snapshot = await self.data_loader.get_snapshot()

        quote = snapshot.get(symbol)

        if quote:
            return quote

        return {"error": "Symbol not found"}

    async def _handle_indices_intent(self, task, symbol):

        return await self.market_service.get_market_indices()

    async def _handle_ranking_intent(self, task, symbol):

        metric = task.get("metric", "price")
        limit = task.get("limit", 5)
        snapshot = await self.data_loader.get_snapshot()

        ranking = self.ranking_engine.rank(
            snapshot,
            metric=metric,
            limit=limit
        )

        return {
            "metric": metric,
            "top": ranking
        }

    async def _handle_history_intent(self, task, symbol):

        days = task.get("days", 60)

        history = await self.data_loader.get_history(symbol, days)

        if "error" in history:
            return history

        return {
            "symbol": symbol,
            "history": history
        }

    async def _handle_indicator_intent(self, task, symbol):

        days = task.get("days", 60)

        history = await self.data_loader.get_history(symbol, days)

        if "error" in history:
            return history

        prices = history.get("prices", [])

        indicator_name = task.get("metric")

        if indicator_name:

            value = self.indicators.compute(indicator_name, prices)

            return {
                "symbol": symbol,
                "indicator": {
                    indicator_name: value
                }
            }

        indicators = {}

        for name in self.default_indicators:

            value = self.indicators.compute(name, prices)

            if value is not None:
                indicators[name] = value

        return {
            "symbol": symbol,
            "indicators": indicators
        }   


if __name__ == "__main__":

    async def main():

        agent = MarketDataAgent()

        print("\n=== Vietnam Market Data Agent ===")
        print("Example queries:")
        print("  - Gia hien tai cua FPT la bao nhieu?")
        print("  - Chi so VNINDEX hom nay")
        print("  - Lich su gia VNM 60 ngay")
        print("  - Top 5 co phieu tang gia")
        print("  - RSI cua HPG")
        print("Type 'exit' to quit.\n")

        while True:

            try:
                message = input("Query> ").strip()

                if not message:
                    continue

                if message.lower() in {"exit", "quit", "q"}:
                    print("Bye 👋")
                    break

                result = await agent.process({"message": message})

                print("\nResult:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
                print()

            except KeyboardInterrupt:
                print("\nInterrupted. Bye 👋")
                break

            except Exception as e:
                logger.error(f"Query processing failed: {e}")
                print({"error": str(e)})

    asyncio.run(main())