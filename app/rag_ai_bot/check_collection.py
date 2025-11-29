import chromadb
import sys

# 初始化Chroma客户端
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# 获取集合
collection = chroma_client.get_collection(name="oscar_awards")

# 打印集合信息
print("集合名称:", collection.name)
print("集合元数据:", collection.metadata)
print("集合文档数量:", collection.count())

# 尝试获取集合配置
print("\n尝试获取集合配置...")
# Chroma Python客户端没有直接获取嵌入维度的方法
# 我们可以通过查询一个简单的文档来间接了解

try:
    # 尝试查询一个简单的文档
    results = collection.query(
        query_texts=["test"],
        n_results=1
    )
    print("查询成功，集合配置正常")
except Exception as e:
    print(f"查询失败: {e}")
    print("\n建议重新创建集合，使用正确的嵌入模型")
