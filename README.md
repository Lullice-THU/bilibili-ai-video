# bilibili-ai-video
Bilibili AI Video Assistant - MVP

## 项目结构
```
bilibili-ai-video/
├── backend/           # FastAPI 后端
│   ├── main.py       # API 服务
│   ├── .env         # 环境配置
│   └── .env.example # 配置示例
└── frontend/         # Taro 前端 (H5/小程序)
```

## 快速启动

### 前置要求
- Python 3.8+
- Node.js 16+

### 后端启动
```bash
cd backend

# 安装依赖
pip install --break-system-packages fastapi uvicorn pydantic python-dotenv httpx

# 启动服务（默认 mock 模式，无需 API Key）
python main.py
```
服务地址: http://localhost:8000

### 前端启动
```bash
cd frontend
npm install
npm run dev
```

## 配置说明

### 环境变量 (.env)
在 `backend/.env` 中配置：

```bash
# LLM Provider: openai | minimax | mock
LLM_PROVIDER=mock

# OpenAI 配置（可选）
OPENAI_API_KEY=your-openai-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo

# MiniMax 配置（可选）
MINIMAX_API_KEY=your-minimax-api-key
MINIMAX_BASE_URL=https://api.minimax.chat/v1
MINIMAX_MODEL=abab6.5s-chat
```

### 使用真实 LLM
1. 申请 API Key（OpenAI 或 MiniMax）
2. 编辑 `backend/.env`，设置：
   - `LLM_PROVIDER=openai` 或 `LLM_PROVIDER=minimax`
   - 填入对应的 API Key
3. 重启后端服务

## API 接口

### 1. 健康检查
```bash
GET /
# 返回: {"message": "Bilibili AI Video API", "status": "running", "mode": "mock"}
```

### 2. 配置信息
```bash
GET /config
# 返回: {"provider": "mock", "mock_mode": true, ...}
```

### 3. 生成文案
```bash
POST /api/generate
Content-Type: application/json

{
  "material": "素材内容，至少10个字符",
  "video_type": "general"  // 或 "professional"
}

# 成功返回:
{
  "title": "生成的标题",
  "script": "生成的文案",
  "success": true,
  "mode": "mock"
}
```

## MVP 功能
- ✅ 素材输入 → AI 生成文案+标题 → 一键复制
- ✅ 支持 Mock 模式（无需 API Key）
- ✅ 支持 OpenAI API
- ✅ 支持 MiniMax API
- ✅ 前后端分离架构
- ✅ 加载状态和错误处理

## 开发说明

### 端口说明
- 后端: 8000
- 前端: 10086 (Taro 默认)

### 前端调用
前端通过 `http://localhost:8000` 调用后端 API。如需修改，编辑：
`frontend/src/pages/index/index.tsx` 中的 `API_BASE` 常量。

## 常见问题

### Q: 启动失败提示端口占用
```bash
# 查找占用进程
lsof -i :8000
# 杀掉进程
kill -9 <PID>
```

### Q: 如何使用真实 LLM？
确保 `.env` 中 `LLM_PROVIDER` 设置为 `openai` 或 `minimax`，并填入有效的 API Key。
