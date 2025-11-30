# 测试OpenAI Embedding API是否能正常工作

from dotenv import load_dotenv
import os
import openai

# 加载环境变量
print("正在加载环境变量...")
load_dotenv(dotenv_path='../../.env')
print("环境变量加载完成")

# 配置OpenAI客户端
print("正在配置OpenAI客户端...")
openai.api_key = os.environ.get("QWEN_APP_KEY")
openai.base_url = os.environ.get("QWEN_BASE_URL") + "/"
openai.api_type = "openai"
rag_model = os.environ.get("RAG_MODEL")

print(f"OpenAI客户端配置完成")
print(f"使用的嵌入模型: {rag_model}")

# 测试文本
texts = ["这是一个测试文本，用于测试OpenAI Embedding API是否能正常工作", "这是第二个测试文本"]

print(f"\n测试文本: {texts}")

# 调用OpenAI Embedding API
try:
    print("\n正在调用OpenAI Embedding API...")
    response = openai.embeddings.create(
        model=rag_model,
        input=texts
    )
    
    print("API调用成功！")
    print(f"响应状态: 成功")
    print(f"生成的嵌入向量数量: {len(response.data)}")
    
    # 打印嵌入向量的详细信息
    for i, embedding_data in enumerate(response.data):
        print(f"\n嵌入向量 {i+1}:")
        print(f"  索引: {embedding_data.index}")
        print(f"  对象类型: {embedding_data.object}")
        print(f"  嵌入向量维度: {len(embedding_data.embedding)}")
        print(f"  嵌入向量前5个值: {embedding_data.embedding[:5]}...")
        print(f"  嵌入向量后5个值: {embedding_data.embedding[-5:]}...")
        print(f"  对应的文本: {texts[i]}")
        
    print("\nOpenAI Embedding API测试成功！")
    
except Exception as e:
    print(f"API调用失败: {e}")
    print(f"错误类型: {type(e).__name__}")
    print("请检查环境变量配置是否正确，特别是QWEN_APP_KEY、QWEN_BASE_URL和RAG_MODEL")
    print("确保您的API密钥有效，并且有访问该嵌入模型的权限")
