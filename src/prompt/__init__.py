"""
Prompt Generation Module

This module provides:
- Henry client for calling main agent to generate prompts
- Prompt generation from hot topics
- Multiple template types (HOT_INTERPRET, KNOWLEDGE, ROUNDUP)
- Quality scoring
"""
from .generator import PromptGenerator, generate_prompt
from .henry_client import HenryClient, generate_prompt_with_henry
from .models import GeneratedPrompt, TemplateType
from .templates import get_template, format_template

__all__ = [
    # Henry Client
    "HenryClient",
    "generate_prompt_with_henry",
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
