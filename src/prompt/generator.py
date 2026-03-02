"""
Prompt Generator - Generates video prompts from hot topics
"""
import json
import random
from typing import Optional, List
import logging

from .client import get_llm_client, LLMClient
from .config import llm_config
from .models import GeneratedPrompt, TemplateType
from .templates import format_template

logger = logging.getLogger(__name__)


class PromptGenerator:
    """Generate video prompts from hot topics"""
    
    # Template type weights
    TEMPLATE_WEIGHTS = {
        TemplateType.HOT_INTERPRET: 0.6,
        TemplateType.KNOWLEDGE: 0.25,
        TemplateType.ROUNDUP: 0.15,
    }
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        """Initialize prompt generator"""
        self.llm_client = llm_client
    
    def _get_llm_client(self) -> LLMClient:
        """Get or create LLM client"""
        if self.llm_client is None:
            self.llm_client = get_llm_client()
        return self.llm_client
    
    def _select_template_type(self) -> TemplateType:
        """Select template type based on weights"""
        rand = random.random()
        cumulative = 0
        
        for template_type, weight in self.TEMPLATE_WEIGHTS.items():
            cumulative += weight
            if rand <= cumulative:
                return template_type
        
        return TemplateType.HOT_INTERPRET  # Default
    
    def _parse_llm_response(self, response: str) -> dict:
        """Parse LLM response to extract JSON"""
        # Try to find JSON in response
        response = response.strip()
        
        # Handle markdown code blocks
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0]
        elif "```" in response:
            response = response.split("```")[1].split("```")[0]
        
        # Try to parse JSON
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Try to find JSON-like content
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        
        raise ValueError(f"Failed to parse LLM response as JSON: {response[:200]}")
    
    def generate(
        self,
        topic,
        template_type: Optional[TemplateType] = None,
        temperature: Optional[float] = None,
    ) -> GeneratedPrompt:
        """Generate prompt from hot topic
        
        Args:
            topic: HotTopic object
            template_type: Optional template type (auto-selected if not provided)
            temperature: Optional temperature override
            
        Returns:
            GeneratedPrompt object
        """
        # Auto-select template type if not provided
        if template_type is None:
            template_type = self._select_template_type()
        
        logger.info(f"Generating prompt with template: {template_type.value}")
        
        # Prepare topic data
        topic_data = {
            "title": topic.title,
            "desc": topic.desc or "无",
            "author": topic.author or "未知",
            "view": topic.view,
            "like": topic.like,
            "coin": topic.coin,
            "favorite": topic.favorite,
            "share": topic.share,
        }
        
        # Format prompt
        prompt = format_template(template_type, topic_data)
        
        # Call LLM
        client = self._get_llm_client()
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        response = client.chat_completion(
            messages=messages,
            temperature=temperature,
        )
        
        # Parse response
        data = self._parse_llm_response(response)
        
        # Validate and create result
        data["template_type"] = template_type
        data["source_bvid"] = topic.bvid
        data["source_title"] = topic.title
        
        # Calculate quality score
        data["quality_score"] = self._calculate_quality_score(data)
        
        return GeneratedPrompt(**data)
    
    def _calculate_quality_score(self, data: dict) -> float:
        """Calculate basic quality score (0-1)"""
        score = 0.0
        
        # Check title suggestions (3 required)
        titles = data.get("title_suggestions", [])
        if len(titles) == 3:
            score += 0.2
        
        # Check core viewpoints (3-5 required)
        viewpoints = data.get("core_viewpoints", [])
        if 3 <= len(viewpoints) <= 5:
            score += 0.2
        
        # Check all required fields exist
        required_fields = ["opening", "body", "ending", "ending_interaction", "estimated_duration"]
        existing_fields = sum(1 for f in required_fields if data.get(f))
        score += (existing_fields / len(required_fields)) * 0.4
        
        # Check duration is reasonable
        duration = data.get("estimated_duration", 0)
        if 30 <= duration <= 600:
            score += 0.2
        
        return min(score, 1.0)
    
    def generate_all_types(
        self,
        topic,
        temperature: Optional[float] = None,
    ) -> List[GeneratedPrompt]:
        """Generate prompts for all template types
        
        Useful for testing or selecting best result
        """
        results = []
        for template_type in TemplateType:
            try:
                prompt = self.generate(topic, template_type, temperature)
                results.append(prompt)
            except Exception as e:
                logger.error(f"Failed to generate {template_type.value}: {e}")
        
        return results


# Convenience function
def generate_prompt(topic, template_type: Optional[TemplateType] = None) -> GeneratedPrompt:
    """Generate prompt from hot topic"""
    generator = PromptGenerator()
    return generator.generate(topic, template_type)
