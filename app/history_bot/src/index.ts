import express, { Request, Response } from 'express';
import * as path from 'path';
import { PythonShell } from 'python-shell';
import * as dotenv from 'dotenv';

// 加载环境变量
dotenv.config({ path: '../../.env' });

const app = express();
const PORT = process.env.PORT || 3000;

// 配置中间件
app.use(express.json());
app.use(express.static(path.join(__dirname, '../public')));

// 聊天API端点
app.post('/api/chat', (req: Request, res: Response) => {
  try {
    const { person, question } = req.body;
    
    if (!person || !question) {
      return res.status(400).json({ error: '缺少必要参数：person 和 question' });
    }
    
    // 调用Python脚本
    const options = {
      args: [person, question],
      pythonPath: 'python' // 或者指定具体的Python路径
    };
    
    // 使用PythonShell的正确API
    PythonShell.run(path.join(__dirname, '../history_chat.py'), options)
      .then((results) => {
        try {
          // 解析Python脚本的输出
          const result = JSON.parse(results[0]);
          if (result.error) {
            return res.status(500).json({ error: result.error });
          }
          return res.json({ response: result.response });
        } catch (parseError) {
          console.error('解析Python输出错误:', parseError);
          return res.status(500).json({ 
            error: '解析Python输出错误', 
            details: parseError instanceof Error ? parseError.message : String(parseError) 
          });
        }
      })
      .catch((err) => {
        console.error('Python脚本执行错误:', err);
        return res.status(500).json({ 
          error: 'Python脚本执行错误', 
          details: err instanceof Error ? err.message : String(err) 
        });
      });
  } catch (error) {
    console.error('API错误:', error);
    res.status(500).json({ 
      error: '服务器内部错误',
      details: error instanceof Error ? error.message : String(error)
    });
  }
});

// 启动服务器
app.listen(PORT, () => {
  console.log(`历史人物聊天机器人服务器已启动，端口：${PORT}`);
  console.log(`访问地址：http://localhost:${PORT}`);
});
