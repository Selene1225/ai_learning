from dotenv import load_dotenv
import os
import openai
import sys
import json
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings

# 加载环境变量
load_dotenv(dotenv_path='../../.env')

# 配置OpenAI客户端
openai.api_key = os.environ.get("QWEN_APP_KEY")
openai.base_url = os.environ.get("QWEN_BASE_URL") + "/"
openai.api_type = "openai"
deployment_name = os.environ.get("CHAT_MODEL")

# 自定义OpenAI嵌入函数
class OpenAIEmbeddingFunction(EmbeddingFunction):
    def __init__(self):
        # 初始化方法，满足Chroma未来版本的要求
        pass
    
    def __call__(self, input: Documents) -> Embeddings:
        # 调用OpenAI API生成嵌入（使用OpenAI 1.0.0+新API格式）
        client = openai.OpenAI(
            api_key=openai.api_key,
            base_url=openai.base_url
        )
        response = client.embeddings.create(
            model="text-embedding-v2",
            input=input
        )
        # 提取嵌入向量
        embeddings = [item.embedding for item in response.data]
        return embeddings

# 初始化Chroma客户端和集合
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# 获取集合，使用自定义OpenAI嵌入函数
collection = chroma_client.get_collection(
    name="oscar_awards",
    embedding_function=OpenAIEmbeddingFunction()
)

def rag_chat(question):
    """
    基于奥斯卡获奖数据集的RAG聊天核心函数
    Args:
        question: 用户问题
    Returns:
        LLM生成的回答
    """
    try:
        # 1. 在Chroma中搜索相关文档
        results = collection.query(
            query_texts=[question],
            n_results=5
        )
        
        # 2. 构建上下文
        contexts = results['documents'][0] if results['documents'] and results['documents'][0] else []
        
        if not contexts:
            context_str = "没有找到相关的奥斯卡获奖数据。"
        else:
            context_str = "\n".join([f"相关数据 {i+1}: {doc}" for i, doc in enumerate(contexts)])
        
        # 3. 构建prompt
        prompt = f"""
        你是一个基于奥斯卡获奖数据集的智能问答助手。请根据提供的上下文信息，回答用户的问题。
        
        上下文信息：
        {context_str}
        
        用户问题：{question}
        
        请基于上下文信息，用中文回答用户的问题。如果上下文信息不足，请明确说明。
        """
        
        # 4. 调用LLM生成回答
        messages = [{"role": "user", "content": prompt}]
        client = openai.OpenAI(
            api_key=openai.api_key,
            base_url=openai.base_url
        )
        completion = client.chat.completions.create(
            model=os.environ.get("CHAT_MODEL"), 
            messages=messages, 
            max_tokens=1000, 
            temperature=0.5
        )
        
        return completion.choices[0].message.content
    except Exception as e:
        # 直接抛出异常，不输出额外信息
        raise

if __name__ == "__main__":
    # 从命令行获取参数
    if len(sys.argv) < 2:
        print(json.dumps({"error": "缺少参数：需要用户问题"}))
        sys.exit(1)
    
    question = sys.argv[1]
    
    try:
        response = rag_chat(question)
        print(json.dumps({"response": response}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))