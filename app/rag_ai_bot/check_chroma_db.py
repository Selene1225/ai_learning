import chromadb
import json

# 连接到chroma_db
print("正在连接到chroma_db...")
chroma_client = chromadb.PersistentClient(path="./chroma_db")
print("连接成功")

# 获取所有集合
print("\n获取所有集合...")
collections = chroma_client.list_collections()
print(f"共找到 {len(collections)} 个集合")

# 遍历每个集合，查看详细信息
for collection in collections:
    print(f"\n=== 集合信息 ===")
    print(f"集合名称: {collection.name}")
    print(f"集合元数据: {collection.metadata}")
    print(f"文档数量: {collection.count()}")
    
    # 查看集合中的文档
    print(f"\n=== 文档示例 (前3个) ===")
    results = collection.query(
        query_texts=["test"],
        n_results=3,
        include=["documents", "metadatas", "distances"]
    )
    
    # 打印查询结果
    print(f"查询结果: {json.dumps(results, indent=2, ensure_ascii=False)}")
    
    # 查看集合中的嵌入向量信息
    print(f"\n=== 嵌入向量信息 ===")
    # Chroma Python客户端没有直接获取嵌入向量的方法
    # 我们可以通过添加一个测试文档来间接了解
    
    try:
        # 添加一个测试文档
        test_id = "test_document"
        collection.add(
            documents=["这是一个测试文档"],
            ids=[test_id]
        )
        
        # 查询这个测试文档
        test_results = collection.query(
            query_texts=["这是一个测试文档"],
            n_results=1,
            include=["embeddings"]
        )
        
        if "embeddings" in test_results and test_results["embeddings"]:
            embeddings = test_results["embeddings"][0]
            print(f"嵌入向量数量: {len(embeddings)}")
            if embeddings:
                print(f"嵌入向量维度: {len(embeddings[0])}")
                print(f"嵌入向量示例: {embeddings[0][:5]}...")  # 只显示前5个元素
        
        # 删除测试文档
        collection.delete(ids=[test_id])
    except Exception as e:
        print(f"获取嵌入向量信息失败: {e}")
        print("无法直接获取嵌入向量信息，可能是因为Chroma客户端版本限制")

print("\n=== 数据库结构查看完成 ===")
