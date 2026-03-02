"""
LLM Configuration for Prompt Generation
"""
import os
from typing import Optional
from pydantic import BaseModel


class LLMConfig(BaseModel):
    """LLM API Configuration"""
    # Provider: deepseek or anthropic
    provider: str = os.getenv("LLM_PROVIDER", "deepseek")
    
    # DeepSeek
    deepseek_api_key: str = os.getenv("DEEPSEEK_API_KEY", "")
    deepseek_base_url: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    deepseek_model: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    
    # Anthropic (backup)
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    anthropic_model: str = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
    
    # Common settings
    temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "2000"))
    
    # Timeout
    timeout: int = int(os.getenv("LLM_TIMEOUT", "60"))
    
    class Config:
        extra = "allow"


# Global config instance
llm_config = LLMConfig()
