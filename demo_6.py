from dotenv import load_dotenv
import os
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
import openai

load_dotenv()


openai.api_key = os.environ.get("API_KEY")
openai.base_url = os.environ.get("BASE_URL") + "/"
openai.api_type = "openai"
deployment_name = os.environ.get("MODEL")

no_recipes = input("Number of recipes (for example, 5): ")
ingredients = input("List of ingredients (for example, chicken, potatoes, and carrots): ")
filter = input("Filter (for example, dairy, nuts, or gluten): ")
haved = input("我已经有的食材 (for example, salt, pepper, and olive oil): ")

# interpolate the number of recipes into the prompt an ingredients
prompt = f"给我看{no_recipes}道菜的食谱，里面有以下配料：{ingredients}。每个食谱，列出所有使用的材料，排除掉任何{filter}的食谱。用中文回答。"
messages = [{"role": "user", "content": prompt}]

# make completion
completion = openai.chat.completions.create(model=deployment_name, messages=messages)

old_prompt_result = completion.choices[0].message.content
prompt = f"列出食谱，并为每个食谱制作对应的购物清单，请不要包括我已经拥有的食材: {haved}。"

new_prompt = f"{old_prompt_result} {prompt}"
messages = [{"role": "user", "content": new_prompt}]
completion = openai.chat.completions.create(model=deployment_name, messages=messages, max_tokens=1200)

# print response
print(completion.choices[0].message.content)