"""
Tests for agent functionality
"""
from app.agents.base_agent import BaseAgent
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

API_KEY = os.getenv("MODAS_API_KEY")
API_ENDPOINT = os.getenv("MODAS_API_ENDPOINT")


async def main():
    agent = BaseAgent(
        api_key=API_KEY,
        base_url=API_ENDPOINT,
        model="Qwen3-32B"
    )

    chat_history = []

    while True:
        user_input = input("\nUser: ")
        chat_history.append({"role": "user", "content": user_input})

        print("\nAssistant: ", end="")
        await agent.chat(chat_history)

asyncio.run(main())