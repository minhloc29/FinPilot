import json

from app.agents.base_agent import BaseAgent
from app.core.config import settings


class QueryParserAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            api_key=settings.API_KEY,
            base_url=settings.API_ENDPOINT,
            model=settings.DEFAULT_MODEL,
            system_prompt="""
            You are a financial query parser for a Vietnamese stock market assistant.

            Your task is to convert user queries into JSON. One user query may includes many tasks

            Supported intents:
            quote
            history
            indices
            ranking
            indicator

            Fields:
            intent (required)
            symbol (optional)
            sector (optional)
            metric (optional) (rsi | ma | ema | macd | bollinger | volatility | change_percent)
            days (optional)
            limit (optional)

            Output schema:

            {
                "tasks":[
                    {
                        "intent": "...",
                        "symbol": "...",
                        "sector": "...",
                        "metric": "...",
                        "days": ...,
                        "limit": ...
                    }
                ]
            }

            Rules:
            - Detect stock symbols like VNM, FPT, HPG.
            - Queries about price → quote.
            - Queries about historical price or chart → history.
            - Queries about indicator → indicator.
            - Queries about VNINDEX/HNXINDEX/UPCOMINDEX → indices.
            - Queries with "top", "highest", "ranking" → ranking.
            - If the query mentions a time range like "last 7 days", "1 month", "30 days", extract it into `days`.
            - `limit` is used only for ranking queries (default = 5).
            - top gainers and top losers should be ranking with metric change_percent
            Output rules:
            Return ONLY valid JSON.
            No explanation.
            No markdown.
            No extra text.
            """,
            max_iterations=1,
        )
    async def parse(self, message: str):

        prompt = f"""
    User query:
    {message}

    Convert it into JSON tasks using the schema defined in the system prompt.
    Return JSON only.
    """

        response = await self.llm_call(prompt)

        try:

            response = response.strip()

            if response.startswith("```"):
                response = response.replace("```json", "").replace("```", "")

            data = json.loads(response)

            if "tasks" not in data:
                return {"tasks": [{"intent": "quote"}]}

            return data

        except Exception:

            return {"tasks": [{"intent": "quote"}]}