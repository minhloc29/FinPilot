import asyncio
import time
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from app.utils.helpers import remove_reasoning_tags
from app.utils.string_utils import normalize, parse_dict_to_string

from app.utils.file_utils import read_txt

import tiktoken
class BaseAgent:
    
    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str = "gpt-4o-mini",
        system_prompt: str = "Bạn là 1 trợ lý tài chính thông minh.",
        max_iterations: int = 1,
    ):
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        self.model = model
        self.system_prompt = system_prompt
        self.summarization_prompt = read_txt("backend/prompts/conversation_summarization_prompt.txt")
        self.max_iterations = max_iterations

    def build_context(
        self,
        chat_history: List[Dict[str, str]],
    ) -> List[Dict[str, str]]:
        return [
            {"role": "system", "content": self.system_prompt},
            *chat_history,
        ]

    async def stream_response(
        self,
        messages: List[Dict[str, str]],
    ) -> str:

        full_response = ""
        start_time = time.perf_counter()

        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
        )

        async for chunk in stream:
            
            if not chunk.choices:
                continue

            choice = chunk.choices[0]

            if not hasattr(choice, "delta") or choice.delta is None:
                continue
            delta = getattr(choice.delta, "content", None)

            if delta:
                print(delta, end="", flush=True)
                full_response += delta

        latency = (time.perf_counter() - start_time) * 1000
        print(f"\n\n[Latency: {latency:.2f} ms]")

        cleaned = remove_reasoning_tags(full_response)
        return cleaned

    async def chat(
        self,
        chat_history: List[Dict[str, str]],
    ) -> str:
        iteration = 0
        response = ""

        while iteration < self.max_iterations:
            iteration += 1
            context = self.build_context(chat_history)

            response = await self.stream_response(context)

            chat_history.append(
                {"role": "assistant", "content": response}
            )

            break  

        return response

    def _calculate_token_length(self, chat_history: List[Dict[str, str]]) -> int:
       
        encoding = tiktoken.encoding_for_model("gpt-4o")
        token_count = 0
        for message in chat_history:
            content = message.get("content", "")
            token_count += len(encoding.encode(content))
        return token_count

    async def _summarize_history(self, chat_history: List[Dict[str, str]]) -> str:
        
        if not chat_history:
            return ""

        full_summarization_prompt = self.summarization_prompt.format(
            history = parse_dict_to_string(chat_history)
        )
        
        summary = self.llm_call(full_summarization_prompt)
        return summary.strip()
    
    async def llm_call(
        self,
        prompt: str
    ) -> str:

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt},
            ],
            stream=False,
        )

        return response.choices[0].message.content
    
    
if __name__ == "__main__":
    import asyncio
    import os
    from dotenv import load_dotenv
    
    async def main():
        
        load_dotenv()
        
        API_KEY = os.getenv("API_KEY")
        API_ENDPOINT = os.getenv("API_ENDPOINT")
        
        agent = BaseAgent(
            api_key=API_KEY,
            base_url=API_ENDPOINT,
            model="gemma-3-27b-it",
            system_prompt="You are a helpful assistant.",
            max_iterations=1,
        )

        chat_history = [
            {"role": "user", "content": "Hello, who are you?"}
        ]

        print("\n=== Response ===")
        response = await agent.chat(chat_history)
        print("\nFinal Response:", response)

    asyncio.run(main())