import chromadb
import sys

# 初始化Chroma客户端
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# 删除现有集合
print("正在删除现有集合...")
try:
    chroma_client.delete_collection(name="oscar_awards")
    print("集合删除成功")
except Exception as e:
    print(f"集合删除失败: {e}")
    sys.exit(1)

print("\n集合已成功删除，现在可以重新运行load_data.py来加载数据")
