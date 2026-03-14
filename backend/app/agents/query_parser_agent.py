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

            Your task is to convert user queries into JSON.

            Supported intents:
            quote
            history
            indices
            sector_ranking

            Fields:
            intent (required)
            symbol (optional)
            sector (optional)
            metric (price | volume | rsi | ma20 | volatility)
            limit (optional)

            Rules:
            - Detect stock symbols like VNM, FPT, HPG.
            - Queries about price → quote.
            - Queries about historical price or chart → history.
            - Queries about VNINDEX/HNXINDEX/UPCOMINDEX → indices.
            - Queries with "top", "highest", "ranking" → sector_ranking.

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

    Convert it into JSON using the schema defined in the system prompt.

    Return JSON only.
    """

        response = await self.complete(prompt)

        try:

            response = response.strip()

            if response.startswith("```"):
                response = response.replace("```json", "").replace("```", "")

            data = json.loads(response)

            if "intent" not in data:
                data["intent"] = "quote"

            return data

        except Exception:

            return {"intent": "quote"}
    