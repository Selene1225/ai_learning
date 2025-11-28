from dotenv import load_dotenv
from agent_framework.openai import OpenAIChatClient
from agent_framework import ChatAgent
import os
import openai

load_dotenv()

openai.api_key = os.environ.get("API_KEY")
openai.base_url = os.environ.get("BASE_URL") + "/"
openai.api_type = "openai"
deployment_name = os.environ.get("MODEL")

personal = input("告诉我你希望我是历史中的哪个人？")
question = input("你想要问我什么历史问题？")
prompt = f"""
你将扮演历史上的人物：{personal}。请根据你的身份回答以下问题：{question}。请用中文回答。
"""

message = [{"role": "user", "content": prompt}]
completion = openai.chat.completions.create(model=deployment_name, messages=message, max_tokens=100, temperature=0.5)
print(completion.choices[0].message.content)