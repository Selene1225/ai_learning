from dotenv import load_dotenv
import os
import asyncio
from random import randint
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient

load_dotenv()

def get_random_destination() -> str:
    """Get a random vacation destination.
    
    Returns:
        str: A randomly selected destination from our predefined list
    """
    # List of popular vacation destinations around the world
    destinations = [
        "Barcelona, Spain",
        "Paris, France", 
        "Berlin, Germany",
        "Tokyo, Japan",
        "Sydney, Australia",
        "New York, USA",
        "Cairo, Egypt",
        "Cape Town, South Africa",
        "Rio de Janeiro, Brazil",
        "Bali, Indonesia"
    ]
    # Return a random destination from the list
    return destinations[randint(0, len(destinations) - 1)]

openai_chat_client = OpenAIChatClient(
    base_url=os.environ.get("BASE_URL"),
    api_key=os.environ.get("API_KEY"), 
    model_id="deepseek-chat"
)
agent = ChatAgent(
    chat_client=openai_chat_client,
    instructions="You are a helpful AI Agent that can help plan vacations for customers at random destinations.",
    tools=[get_random_destination]  # Our random destination tool function
)

response = asyncio.run(agent.run("Plan me a day trip"))
response

# 📖 Extract and Display the Travel Plan
# Get the last message from the conversation (agent's response)s
last_message = response.messages[-1]
# Extract the text content from the message
text_content = last_message.contents[0].text
# Display the formatted travel plan
print("🏖️ Travel plan:") 
print(text_content)