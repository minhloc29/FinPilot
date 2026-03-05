"""
Planner agent - orchestrates other agents based on user intent
"""
from typing import Dict, Any
from app.agents.base_agent import BaseAgent
from app.agents.market_data_agent import MarketDataAgent
from app.agents.portfolio_agent import PortfolioAgent
from app.agents.risk_agent import RiskAgent
from app.agents.news_agent import NewsAgent
from app.services.llm_service import LLMService
from app.core.logger import logger


class PlannerAgent(BaseAgent):
    """
    Orchestrates other specialized agents based on user query
    """

    def __init__(self):
        super().__init__(
            name="Planner",
            description="Analyzes user intent and coordinates specialized agents"
        )
        self.llm_service = LLMService()
        self.sub_agents = {
            "market_data": MarketDataAgent(),
            "portfolio": PortfolioAgent(),
            "risk": RiskAgent(),
            "news": NewsAgent()
        }

    async def process(self, message: str, conversation_id: str = None, user_id: str = None) -> Dict[str, Any]:
        """
        Process user message and coordinate agents
        """
        logger.info(f"Planning response for message: {message[:50]}...")

        # Analyze user intent
        intent = await self._analyze_intent(message)

        # Determine which agents to invoke
        agent_plan = await self._create_agent_plan(intent, message)

        # Execute plan
        results = await self._execute_plan(agent_plan, message)

        # Synthesize final response
        response = await self._synthesize_response(results, message)

        return {
            "message": response,
            "conversation_id": conversation_id or "new_conversation",
            "sources": results.get("sources", []),
            "metadata": {
                "intent": intent,
                "agents_used": list(agent_plan.keys())
            }
        }

    async def _analyze_intent(self, message: str) -> str:
        """
        Analyze user intent from message
        """
        prompt = f"""Analyze the user's financial query and classify their intent.
        
User query: {message}

Classify into one of: portfolio_analysis, market_research, risk_assessment, news_analysis, general_advice
"""
        response = await self.llm_service.generate(prompt, max_tokens=50)
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
        prompt = f"""You are a financial advisor AI. Based on the analysis results, provide a clear and helpful response to the user.

User query: {message}

Analysis results: {results['data']}

Provide a concise, actionable response:"""

        response = await self.llm_service.generate(prompt, max_tokens=500)
        return response

    def get_system_prompt(self) -> str:
        return "You are a financial planning AI that coordinates specialized agents to help users with financial decisions."
