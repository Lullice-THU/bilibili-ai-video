"""
LLM API Client - DeepSeek and Anthropic support
"""
import json
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
import httpx
from .config import llm_config


class LLMClient(ABC):
    """Abstract base class for LLM clients"""
    
    @abstractmethod
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate chat completion"""
        pass


class DeepSeekClient(LLMClient):
    """DeepSeek API client"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.deepseek.com",
        model: str = "deepseek-chat",
    ):
        self.api_key = api_key or llm_config.deepseek_api_key
        self.base_url = base_url
        self.model = model
        self.timeout = llm_config.timeout
        
        if not self.api_key:
            raise ValueError("DeepSeek API key is required")
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate chat completion using DeepSeek API"""
        url = f"{self.base_url}/v1/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature or llm_config.temperature,
            "max_tokens": max_tokens or llm_config.max_tokens,
        }
        
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            return data["choices"][0]["message"]["content"]


class AnthropicClient(LLMClient):
    """Anthropic API client (Claude)"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-3-5-sonnet-20241022",
    ):
        self.api_key = api_key or llm_config.anthropic_api_key
        self.model = model
        self.timeout = llm_config.timeout
        
        if not self.api_key:
            raise ValueError("Anthropic API key is required")
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate chat completion using Anthropic API"""
        url = "https://api.anthropic.com/v1/messages"
        
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
        }
        
        # Convert messages format for Anthropic
        system_message = ""
        anthropic_messages = []
        
        for msg in messages:
            if msg.get("role") == "system":
                system_message = msg.get("content", "")
            else:
                anthropic_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        payload = {
            "model": self.model,
            "messages": anthropic_messages,
            "max_tokens": max_tokens or llm_config.max_tokens,
            "temperature": temperature or llm_config.temperature,
        }
        
        if system_message:
            payload["system"] = system_message
        
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            return data["content"][0]["text"]


def get_llm_client(provider: Optional[str] = None) -> LLMClient:
    """Get LLM client based on configuration"""
    provider = provider or llm_config.provider
    
    if provider == "deepseek":
        return DeepSeekClient()
    elif provider == "anthropic":
        return AnthropicClient()
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
