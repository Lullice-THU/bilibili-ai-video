"""
Prompt Generation Configuration
"""
import os
from typing import Optional
from pydantic import BaseModel


class HenryConfig(BaseModel):
    """Henry API Configuration"""
    # Henry API endpoint
    api_url: str = os.getenv("HENRY_API_URL", "http://localhost:5000/api/henry/generate")
    
    # API timeout in seconds
    timeout: int = int(os.getenv("HENRY_API_TIMEOUT", "120"))
    
    class Config:
        extra = "allow"


# Global config instance
henry_config = HenryConfig()


# Legacy alias (for backwards compatibility)
class LLMConfig(BaseModel):
    """Legacy LLM Config - Deprecated"""
    provider: str = "henry"
    timeout: int = 120
    
    class Config:
        extra = "allow"

llm_config = LLMConfig()
