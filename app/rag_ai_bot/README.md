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
- **RAG 核心**: Python + Chroma + OpenAI API
- **数据集**: 奥斯卡获奖数据集 (Kaggle)

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
├── package.json         # Node.js 依赖配置
├── requirements.txt     # Python 依赖配置
└── README.md            # 项目说明
```

## 环境要求

- Node.js 16+ 
- Python 3.7+  
- npm 或 yarn
- 有效的 OpenAI API 密钥

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
QWEN_APP_KEY=sk-234
QWEN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
RAG_MODEL=text-embedding-v3
```

## 数据准备

在首次运行应用前，需要加载奥斯卡获奖数据集到 Chroma 向量数据库：

```bash
python load_data.py
```

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

## 许可证

ISC
