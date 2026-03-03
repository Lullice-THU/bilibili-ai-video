# bilibili-ai-video

[![Stars](https://img.shields.io/github/stars/Lullice-THU/bilibili-ai-video?style=social)](https://github.com/Lullice-THU/bilibili-ai-video/stargazers)
# bilibili-ai-video
Bilibili AI Video Prompt Generator - 基于B站热点自动生成AI视频Prompt

## 项目简介

本项目从B站采集实时热点话题，计算热度分数，并自动生成AI视频创作的Prompt。支持手动触发和定时任务（每天08:00和20:00自动运行）。

## 项目结构

```
bilibili-ai-video/
├── config.py           # 配置文件
├── main.py            # 主程序入口
├── scheduler.py       # 定时任务模块
├── dashboard_app.py   # Dashboard服务
├── dashboard/         # 前端页面
├── src/
│   ├── collector/     # B站数据采集
│   ├── calculator/   # 热度计算引擎
│   ├── prompt/        # Prompt生成器
│   └── dashboard/     # Dashboard API
└── data/
    ├── prompts.json        # 生成的Prompt数据
    └── daily_prompts/      # 每日Prompt文件
```

## 快速开始

### 前置要求
- Python 3.8+
- 网络访问B站API

### 安装依赖
```bash
pip install httpx pydantic fastapi uvicorn
```

### 运行方式

#### 1. 立即生成Prompt
```bash
python main.py --run-now
```
生成完成后会：
- 在 `data/daily_prompts/YYYY-MM-DD-HH.md` 保存Markdown格式
- 在 `data/prompts.json` 保存JSON格式（供Dashboard使用）

#### 2. 启动定时任务（每天08:00和20:00自动运行）
```bash
python main.py --schedule
```

#### 3. 启动Dashboard
```bash
python dashboard_app.py
```
访问 http://localhost:5000 查看Prompt列表

### 使用真实的LLM API

设置环境变量：
```bash
# DeepSeek (默认)
export DEEPSEEK_API_KEY=your-api-key

# 或 Anthropic Claude
export LLM_PROVIDER=anthropic
export ANTHROPIC_API_KEY=your-api-key
```

## 输出格式

### Markdown文件 (data/daily_prompts/YYYY-MM-DD-HH.md)
```markdown
# Prompt - 2026-03-03 08:00

## 热点话题
1. 热点话题1...
2. 热点话题2...

## 生成 Prompt
### 话题 1: xxx
**类型**: hot_interpret

**标题建议:**
- 标题1
- 标题2
...

**开头:** 开场白内容
**主体:** 主体内容
**结尾:** 结尾内容
**互动话术:** 互动话术
**预估时长:** 120秒
```

### Dashboard API
- `GET /api/dashboard` - 获取所有数据
- `GET /api/prompts` - 获取Prompt列表
- `POST /api/generate` - 手动触发生成

## 功能说明

1. **数据采集** - 从B站API获取热门视频
2. **热度计算** - 根据播放、点赞、投币等计算热度分数
3. **Prompt生成** - 基于热点话题生成AI视频创作Prompt（支持DeepSeek/Anthropic）
4. **定时任务** - 每天08:00和20:00自动运行
5. **Dashboard** - Web界面查看生成的Prompt
