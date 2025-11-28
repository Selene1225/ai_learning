import os
from openai import OpenAI

API_KEY = os.getenv("API_KEY","")
BASE_URL= os.environ.get("BASE_URL") + "/"
MODEL_NAME = os.environ.get("MODEL")
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

chat_completion = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[{
        "role": "user",
        "content": "关于生成式人工智能聊天应用程序的教学课程建议两个标题。"}])