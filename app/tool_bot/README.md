# 全球城市时间查询应用

这是一个基于 Python 和 JavaScript 的全球城市时间查询应用，支持查询全球超过 1000 个城市的当前时间，同时集成了 AI 自然语言处理功能。

## 功能特性

- 支持全球超过 1000 个城市的时间查询
- 提供友好的 Web 界面，支持标签页切换
- 支持直接查询和 AI 自然语言查询两种方式
- 支持热门城市快速选择
- 提供 RESTful API 接口
- 时区数据可扩展
- 集成 AI 模型，支持自然语言理解和工具调用

## 技术栈

- **前端**：HTML、CSS、JavaScript
- **后端**：Python、Flask
- **AI 模型**：OpenAI API
- **数据存储**：JSON 配置文件

## 项目结构

```
app/tool_bot/
├── index.html          # 前端页面
├── app.py              # Flask 后端服务（集成 AI 功能）
├── requirements.txt    # 后端依赖
├── timezone_config.json # 时区配置文件
├── tool_chat_bot.py    # 原始的工具调用脚本
└── README.md           # 项目说明文档
```

## 安装和运行

### 1. 配置环境变量

在项目根目录下创建或编辑 `.env` 文件，添加以下配置：

```
QWEN_APP_KEY=your_api_key
QWEN_BASE_URL=your_api_base_url
TOOL_CALL_MODEL=your_model_name
```

### 2. 安装依赖

打开终端，进入项目目录，安装后端依赖：

```bash
cd d:\github\ai_learning\app\tool_bot
pip install -r requirements.txt
```

### 3. 启动后端服务

```bash
python app.py
```

服务启动后，会显示类似以下信息：

```
* Serving Flask app 'app'
* Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
* Running on http://192.168.11.112:5000
Press CTRL+C to quit
* Restarting with stat
* Debugger is active!
* Debugger PIN: 611-119-298
```

### 4. 访问前端页面

在浏览器中打开 `index.html` 文件：

- 直接双击 `d:\github\ai_learning\app\tool_bot\index.html` 文件
- 或在浏览器地址栏中输入文件的完整路径

## 使用说明

### 1. 直接查询

1. 切换到「直接查询」标签页
2. 在输入框中输入城市名称（英文，例如：Beijing、New York、London）
3. 点击「查询时间」按钮或按回车键
4. 查看查询结果

### 2. 通过热门城市标签查询

1. 切换到「直接查询」标签页
2. 点击页面下方的热门城市标签（例如：北京、上海、纽约等）
3. 自动显示查询结果

### 3. AI 自然语言查询

1. 切换到「AI 自然语言查询」标签页
2. 输入自然语言请求（例如："北京现在几点？"、"纽约的时间是多少？"）
3. 点击「AI 查询」按钮或按 Ctrl+Enter
4. 查看 AI 生成的自然语言响应

## API 接口

### 1. 查询城市时间（直接调用）

**请求 URL**：
```
GET http://localhost:5000/api/time?city={城市名称}
```

**请求示例**：
```
curl http://localhost:5000/api/time?city=Beijing
```

**响应示例**：
```json
{
  "current_time": "06:13 PM",
  "location": "Beijing"
}
```

### 2. AI 自然语言查询

**请求 URL**：
```
POST http://localhost:5000/api/ai-time
```

**请求体**：
```json
{
  "query": "北京现在几点？"
}
```

**请求示例**：
```
curl -X POST -H "Content-Type: application/json" -d '{"query": "北京现在几点？"}' http://localhost:5000/api/ai-time
```

**响应示例**：
```json
{
  "response": "北京现在的时间是下午6点13分"
}
```

### 3. 获取支持的城市列表

**请求 URL**：
```
GET http://localhost:5000/api/cities
```

**请求示例**：
```
curl http://localhost:5000/api/cities
```

**响应示例**：
```json
{
  "cities": ["beijing", "shanghai", "guangzhou", ...]
}
```

## 扩展城市数据

要添加新的城市，只需编辑 `timezone_config.json` 文件，按照以下格式添加城市和对应的时区：

```json
{
  "timezones": {
    "城市名称": "时区标识符",
    "另一个城市": "另一个时区标识符"
  }
}
```

例如：
```json
{
  "timezones": {
    "beijing": "Asia/Shanghai",
    "new york": "America/New_York"
  }
}
```

时区标识符可以参考 [IANA 时区数据库](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)。

## 注意事项

- 确保输入的城市名称为英文（直接查询模式）
- AI 自然语言查询支持中文和英文
- 后端服务必须保持运行状态，前端页面才能正常获取数据
- 确保环境变量配置正确，AI 功能需要有效的 API 密钥
- 如果遇到问题，可以查看后端服务终端的日志信息
- 支持的城市列表可以在 `timezone_config.json` 文件中查看和扩展

## 许可证

本项目采用 MIT 许可证。
