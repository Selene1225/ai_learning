from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from zoneinfo import ZoneInfo
import json
import os

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 加载时区配置文件
with open('timezone_config.json', 'r', encoding='utf-8') as f:
    timezone_config = json.load(f)
    TIMEZONE_DATA = timezone_config['timezones']

@app.route('/api/time', methods=['GET'])
def get_time():
    """获取指定城市的当前时间"""
    city = request.args.get('city', '').strip()
    
    if not city:
        return jsonify({'error': '城市名称不能为空'}), 400
    
    location_lower = city.lower()
    
    # 查找城市对应的时区
    for key, timezone in TIMEZONE_DATA.items():
        if key in location_lower:
            current_time = datetime.now(ZoneInfo(timezone)).strftime("%I:%M %p")
            return jsonify({
                'location': city,
                'current_time': current_time
            })
    
    return jsonify({
        'location': city,
        'current_time': 'unknown'
    })

@app.route('/api/cities', methods=['GET'])
def get_cities():
    """获取支持的所有城市列表"""
    cities = list(TIMEZONE_DATA.keys())
    return jsonify({'cities': cities})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)