"""
Bilibili AI Video MVP - Backend API
使用子Agent模式调用LLM生成文案
"""
import os
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import httpx

# 加载环境变量
load_dotenv()

app = FastAPI(title="Bilibili AI Video API", version="1.0.0")


# ==================== 配置 ====================
class Config:
    """LLM 配置"""
    # LLM 提供商: openai | minimax | mock
    PROVIDER = os.getenv("LLM_PROVIDER", "mock").lower()
    
    # OpenAI 配置
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # MiniMax 配置
    MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "")
    MINIMAX_BASE_URL = os.getenv("MINIMAX_BASE_URL", "https://api.minimax.chat/v1")
    MINIMAX_MODEL = os.getenv("MINIMAX_MODEL", "abab6.5s-chat")
    
    # 是否启用模拟模式
    MOCK_MODE = PROVIDER == "mock" or not (OPENAI_API_KEY or MINIMAX_API_KEY)


config = Config()


# ==================== LLM 客户端 ====================
class LLMClient:
    """LLM 客户端基类"""
    
    async def generate(self, material: str, video_type: str) -> tuple[str, str]:
        """生成标题和文案"""
        raise NotImplementedError


class OpenAIClient(LLMClient):
    """OpenAI 客户端"""
    
    def __init__(self, api_key: str, base_url: str, model: str):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
    
    async def generate(self, material: str, video_type: str) -> tuple[str, str]:
        prompt = self._build_prompt(material, video_type)
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "你是一个专业的B站视频文案生成助手，擅长生成吸引人的标题和脚本。"},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.8,
                    "max_tokens": 2000
                }
            )
            
            if response.status_code != 200:
                raise Exception(f"OpenAI API error: {response.text}")
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            return self._parse_response(content)
    
    def _build_prompt(self, material: str, video_type: str) -> str:
        return f"""请根据以下素材生成一个B站视频的标题和文案。

素材内容：
{material}

视频类型：{video_type}

请按以下JSON格式返回（只需要返回JSON，不要其他内容）：
{{
    "title": "标题（20-30字，有吸引力）",
    "script": "文案内容（300-800字）"
}}
"""

    def _parse_response(self, content: str) -> tuple[str, str]:
        import json
        import re
        
        # 尝试提取 JSON
        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            try:
                data = json.loads(json_match.group())
                return data.get("title", ""), data.get("script", "")
            except:
                pass
        
        # 如果解析失败，尝试简单分割
        lines = content.split("\n")
        title = ""
        script = ""
        
        for i, line in enumerate(lines):
            if "标题" in line and ":" in line:
                title = line.split(":", 1)[1].strip()
            elif "文案" in line and ":" in line:
                script = "\n".join(lines[i+1:]).strip()
        
        return title or content[:50], script or content


class MiniMaxClient(LLMClient):
    """MiniMax 客户端"""
    
    def __init__(self, api_key: str, base_url: str, model: str):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
    
    async def generate(self, material: str, video_type: str) -> tuple[str, str]:
        prompt = self._build_prompt(material, video_type)
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/text/chatcompletion_v2",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "你是一个专业的B站视频文案生成助手，擅长生成吸引人的标题和脚本。"},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.8,
                    "max_tokens": 2000
                }
            )
            
            if response.status_code != 200:
                raise Exception(f"MiniMax API error: {response.text}")
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            return self._parse_response(content)
    
    def _build_prompt(self, material: str, video_type: str) -> str:
        return f"""请根据以下素材生成一个B站视频的标题和文案。

素材内容：
{material}

视频类型：{video_type}

请按以下JSON格式返回（只需要返回JSON，不要其他内容）：
{{
    "title": "标题（20-30字，有吸引力）",
    "script": "文案内容（300-800字）"
}}
"""

    def _parse_response(self, content: str) -> tuple[str, str]:
        import json
        import re
        
        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            try:
                data = json.loads(json_match.group())
                return data.get("title", ""), data.get("script", "")
            except:
                pass
        
        return content[:50], content


class MockClient(LLMClient):
    """模拟客户端 - 无API Key时使用"""
    
    async def generate(self, material: str, video_type: str) -> tuple[str, str]:
        # 模拟延迟
        import asyncio
        await asyncio.sleep(1)
        
        # 生成标题
        keywords = material[:20] if material else "热门"
        title = f"【必看】{keywords}的真相来了！"
        
        # 生成文案
        script = f"""各位小伙伴大家好！

今天给大家带来的是关于「{material[:50]}」的深度解析。

{('首先，让我们来看看这个话题的核心要点。' if video_type == 'general' else '作为一个专业的内容创作者，我来为大家详细分析。')}

{ material }

{('如果觉得有帮助，记得一键三连支持一下！' if video_type == 'general' else '以上就是本次分享的全部内容，感谢大家的观看。')}

我是你们的UP主，我们下期再见！

#bilibili #AI #干货分享"""
        
        return title, script


# ==================== 获取 LLM 客户端 ====================
def get_llm_client() -> LLMClient:
    """获取 LLM 客户端实例"""
    if config.MOCK_MODE:
        return MockClient()
    
    if config.PROVIDER == "openai":
        return OpenAIClient(
            api_key=config.OPENAI_API_KEY,
            base_url=config.OPENAI_BASE_URL,
            model=config.OPENAI_MODEL
        )
    elif config.PROVIDER == "minimax":
        return MiniMaxClient(
            api_key=config.MINIMAX_API_KEY,
            base_url=config.MINIMAX_BASE_URL,
            model=config.MINIMAX_MODEL
        )
    else:
        return MockClient()


# ==================== API 模型 ====================
class GenerateRequest(BaseModel):
    """生成文案请求"""
    material: str  # 素材内容
    video_type: Optional[str] = "general"  # 视频类型


class GenerateResponse(BaseModel):
    """生成文案响应"""
    title: str  # 生成的标题
    script: str  # 生成的文案
    success: bool
    error: Optional[str] = None
    mode: str  # 使用的模式: real | mock


class HenryGenerateRequest(BaseModel):
    """Henry 生成 Prompt 请求"""
    prompt: str  # 给 Henry 的指令
    topic_title: str  # 热点标题
    topic_desc: str  # 热点描述


class HenryGenerateResponse(BaseModel):
    """Henry 生成 Prompt 响应"""
    success: bool
    title_suggestions: list = []
    core_viewpoints: list = []
    opening: str = ""
    body: str = ""
    ending: str = ""
    ending_interaction: str = ""
    estimated_duration: int = 120
    error: Optional[str] = None


# ==================== API 路由 ====================
@app.get("/")
async def root():
    return {
        "message": "Bilibili AI Video API", 
        "status": "running",
        "mode": "mock" if config.MOCK_MODE else config.PROVIDER
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "mode": "mock" if config.MOCK_MODE else config.PROVIDER
    }


@app.get("/config")
async def get_config():
    """获取当前配置信息"""
    return {
        "provider": config.PROVIDER,
        "mock_mode": config.MOCK_MODE,
        "has_openai_key": bool(config.OPENAI_API_KEY),
        "has_minimax_key": bool(config.MINIMAX_API_KEY)
    }


@app.post("/api/generate", response_model=GenerateResponse)
async def generate_content(request: GenerateRequest):
    """
    生成文案 API
    输入素材，调用LLM生成标题和文案
    """
    if not request.material or len(request.material.strip()) < 10:
        raise HTTPException(status_code=400, detail="素材内容至少需要10个字符")
    
    try:
        # 获取 LLM 客户端
        client = get_llm_client()
        
        # 调用 LLM 生成
        title, script = await client.generate(request.material, request.video_type or "general")
        
        return GenerateResponse(
            title=title,
            script=script,
            success=True,
            mode="mock" if config.MOCK_MODE else config.PROVIDER
        )
    except Exception as e:
        return GenerateResponse(
            title="",
            script="",
            success=False,
            error=str(e),
            mode="mock" if config.MOCK_MODE else config.PROVIDER
        )


@app.post("/api/henry/generate", response_model=HenryGenerateResponse)
async def henry_generate(request: HenryGenerateRequest):
    """
    Henry 生成 Prompt API
    调用 Henry agent 生成 AI 视频脚本/prompt
    
    注意: 这个端点需要 Henry agent 运行在后台
    当前实现使用 mock 模式返回示例数据
    """
    import asyncio
    
    try:
        # 这里可以集成实际的 Henry agent 调用
        # 目前使用模拟实现，返回基于话题的示例数据
        
        await asyncio.sleep(0.5)  # 模拟延迟
        
        # 基于话题生成示例数据
        topic = request.topic_title
        desc = request.topic_desc or ""
        
        return HenryGenerateResponse(
            success=True,
            title_suggestions=[
                f"深度解析: {topic[:20]}",
                f"原来这就是{topic[:15]}的真相",
                f"{topic[:15]}，看完你就懂了"
            ],
            core_viewpoints=[
                f"{topic}引发了广泛讨论",
                "该话题在社交媒体上热度很高",
                "值得我们深入分析和思考"
            ],
            opening=f"各位观众朋友们大家好，今天我们来聊聊{topic}这个话题...",
            body=f"最近{topic}成为了热点中的热点。{desc}让我们一起来深入分析一下这背后的原因和影响。",
            ending=f"以上就是关于{topic}的深度分析，感谢大家的观看。",
            ending_interaction="如果你对这个话题有什么看法，欢迎在评论区留言讨论。记得点赞投币支持一下！",
            estimated_duration=120
        )
    except Exception as e:
        return HenryGenerateResponse(
            success=False,
            error=str(e)
        )


# ==================== 启动 ====================
if __name__ == "__main__":
    print(f"Starting Bilibili AI Video API...")
    print(f"LLM Provider: {config.PROVIDER}")
    print(f"Mock Mode: {config.MOCK_MODE}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
