from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from zoneinfo import ZoneInfo
import json
import os
from dotenv import load_dotenv
import openai

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 加载环境变量
load_dotenv(dotenv_path="../../.env")
api_key = os.getenv("QWEN_APP_KEY")
base_url = os.getenv("QWEN_BASE_URL")
model_name = os.getenv("TOOL_CALL_MODEL")

# 加载时区配置文件
with open('timezone_config.json', 'r', encoding='utf-8') as f:
    timezone_config = json.load(f)
    TIMEZONE_DATA = timezone_config['timezones']

# 初始化 OpenAI 客户端
openai.api_key = api_key
openai.base_url = base_url
openai.api_type = "openai"

# 工具定义
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前城市的时间",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "提供location的英文去获取时间, e.g. San Francisco"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

def get_current_time(location: str) -> str:
    """获取指定城市的当前时间"""
    location_lower = location.lower()
    
    # 查找城市对应的时区
    for key, timezone in TIMEZONE_DATA.items():
        if key in location_lower:
            current_time = datetime.now(ZoneInfo(timezone)).strftime("%I:%M %p")
            return json.dumps({
                "location": location,
                "current_time": current_time
            })
    
    return json.dumps({
        "location": location,
        "current_time": "unknown"
    })

@app.route('/api/ai-time', methods=['POST'])
def ai_time():
    """使用 AI 处理自然语言请求，获取城市时间"""
    data = request.get_json()
    user_query = data.get('query', '').strip()
    
    if not user_query:
        return jsonify({'error': '请求内容不能为空'}), 400
    
    try:
        # 第一步：发送用户请求给 AI，获取工具调用
        messages = [{"role": "user", "content": user_query}]
        response = openai.chat.completions.create(
            model=model_name,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        messages.append(response_message)
        
        # 第二步：处理工具调用
        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                if tool_call.function.name == "get_current_time":
                    tool_args = json.loads(tool_call.function.arguments)
                    time_response = get_current_time(tool_args["location"])
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": "get_current_time",
                        "content": time_response
                    })
                else:
                    return jsonify({'error': f'未知的工具调用: {tool_call.function.name}'}), 400
            
            # 第三步：获取最终响应
            final_response = openai.chat.completions.create(
                model=model_name,
                messages=messages,
            )
            
            return jsonify({
                'response': final_response.choices[0].message.content
            })
        else:
            # 如果没有工具调用，直接返回 AI 响应
            return jsonify({
                'response': response_message.content
            })
    
    except Exception as e:
        return jsonify({'error': f'处理请求时出错: {str(e)}'}), 500

@app.route('/api/time', methods=['GET'])
def get_time():
    """获取指定城市的当前时间（直接调用）"""
    city = request.args.get('city', '').strip()
    
    if not city:
        return jsonify({'error': '城市名称不能为空'}), 400
    
    time_response = json.loads(get_current_time(city))
    return jsonify(time_response)

@app.route('/api/cities', methods=['GET'])
def get_cities():
    """获取支持的所有城市列表"""
    cities = list(TIMEZONE_DATA.keys())
    return jsonify({'cities': cities})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)