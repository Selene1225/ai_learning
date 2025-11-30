# 奥斯卡获奖数据 RAG AI Bot

基于 Chroma 的奥斯卡获奖数据集智能问答系统

## 功能介绍

- 基于奥斯卡获奖数据集的智能问答
- 使用 Chroma 向量数据库进行高效的相似性搜索
- 集成 LLM 生成高质量回答
- 现代化的 Web 界面
- 支持自然语言查询

## 技术栈

- **前端**: HTML + CSS + JavaScript
- **后端**: Node.js + TypeScript + Express
- **RAG 核心**: Python + Chroma (自定义OpenAI嵌入函数) + OpenAI API
- **数据集**: 奥斯卡获奖数据集 (Kaggle, 2022年及以后)

## 项目结构

```
rag_ai_bot/
├── public/              # 静态资源
│   └── index.html       # 前端页面
├── src/                 # TypeScript 源文件
│   └── index.ts         # 主入口文件
├── chroma_db/           # Chroma 向量数据库持久化目录
├── rag_chat.py          # Python RAG 核心聊天逻辑
├── load_data.py         # 数据加载和处理脚本
├── recreate_collection.py  # 重新创建集合脚本
├── check_chroma_db.py      # 查看数据库结构脚本
├── package.json         # Node.js 依赖配置
├── requirements.txt     # Python 依赖配置
└── README.md            # 项目说明
```

## 环境要求

- Node.js 16+ 
- Python 3.7+  
- npm 或 yarn
- 有效的 OpenAI API 密钥（用于 LLM 调用）

## 安装依赖

### Node.js 依赖

```bash
npm install
```

### Python 依赖

```bash
pip install -r requirements.txt
```

## 配置环境变量

确保项目根目录下有 `.env` 文件，包含以下配置：

```
# deepseek
API_KEY=sk-xxx
BASE_URL=https://api.deepseek.com/v1
MODEL=deepseek-chat

# qwen
QWEN_APP_KEY=sk-xxx
QWEN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
TOOL_CALL_MODEL=qwen3-max
CHAT_MODEL=qwen3-max
RAG_MODEL=text-embedding-v2
```

## 数据准备

在首次运行应用前，需要加载奥斯卡获奖数据集到 Chroma 向量数据库：

```bash
python load_data.py
```

### 数据处理逻辑

数据加载脚本会执行以下处理：
1. 从 Kaggle 加载完整的奥斯卡获奖数据集
2. **只保留 2022 年及以后的数据**
3. **过滤掉空的 film 条目**
4. 使用自定义 OpenAI 嵌入函数生成向量
5. 将处理后的数据分批插入 Chroma 数据库

### 数据量

处理后的数据量约为 **481 条记录**（基于 2022 年及以后的奥斯卡获奖数据）

## 运行应用

### 开发模式

```bash
npm run dev
```

### 生产模式

1. 编译 TypeScript：
```bash
npm run build
```

2. 启动应用：
```bash
npm start
```

## 访问应用

打开浏览器访问：`http://localhost:3000`

## 使用说明

1. 在输入框中输入您的问题，例如：
   - "谁获得了第90届奥斯卡最佳影片？"
   - "莱昂纳多·迪卡普里奥获得过几次奥斯卡奖？"
   - "哪部电影获得的奥斯卡奖项最多？"
2. 点击「发送问题」按钮
3. 等待 AI 回答

## 开发说明

### 查看数据库结构

可以使用以下脚本查看 Chroma 数据库的结构：

```bash
python check_chroma_db.py
```

### 重新创建集合

如果需要重新创建集合（例如嵌入维度不匹配时），可以使用以下脚本：

```bash
python recreate_collection.py
```

### 修改数据集

编辑 `load_data.py` 文件，您可以：
- 更改数据集文件（默认为 `the_oscar_award.csv`）
- 调整数据预处理逻辑
- 修改文档构建方式
- 调整插入到 Chroma 的数据量

### 修改 RAG 逻辑

编辑 `rag_chat.py` 文件，您可以：
- 调整相似性搜索的结果数量
- 修改 prompt 模板
- 调整 LLM 调用参数

### 修改前端界面

编辑 `public/index.html` 文件，您可以：
- 调整页面样式
- 修改输入输出区域
- 添加新的交互功能

## 注意事项

1. 本项目使用**自定义 OpenAI 嵌入函数**（`text-embedding-v2`），需要确保环境变量中配置了有效的 `QWEN_APP_KEY` 和 `QWEN_BASE_URL`
2. 数据加载脚本会处理**所有 2022 年及以后**的有效数据，不限制数据量
3. 数据加载使用**分批处理**（每批 10 条），避免 API 速率限制
4. 如果遇到嵌入维度不匹配的错误，可以使用 `recreate_collection.py` 脚本重新创建集合
5. 可以使用 `check_chroma_db.py` 脚本查看数据库结构
6. 确保 `load_data.py` 和 `rag_chat.py` 使用**相同的嵌入函数**，否则会导致向量空间不一致
7. 项目使用 **OpenAI 1.0.0+ API 格式**，确保 Python 依赖中的 `openai` 包版本兼容

## 许可证

ISC
