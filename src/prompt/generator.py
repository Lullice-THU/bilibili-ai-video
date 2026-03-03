"""
Prompt Generator - Generates video prompts from hot topics using Henry agent
"""
import json
import random
from typing import Optional, List
import logging

from .henry_client import HenryClient, generate_prompt_with_henry
from .models import GeneratedPrompt, TemplateType
from .templates import format_template

logger = logging.getLogger(__name__)


class PromptGenerator:
    """Generate video prompts from hot topics using Henry agent"""
    
    # Template type weights
    TEMPLATE_WEIGHTS = {
        TemplateType.HOT_INTERPRET: 0.6,
        TemplateType.KNOWLEDGE: 0.25,
        TemplateType.ROUNDUP: 0.15,
    }
    
    def __init__(self, henry_client: Optional[HenryClient] = None):
        """Initialize prompt generator"""
        self.henry_client = henry_client
    
    def _get_henry_client(self) -> HenryClient:
        """Get or create Henry client"""
        if self.henry_client is None:
            self.henry_client = HenryClient()
        return self.henry_client
    
    def _select_template_type(self) -> TemplateType:
        """Select template type based on weights"""
        rand = random.random()
        cumulative = 0
        
        for template_type, weight in self.TEMPLATE_WEIGHTS.items():
            cumulative += weight
            if rand <= cumulative:
                return template_type
        
        return TemplateType.HOT_INTERPRET  # Default
    
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
            temperature: Optional temperature override (not used with Henry)
            
        Returns:
            GeneratedPrompt object
        """
        # Auto-select template type if not provided
        if template_type is None:
            template_type = self._select_template_type()
        
        logger.info(f"Generating prompt with template: {template_type.value}")
        
        # Call Henry client to generate prompt
        client = self._get_henry_client()
        
        result = client.generate_prompt(
            topic_title=topic.title,
            topic_desc=topic.desc or "",
        )
        
        # Validate and create result
        result["template_type"] = template_type
        result["source_bvid"] = topic.bvid
        result["source_title"] = topic.title
        
        # Calculate quality score
        result["quality_score"] = self._calculate_quality_score(result)
        
        return GeneratedPrompt(**result)
    
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
