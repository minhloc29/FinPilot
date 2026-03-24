import asyncio
from backend.app.agents.base_agent import BaseAgent

async def test_continuous_chat():
    # Initialize the BaseAgent with mock parameters
    agent = BaseAgent(
        api_key="mock_api_key",
        base_url="https://mockapi.openai.com",
        model="gpt-4o-mini",
        system_prompt="You are a helpful assistant.",
        max_iterations=5
    )

    # Mock chat history
    chat_history = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm good, thank you! How can I assist you today?"}
    ]

    try:
        # Run the chat method continuously
        while True:
            response = await agent.chat(chat_history)
            print("Agent Response:", response)

            # Append the response to the chat history
            chat_history.append({"role": "assistant", "content": response})

            # Simulate user input for continuous testing
            user_input = input("Enter user message: ")
            chat_history.append({"role": "user", "content": user_input})

            # Break the loop if user types 'exit'
            if user_input.lower() == "exit":
                print("Exiting continuous chat test.")
                break

    except KeyboardInterrupt:
        print("Test interrupted by user.")

if __name__ == "__main__":
    asyncio.run(test_continuous_chat())