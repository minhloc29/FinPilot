"""
Planner agent - orchestrates other agents based on user intent
"""
from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent
from app.agents.market_data_agent import MarketDataAgent
from app.agents.portfolio_agent import PortfolioAgent
from app.agents.risk_agent import RiskAgent
from app.agents.news_agent import NewsAgent
from app.core.logger import logger
from app.core.config import settings
import tiktoken

class PlannerAgent(BaseAgent):
    """
    Orchestrates other specialized agents based on user query
    """
    TOKEN_THRESHOLD = 1000

    def __init__(self):
        super().__init__(
            api_key=settings.API_KEY,
            base_url=settings.API_ENDPOINT,
            model=settings.DEFAULT_MODEL,
            system_prompt="You are a financial planning AI that coordinates specialized agents to help users with financial decisions.",
            max_iterations=1
        )
        self.sub_agents = {
            "market_data": MarketDataAgent(),
            "portfolio": PortfolioAgent(),
            "risk": RiskAgent(),
            "news": NewsAgent()
        }

    
    
    async def chat(self, chat_history: List[Dict[str, str]]) -> str:
       
        token_length = self._calculate_token_length(chat_history)
        if token_length > self.TOKEN_THRESHOLD:
            summarized_history = await self._summarize_history(chat_history)
        else:
            summarized_history = self._format_chat_history(chat_history)

        # Extract the latest user message
        user_message = ""
        for message in reversed(chat_history):
            if message.get("role") == "user":
                user_message = message.get("content", "")
                break

        if not user_message:
            return "I didn't receive a message. How can I help you with your finances?"

        # Process the summarized history and user message
        result = await self.process(
            message=user_message,
            conversation_id=None,
            user_id=None,
            summarized_history=summarized_history
        )

        return result["message"]

    async def process(self, message: str, conversation_id: str = None, user_id: str = None, summarized_history: str = "") -> Dict[str, Any]:
        """
        Processes the user message and generates a response.
        """
        response = await self.llm_call(f"{summarized_history}\n\n{message}")
        results = {}
        return {
            "message": response,
            "conversation_id": conversation_id or "new_conversation",
            "sources": results.get("sources", []),
            "metadata": {
                "intent": "HIHI",  # Placeholder intent
                "agents_used": []
            }
        }

    async def _analyze_intent(self, message: str) -> str:
        """
        Analyze user intent from message
        """
        chat_history = [
            {
                "role": "user",
                "content": f"""Analyze the user's financial query and classify their intent.
        
User query: {message}

Classify into one of: portfolio_analysis, market_research, risk_assessment, news_analysis, general_advice"""
            }
        ]
        response = await super().chat(chat_history)
        print(f"check response: {response}")
        return response.strip().lower()

    async def _create_agent_plan(self, intent: str, message: str) -> Dict[str, Any]:
        """
        Create execution plan for agents
        """
        plan = {}

        if "portfolio" in intent:
            plan["portfolio"] = {"action": "analyze"}
        if "market" in intent or "stock" in message.lower():
            plan["market_data"] = {"action": "fetch"}
        if "risk" in intent:
            plan["risk"] = {"action": "assess"}
        if "news" in intent:
            plan["news"] = {"action": "fetch"}

        # Default to market data if no specific intent
        if not plan:
            plan["market_data"] = {"action": "fetch"}

        print(f"Check plan: {plan}")
        return plan

    async def _execute_plan(self, plan: Dict[str, Any], message: str) -> Dict[str, Any]:
        """
        Execute the agent plan
        """
        results = {"sources": [], "data": {}}

        for agent_name, config in plan.items():
            if agent_name in self.sub_agents:
                agent = self.sub_agents[agent_name]
                agent_result = await agent.process({"message": message, **config})
                results["data"][agent_name] = agent_result

        return results

    async def _synthesize_response(self, results: Dict[str, Any], message: str) -> str:
        """
        Synthesize final response from agent results
        """
        chat_history = [
            {
                "role": "user",
                "content": f"""You are a financial advisor AI. Based on the analysis results, provide a clear and helpful response to the user.

User query: {message}

Analysis results: {results['data']}

Provide a concise, actionable response:"""
            }
        ]
        response = await super().chat(chat_history)
        return response


if __name__ == "__main__":
    import asyncio

    async def main():
        agent = PlannerAgent()

        # Example conversation history
        chat_history = [
            {
                "role": "user",
                "content": "Should I invest in FPT stock for the long term?"
            }
        ]

        print("User:", chat_history[0]["content"])

        response = await agent.chat(chat_history)

        print("\nAI Response:")
        print(response)

    asyncio.run(main())