import express, { Request, Response } from 'express';
import * as path from 'path';
import { PythonShell } from 'python-shell';
import * as dotenv from 'dotenv';

// 加载环境变量
console.log('正在加载环境变量...');
dotenv.config({ path: '../../../.env' });
console.log('环境变量加载完成');

const app = express();
const PORT = process.env.PORT || 3000;

// 配置中间件
app.use(express.json());
app.use(express.static(path.join(__dirname, '../public')));

// 聊天API端点
app.post('/api/chat', (req: Request, res: Response) => {
  try {
    console.log('收到API请求:', req.body);
    const { question } = req.body;
    
    if (!question) {
      return res.status(400).json({ error: '缺少必要参数：question' });
    }
    
    // 调用Python脚本
    const options = {
      args: [question],
      pythonPath: 'python' // 或者指定具体的Python路径
    };
    
    // 使用PythonShell调用rag_chat.py脚本
    PythonShell.run(path.join(__dirname, '../rag_chat.py'), options)
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

// 健康检查端点
app.get('/health', (req: Request, res: Response) => {
  res.json({ status: 'ok', message: '奥斯卡获奖数据 RAG AI Bot服务器运行正常' });
});

// 启动服务器
console.log('正在启动服务器...');
app.listen(PORT, () => {
  console.log(`奥斯卡获奖数据 RAG AI Bot服务器已启动，端口：${PORT}`);
  console.log(`访问地址：http://localhost:${PORT}`);
  console.log(`健康检查地址：http://localhost:${PORT}/health`);
});