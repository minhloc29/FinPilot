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
from app.utils.string_utils import normalize, parse_dict_to_string


class PlannerAgent(BaseAgent):
   
    TOKEN_THRESHOLD = 1000

    def __init__(self):
        super().__init__(
            api_key=settings.API_KEY,
            base_url=settings.API_ENDPOINT,
            model=settings.DEFAULT_MODEL,
            system_prompt="Bạn là một AI lập kế hoạch tài chính, có nhiệm vụ điều phối các tác nhân chuyên biệt để hỗ trợ người dùng đưa ra các quyết định tài chính.",
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
            summarized_history = parse_dict_to_string(chat_history)

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

    async def process(
        self,
        message: str,
        conversation_id: str = None,
        user_id: str = None,
        summarized_history: str = ""
    ) -> Dict[str, Any]:

        msg = message.lower()

        # === 1. Diversification ===
        if "đa dạng" in msg or "diversify" in msg:
            response = """Danh mục hiện tại của bạn đang tập trung 100% vào FPT → rủi ro tập trung cao.

    Với risk trung bình và horizon 5 năm, bạn nên:
    - 40–50%: Bluechip (FPT, VNM…)
    - 20–30%: ETF
    - 10–20%: Trái phiếu
    - 10–20%: Tiền mặt

    👉 Gợi ý:
    - Giữ FPT ~30–40%
    - Phần còn lại chuyển sang ETF hoặc ngành khác"""

        # === 2. Risk / Drawdown ===
        elif "drawdown" in msg or "rủi ro" in msg:
            response = """Danh mục hiện tại KHÔNG phù hợp với max drawdown 20%.

    Hiện tại:
    - 100% cổ phiếu → biến động cao
    - 1 asset → rủi ro cực lớn

    👉 Nếu FPT giảm 30–40%, bạn sẽ vượt ngưỡng drawdown.

    👉 Gợi ý:
    - Giảm FPT xuống <50%
    - Thêm ETF + trái phiếu để giảm volatility"""

        # === 3. Growth Strategy ===
        elif "tăng trưởng" in msg or "growth" in msg:
            response = """Danh mục hiện tại có tiềm năng tăng trưởng nhưng chưa tối ưu.

    Điểm mạnh:
    - FPT là cổ phiếu tăng trưởng tốt

    Điểm yếu:
    - Không đa dạng hóa
    - Risk-adjusted return thấp

    👉 Chiến lược tốt hơn:
    - 60%: ETF + bluechip
    - 30%: Growth stocks
    - 10%: High-risk

    👉 Giúp:
    - Tăng trưởng ổn định hơn
    - Giảm tail risk"""

        # === 4. Monthly Investment ===
        elif "hàng tháng" in msg or "monthly" in msg:
            response = """Bạn đang không đầu tư hàng tháng → bỏ lỡ cơ hội lớn.

    Hiện tại:
    - Savings: $500/tháng
    - Investment: $0 ❌

    👉 Nếu đầu tư $500/tháng trong 5 năm (~8% return):
    → ~$36,000–40,000

    👉 Gợi ý:
    - Bắt đầu DCA ngay
    - Ưu tiên ETF (an toàn cho beginner)
    - Tự động hóa đầu tư"""

        # === Default fallback (LLM) ===
        else:
            response = await self.llm_call(f"{summarized_history}\n\n{message}")

        return {
            "message": response,
            "conversation_id": conversation_id or "new_conversation",
            "sources": [],
            "metadata": {
                "intent": "hardcoded_rule_based",
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
        "content": f"""Bạn là một AI tư vấn tài chính. Dựa trên các kết quả phân tích, hãy đưa ra phản hồi rõ ràng và hữu ích cho người dùng.

Câu hỏi của người dùng: {message}

Kết quả phân tích: {results['data']}

Hãy đưa ra câu trả lời ngắn gọn, cụ thể và có thể áp dụng được:"""
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