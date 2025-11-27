from dotenv import load_dotenv
import os
import openai
import sys
import json

load_dotenv(dotenv_path='../../.env')

# 配置OpenAI客户端
openai.api_key = os.environ.get("API_KEY")
openai.base_url = os.environ.get("BASE_URL") + "/"
openai.api_type = "openai"
deployment_name = os.environ.get("MODEL")

def chat_with_history_bot(person, question):
    """
    与历史人物聊天的核心函数
    Args:
        person: 历史人物名称
        question: 用户问题
    Returns:
        历史人物的回答
    """
    prompt = f"""
    你将扮演历史上的人物：{person}。请根据你的身份回答以下问题：{question}。请用中文回答。
    """

    message = [{"role": "user", "content": prompt}]
    completion = openai.chat.completions.create(
        model=deployment_name, 
        messages=message, 
        max_tokens=500, 
        temperature=0.5
    )
    return completion.choices[0].message.content

if __name__ == "__main__":
    # 从命令行获取参数
    if len(sys.argv) < 3:
        print(json.dumps({"error": "缺少参数：需要历史人物名称和问题"}))
        sys.exit(1)
    
    person = sys.argv[1]
    question = sys.argv[2]
    
    try:
        response = chat_with_history_bot(person, question)
        print(json.dumps({"response": response}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
