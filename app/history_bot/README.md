# 历史人物聊天机器人

基于 TypeScript + Node.js + Python 的历史人物聊天应用

## 功能介绍

- 与历史人物进行对话
- 支持多种历史人物选择
- 基于 DeepSeek API 的 AI 对话
- 现代化的 Web 界面

## 技术栈

- **前端**: HTML + CSS + JavaScript
- **后端**: Node.js + TypeScript + Express
- **AI 核心**: Python + OpenAI API

## 项目结构

```
history_bot/
├── src/                  # TypeScript 源文件
│   └── index.ts         # 主入口文件
├── public/              # 静态资源
│   └── index.html       # 前端页面
├── history_chat.py      # Python 核心聊天逻辑
├── package.json         # Node.js 依赖配置
├── tsconfig.json        # TypeScript 配置
└── README.md            # 项目说明
```

## 环境要求

- Node.js 16+ 
- Python 3.7+  
- npm 或 yarn

## 安装依赖

### Node.js 依赖

```bash
npm install
```

### Python 依赖

```bash
pip install openai python-dotenv
```

## 配置环境变量

确保项目根目录下有 `.env` 文件，包含以下配置：

```
API_KEY='your-api-key'
BASE_URL="https://api.deepseek.com/v1"
MODEL="deepseek-chat"
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

1. 选择一个历史人物
2. 输入你的问题
3. 点击「发送问题」按钮
4. 等待 AI 回答

## 支持的历史人物

- 孔子
- 秦始皇
- 汉武帝
- 唐太宗
- 李白
- 苏轼
- 诸葛亮
- 武则天

## 开发说明

### 修改历史人物列表

编辑 `public/index.html` 中的 `<select>` 标签和历史人物快速选择区域。

### 修改 AI 模型参数

编辑 `history_chat.py` 中的 `chat_with_history_bot` 函数，调整 `max_tokens` 和 `temperature` 等参数。

## 许可证

ISC
