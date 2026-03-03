"""
Henry Client - Generate prompts via Henry agent API

This module provides functionality to call the Henry agent (main session)
to generate AI video prompts based on Bilibili hot topics.
"""
import json
import logging
import os
from typing import Optional, Dict, Any, List

import httpx

logger = logging.getLogger(__name__)


# Henry API configuration
HENRY_API_URL = os.getenv("HENRY_API_URL", "http://localhost:5000/api/henry/generate")
HENRY_API_TIMEOUT = int(os.getenv("HENRY_API_TIMEOUT", "120"))


class HenryClient:
    """Client for calling Henry agent to generate prompts"""
    
    def __init__(self, api_url: Optional[str] = None, timeout: int = HENRY_API_TIMEOUT):
        self.api_url = api_url or HENRY_API_URL
        self.timeout = timeout
    
    def generate_prompt(
        self,
        topic_title: str,
        topic_desc: str,
    ) -> Dict[str, Any]:
        """
        Call Henry agent to generate a video prompt.
        
        Args:
            topic_title: The hot topic title
            topic_desc: The hot topic description
            
        Returns:
            Dictionary containing generated prompt data
        """
        # Build the prompt for Henry
        henry_prompt = self._build_henry_prompt(topic_title, topic_desc)
        
        logger.info(f"Calling Henry to generate prompt for: {topic_title}")
        
        try:
            # Call Henry API
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    self.api_url,
                    json={
                        "prompt": henry_prompt,
                        "topic_title": topic_title,
                        "topic_desc": topic_desc,
                    }
                )
                
                if response.status_code != 200:
                    raise Exception(f"Henry API error: {response.status_code} - {response.text}")
                
                result = response.json()
                logger.info(f"Successfully generated prompt for: {topic_title}")
                return result
                
        except httpx.ConnectError:
            logger.warning(f"Cannot connect to Henry API at {self.api_url}, using fallback")
            return self._generate_fallback_prompt(topic_title, topic_desc)
        except Exception as e:
            logger.error(f"Error calling Henry API: {e}")
            return self._generate_fallback_prompt(topic_title, topic_desc)
    
    def _build_henry_prompt(self, topic_title: str, topic_desc: str) -> str:
        """
        Build the prompt for Henry agent.
        
        This instructs Henry to generate an AI video script/prompt based on
        the Bilibili hot topic.
        """
        return f"""请根据以下B站热点话题，生成一个适合AI视频生成的脚本/分镜prompt。

热点标题: {topic_title}
热点描述: {topic_desc}

请生成：
1. 视频开头（吸引眼球的说法，5-10秒）
2. 核心内容（3-5个要点）
3. 视频结尾（总结+互动话术）
4. 预估时长

要求：
- 适合AI生成（如 Runway、Pika、Leonardo AI 等）
- 语言口语化，有爆款潜力
- 输出格式为 Markdown

请直接输出生成的prompt内容，不要有额外的解释。"""
    
    def _generate_fallback_prompt(
        self,
        topic_title: str,
        topic_desc: str,
    ) -> Dict[str, Any]:
        """
        Generate a fallback prompt when Henry API is not available.
        
        This provides a basic prompt structure that can be used as fallback.
        """
        logger.info(f"Using fallback prompt generation for: {topic_title}")
        
        return {
            "title_suggestions": [
                f"深度解析: {topic_title[:20]}",
                f"原来这就是{topic_title[:15]}的真相",
                f"{topic_title[:15]}，看完你就懂了"
            ],
            "core_viewpoints": [
                f"{topic_title}引发了广泛讨论",
                "该话题在社交媒体上热度很高",
                "值得我们深入分析和思考"
            ],
            "opening": f"各位观众朋友们大家好，今天我们来聊聊{topic_title}这个话题...",
            "body": f"最近{topic_title}成为了热点中的热点。{topic_desc or '这个话题引起了广泛关注。'}让我们一起来深入分析一下这背后的原因和影响。",
            "ending": f"以上就是关于{topic_title}的深度分析，感谢大家的观看。",
            "ending_interaction": "如果你对这个话题有什么看法，欢迎在评论区留言讨论。记得点赞投币支持一下！",
            "estimated_duration": 120,
        }


def generate_prompt_with_henry(topic_title: str, topic_desc: str) -> Dict[str, Any]:
    """
    Convenience function to generate prompt via Henry.
    
    Args:
        topic_title: The hot topic title
        topic_desc: The hot topic description
        
    Returns:
        Dictionary containing generated prompt data
    """
    client = HenryClient()
    return client.generate_prompt(topic_title, topic_desc)
