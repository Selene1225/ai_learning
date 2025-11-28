from dotenv import load_dotenv
import os
import asyncio
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient

load_dotenv()

client = OpenAIChatClient(
    base_url=os.environ.get("BASE_URL"),
    api_key=os.environ.get("API_KEY"),
    model_id="deepseek-chat"
)


code_str="""
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get('name', 'World')
    return f'Hello, {name}!'

if __name__ == '__main__':
    app.run()
"""
agent = ChatAgent(
    chat_client=client,
    instructions=f"读python脚本 {code_str}"
)


res = asyncio.run(agent.run("改正代码的错误，并根据性能问题进行优化，改进3次以内"))
for i, msg in enumerate(res.messages):
    print(f"-----------msg index: {i}-----------")
    print(msg.contents[0].text)