"""
Prompt Templates for different video types
"""
from typing import Dict, Any
from .models import TemplateType


# Template prompts for LLM
TEMPLATES: Dict[TemplateType, str] = {
    TemplateType.HOT_INTERPRET: """你是一个专业的B站视频策划专家。请根据以下热点话题，生成一个视频Prompt。

## 热点话题信息
- 标题: {title}
- 描述: {desc}
- 作者: {author}
- 播放量: {view}
- 点赞: {like}
- 投币: {coin}
- 收藏: {favorite}
- 分享: {share}

## 任务要求
请生成一个"热点解读"类型的视频脚本，类型权重为60%。

### 要求：
1. 标题建议（3个）：简洁吸睛，能引发好奇
2. 核心观点（3-5个）：深度解读事件背后的原因和影响
3. 视频结构：
   - 开头（5-10秒）：hook观众，说明为什么这个话题值得关注
   - 主体（1-3分钟）：深度分析，层层递进
   - 结尾（10-20秒）：总结观点，引发思考
4. 结尾互动话术：引导评论、点赞、投币
5. 预估时长：60-180秒

请以JSON格式输出，包含以下字段：
{{
    "title_suggestions": ["标题1", "标题2", "标题3"],
    "core_viewpoints": ["观点1", "观点2", "观点3", "观点4"],
    "opening": "开头脚本",
    "body": "主体脚本",
    "ending": "结尾脚本",
    "ending_interaction": "互动话术",
    "estimated_duration": 120
}}

请确保输出是合法的JSON格式。""",

    TemplateType.KNOWLEDGE: """你是一个专业的B站视频策划专家。请根据以下热点话题，生成一个知识科普类视频Prompt。

## 热点话题信息
- 标题: {title}
- 描述: {desc}
- 作者: {author}
- 播放量: {view}
- 点赞: {like}
- 投币: {coin}
- 收藏: {favorite}
- 分享: {share}

## 任务要求
请生成一个"知识科普"类型的视频脚本，类型权重为25%。

### 要求：
1. 标题建议（3个）：能引发学习兴趣
2. 核心观点（3-5个）：围绕话题延伸出的知识点
3. 视频结构：
   - 开头（5-10秒）：引入话题，说明能学到什么
   - 主体（2-4分钟）：知识讲解，循序渐进
   - 结尾（10-20秒）：总结要点
4. 结尾互动话术：引导收藏、学习
5. 预估时长：120-240秒

请以JSON格式输出，包含以下字段：
{{
    "title_suggestions": ["标题1", "标题2", "标题3"],
    "core_viewpoints": ["观点1", "观点2", "观点3", "观点4"],
    "opening": "开头脚本",
    "body": "主体脚本",
    "ending": "结尾脚本",
    "ending_interaction": "互动话术",
    "estimated_duration": 180
}}

请确保输出是合法的JSON格式。""",

    TemplateType.ROUNDUP: """你是一个专业的B站视频策划专家。请根据以下热点话题，生成一个热点盘点类视频Prompt。

## 热点话题信息
- 标题: {title}
- 描述: {desc}
- 作者: {author}
- 播放量: {view}
- 点赞: {like}
- 投币: {coin}
- 收藏: {favorite}
- 分享: {share}

## 任务要求
请生成一个"热点盘点"类型的视频脚本，类型权重为15%。

### 要求：
1. 标题建议（3个）：盘点类标题，有吸引力
2. 核心观点（3-5个）：话题的关键要点或相关延伸
3. 视频结构：
   - 开头（5秒）：快速切入主题
   - 主体（1-2分钟）：要点罗列，简洁有力
   - 结尾（10秒）：话题延伸
4. 结尾互动话术：引导讨论
5. 预估时长：60-120秒

请以JSON格式输出，包含以下字段：
{{
    "title_suggestions": ["标题1", "标题2", "标题3"],
    "core_viewpoints": ["观点1", "观点2", "观点3", "观点4"],
    "opening": "开头脚本",
    "body": "主体脚本",
    "ending": "结尾脚本",
    "ending_interaction": "互动话术",
    "estimated_duration": 90
}}

请确保输出是合法的JSON格式。"""
}


def get_template(template_type: TemplateType) -> str:
    """Get prompt template by type"""
    return TEMPLATES.get(template_type, "")


def format_template(template_type: TemplateType, topic_data: Dict[str, Any]) -> str:
    """Format template with topic data"""
    template = get_template(template_type)
    return template.format(**topic_data)
