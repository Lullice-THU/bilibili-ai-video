"""
Prompt Generation Module

This module provides:
- LLM client support (DeepSeek, Anthropic)
- Prompt generation from hot topics
- Multiple template types (HOT_INTERPRET, KNOWLEDGE, ROUNDUP)
- Quality scoring
"""
from .client import get_llm_client, LLMClient, DeepSeekClient, AnthropicClient
from .config import llm_config, LLMConfig
from .generator import PromptGenerator, generate_prompt
from .models import GeneratedPrompt, TemplateType
from .templates import get_template, format_template

__all__ = [
    # Client
    "get_llm_client",
    "LLMClient",
    "DeepSeekClient",
    "AnthropicClient",
    # Config
    "llm_config",
    "LLMConfig",
    # Generator
    "PromptGenerator",
    "generate_prompt",
    # Models
    "GeneratedPrompt",
    "TemplateType",
    # Templates
    "get_template",
    "format_template",
]
