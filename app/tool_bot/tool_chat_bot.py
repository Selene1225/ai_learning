from semantic_kernel.functions import kernel_function
from dotenv import load_dotenv
import os
import openai
import pytz
from datetime import datetime
from zoneinfo import ZoneInfo
import json

load_dotenv(dotenv_path="../../.env")
api_key = os.getenv("QWEN_APP_KEY")
base_url = os.getenv("QWEN_BASE_URL")
model_name = os.getenv("TOOL_CALL_MODEL")

# Load timezone data from configuration file
with open('timezone_config.json', 'r', encoding='utf-8') as f:
    timezone_config = json.load(f)
    TIMEZONE_DATA = timezone_config['timezones']

def get_current_time(location: str) -> str:
    """Get the current time for a given location"""
    print(f"get_current_time called with location: {location}")  
    location_lower = location.lower()
    
    for key, timezone in TIMEZONE_DATA.items():
        if key in location_lower:
            print(f"Timezone found for {key}")  
            current_time = datetime.now(ZoneInfo(timezone)).strftime("%I:%M %p")
            return json.dumps({
                "location": location,
                "current_time": current_time
            })
  
    print(f"No timezone data found for {location_lower}")  
    return json.dumps({"location": location, "current_time": "unknown"})

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前城市的时间",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "提供location的英文去获取时间, e.g. San Francisco"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

messages = [{
    "role": "user",
    "content": input("你想知道哪个城市的时间? ")
}]

openai.api_key = api_key
openai.base_url = base_url
openai.api_type = "openai"
response = openai.chat.completions.create(
    model=model_name,
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

response_message = response.choices[0].message
messages.append(response_message)

if response_message.tool_calls:
    for tool_call in response_message.tool_calls:
        if tool_call.function.name == "get_current_time":
            tool_args = json.loads(tool_call.function.arguments)
            print(tool_args)
            time_response = get_current_time(tool_args["location"])
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": "get_current_time",
                "content": time_response
            })
        else:
            print(f"Unknown tool call: {tool_call.function.name}")
final_response = openai.chat.completions.create(
    model=model_name,
    messages=messages,
)

print(final_response.choices[0].message.content)