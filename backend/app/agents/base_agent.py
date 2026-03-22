import asyncio
import time
from typing import List, Dict, Any, Optional

from openai import AsyncOpenAI
from app.utils.helpers import remove_reasoning_tags
from app.db.redis_client import redis_client
from app.utils.string_utils import normalize, make_cache_key
from app.core.config import settings
import tiktoken
class BaseAgent:
    
    TOKEN_THRESHOLD = 1000
    
    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str = "gpt-4o-mini",
        system_prompt: str = "You are a helpful assistant.",
        max_iterations: int = 1,
    ):
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        self.model = model
        self.system_prompt = system_prompt
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

        cache_key = make_cache_key(messages)

        cached = redis_client.get(cache_key)

        if cached:
            print("[CACHE HIT]")
            return cached

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

        redis_client.set(
            cache_key,
            cleaned,
            ex=3600  # cache TTL = 1 hour
        )

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

    def _format_chat_history(self, chat_history: List[Dict[str, str]]) -> str:
        """
        Formats the chat history into a string.
        """
        return "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])

    async def _summarize_history(self, chat_history: List[Dict[str, str]]) -> str:
        """
        Summarizes the chat history to reduce token usage.
        """
        if not chat_history:
            return ""

        # Prepare the summarization prompt
        summarization_prompt = [
            {
                "role": "user",
                "content": f"""Summarize the following conversation history into a concise summary:

Conversation history:
{self._format_chat_history(chat_history)}

Provide a summary:"""
            }
        ]

        # Call the LLM to summarize the history
        summary = await super().chat(summarization_prompt)
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