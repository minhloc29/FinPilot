import asyncio
import time
from typing import List, Dict, Any, Optional

from openai import AsyncOpenAI
from app.utils.helpers import remove_reasoning_tags


class BaseAgent:
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

        return remove_reasoning_tags(full_response)

    async def complete(self, prompt: str) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt},
        ]
        return await self.stream_response(messages)

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
