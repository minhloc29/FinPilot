import json

from app.agents.base_agent import BaseAgent
from app.core.config import settings


class QueryParserAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            api_key=settings.API_KEY,
            base_url=settings.API_ENDPOINT,
            model=settings.DEFAULT_MODEL,
            system_prompt="You convert stock queries into JSON intents",
            max_iterations=1,
        )

    async def parse(self, message: str):

        prompt = f"""
Convert the following query into JSON.

Query:
{message}

Return JSON with fields:

intent: quote | history | indices | sector_ranking
symbol: optional
sector: optional
metric: price | volume | rsi | ma20 | volatility
limit: optional

JSON only.
"""

        response = await self.llm_call(prompt)

        try:

            return json.loads(response)

        except Exception:

            return {"intent": "quote"}