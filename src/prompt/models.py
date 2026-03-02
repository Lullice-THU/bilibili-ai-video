"""
Prompt Generation Data Models
"""
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class TemplateType(str, Enum):
    """Prompt template types"""
    HOT_INTERPRET = "hot_interpret"  # 热点解读 (60%)
    KNOWLEDGE = "knowledge"          # 知识科普 (25%)
    ROUNDUP = "roundup"              # 热点盘点 (15%)


class GeneratedPrompt(BaseModel):
    """Generated prompt for AI video generation"""
    # Template type used
    template_type: TemplateType = Field(..., description="Template type")
    
    # Title suggestions (3)
    title_suggestions: List[str] = Field(
        ...,
        description="Title suggestions (3)",
        min_length=3,
        max_length=3
    )
    
    # Core viewpoints (3-5)
    core_viewpoints: List[str] = Field(
        ...,
        description="Core viewpoints (3-5)",
        min_length=3,
        max_length=5
    )
    
    # Video structure
    opening: str = Field(..., description="Opening hook script")
    body: str = Field( ..., description="Main content script")
    ending: str = Field(..., description="Ending script")
    
    # Interaction
    ending_interaction: str = Field(
        ...,
        description="Ending interaction call-to-action"
    )
    
    # Duration estimate (in seconds)
    estimated_duration: int = Field(
        ...,
        description="Estimated video duration in seconds",
        ge=30,
        le=600
    )
    
    # Source topic (for reference)
    source_bvid: Optional[str] = Field(None, description="Source video BV号")
    source_title: Optional[str] = Field(None, description="Source video title")
    
    # Quality score (optional)
    quality_score: Optional[float] = Field(
        None,
        description="Quality score (0-1)",
        ge=0,
        le=1
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "template_type": "hot_interpret",
                "title_suggestions": [
                    "震惊！XX事件背后的真相",
                    "深度解析XX热点事件",
                    "XX爆火背后，普通人能学到什么"
                ],
                "core_viewpoints": [
                    "观点1: xxx",
                    "观点2: xxx",
                    "观点3: xxx"
                ],
                "opening": "开场白...",
                "body": "主体内容...",
                "ending": "结尾总结...",
                "ending_interaction": "欢迎大家在评论区留言...",
                "estimated_duration": 180
            }
        }
