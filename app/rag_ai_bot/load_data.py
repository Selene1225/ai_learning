# 数据加载和处理脚本
# 用于从奥斯卡获奖数据集加载数据并存储到Chroma向量数据库

import kagglehub
from kagglehub import KaggleDatasetAdapter
import pandas as pd
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from dotenv import load_dotenv
import os
import openai

# 加载环境变量
load_dotenv(dotenv_path='../../.env')

# 配置OpenAI客户端
openai.api_key = os.environ.get("QWEN_APP_KEY")
openai.base_url = os.environ.get("QWEN_BASE_URL") + "/"
openai.api_type = "openai"

# 初始化Chroma客户端和集合
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# 获取或创建集合 - 使用Chroma内置的嵌入模型
collection = chroma_client.get_or_create_collection(
    name="oscar_awards"
    # 不指定embedding_function，使用Chroma内置的嵌入模型
)

def load_and_process_data():
    """
    加载奥斯卡获奖数据集并处理存储到Chroma向量数据库
    """
    print("开始加载奥斯卡获奖数据集...")
    
    try:
        # 从Kaggle加载数据集
        df = kagglehub.load_dataset(
            KaggleDatasetAdapter.PANDAS,
            "unanimad/the-oscar-award",
            "the_oscar_award.csv",
        )
        
        print(f"数据集加载成功，共 {len(df)} 条记录")
        print("数据集前5行:")
        print(df.head())
        
        # 数据预处理
        print("开始数据预处理...")
        
        # 选择相关列
        relevant_columns = ['year_ceremony', 'category', 'name', 'film', 'winner']
        
        # 过滤掉缺失值
        df = df[relevant_columns].dropna()
        
        # 限制数据量（可选，用于测试）
        df = df.head(100)  # 只使用前1000条数据进行测试
        
        # 构建文档列表
        documents = []
        ids = []
        metadatas = []
        
        for idx, row in df.iterrows():
            # 构建文档内容
            doc_content = f"颁奖年份: {row['year_ceremony']}\n"
            doc_content += f"奖项类别: {row['category']}\n"
            doc_content += f"获奖者: {row['name']}\n"
            doc_content += f"电影名称: {row['film']}\n"
            doc_content += f"是否获奖: {'是' if row['winner'] else '否'}\n"
            
            documents.append(doc_content)
            ids.append(f"oscar_{idx}")
            
            # 构建元数据
            metadata = {
                'year_ceremony': row['year_ceremony'],
                'category': row['category'],
                'name': row['name'],
                'film': row['film'],
                'winner': row['winner']
            }
            metadatas.append(metadata)
        
        print(f"数据预处理完成，共生成 {len(documents)} 个文档")
        
        # 将数据存储到Chroma
        print("开始将数据存储到Chroma向量数据库...")
        
        # 分批次插入数据，避免API限制（OpenAI API批次大小限制为10）
        batch_size = 10
        for i in range(0, len(documents), batch_size):
            end_idx = min(i + batch_size, len(documents))
            batch_docs = documents[i:end_idx]
            batch_ids = ids[i:end_idx]
            batch_metadatas = metadatas[i:end_idx]
            
            collection.add(
                documents=batch_docs,
                ids=batch_ids,
                metadatas=batch_metadatas
            )
            
            print(f"已插入批次 {i//batch_size + 1}/{(len(documents)+batch_size-1)//batch_size}")
        
        print("数据存储完成！")
        
        # 验证数据
        collection_stats = collection.count()
        print(f"Chroma集合中共有 {collection_stats} 个文档")
        
    except Exception as e:
        print(f"数据加载和处理失败: {e}")
        raise

if __name__ == "__main__":
    load_and_process_data()