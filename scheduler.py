"""
Scheduled Task - Generate Prompts Daily
"""
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from config import DATA_DIR, DAILY_PROMPTS_DIR, SCHEDULED_HOURS
from src.collector.bilibili import get_bilibili_collector
from src.collector.models import HotTopic
from src.calculator.engine import get_default_calculator
from src.prompt.generator import PromptGenerator
from src.prompt.models import TemplateType

logger = logging.getLogger(__name__)


class ScheduledPromptGenerator:
    """Scheduled prompt generation task"""
    
    def __init__(self, topics_count: int = 10):
        self.topics_count = topics_count
        self.collector = get_bilibili_collector()
        self.calculator = get_default_calculator()
        self.generator = PromptGenerator()
    
    def run(self) -> dict:
        """Run the scheduled task to generate prompts"""
        logger.info("=" * 50)
        logger.info("Starting scheduled prompt generation...")
        
        now = datetime.now()
        timestamp_str = now.strftime("%Y-%m-%d %H:%M")
        filename = now.strftime("%Y-%m-%d-%H") + ".md"
        
        # Step 1: Collect hot topics
        logger.info("Step 1: Collecting hot topics from Bilibili...")
        topics = self.collector.collect_topics(limit=self.topics_count)
        
        if not topics:
            logger.warning("No topics collected, using fallback")
            topics = self._get_fallback_topics()
        
        # Step 2: Calculate heat scores
        logger.info("Step 2: Calculating heat scores...")
        ranked_topics = self.calculator.get_top_topics(topics, n=self.topics_count)
        
        # Display top topics
        logger.info("Top 5 hot topics:")
        for i, topic in enumerate(ranked_topics[:5]):
            logger.info(f"  {i+1}. {topic.title} (score: {topic.hot_score})")
        
        # Step 3: Generate prompts for top topics
        logger.info("Step 3: Generating prompts...")
        prompts = []
        
        for topic in ranked_topics[:5]:  # Generate for top 5 topics
            try:
                prompt = self.generator.generate(topic)
                prompts.append({
                    "topic": topic.title,
                    "prompt": prompt,
                    "template_type": prompt.template_type.value,
                })
                logger.info(f"  Generated prompt for: {topic.title}")
            except Exception as e:
                logger.error(f"  Failed to generate prompt for {topic.title}: {e}")
                # Try fallback prompt generation
                try:
                    mock_prompt = self._generate_mock_prompt(topic)
                    prompts.append({
                        "topic": topic.title,
                        "prompt": mock_prompt,
                        "template_type": "hot_interpret",
                    })
                    logger.info(f"  Generated mock prompt for: {topic.title}")
                except Exception as e2:
                    logger.error(f"  Also failed to generate mock prompt: {e2}")
        
        # Step 4: Save to file
        logger.info("Step 4: Saving prompts to file...")
        output_file = DAILY_PROMPTS_DIR / filename
        content = self._format_output(timestamp_str, ranked_topics, prompts)
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        
        logger.info(f"Prompts saved to: {output_file}")
        
        # Also save to prompts.json for dashboard
        self._save_prompts_json(prompts)
        
        # Cleanup
        self.collector.close()
        
        result = {
            "timestamp": timestamp_str,
            "topics_count": len(ranked_topics),
            "prompts_count": len(prompts),
            "output_file": str(output_file),
        }
        
        logger.info(f"Scheduled task completed: {result}")
        logger.info("=" * 50)
        
        return result
    
    def _generate_mock_prompt(self, topic: HotTopic):
        """Generate a mock prompt when LLM API is not available"""
        from src.prompt.models import GeneratedPrompt
        
        titles = [
            f"深度解析: {topic.title[:20]}",
            f"原来这就是{topic.title[:15]}的真相",
            f"{topic.title[:15]}，看完你就懂了"
        ]
        
        viewpoints = [
            f"观点1: {topic.title}引发了广泛讨论",
            f"观点2: 该话题在社交媒体上热度很高",
            f"观点3: 值得我们深入分析和思考"
        ]
        
        return GeneratedPrompt(
            template_type=TemplateType.HOT_INTERPRET,
            title_suggestions=titles,
            core_viewpoints=viewpoints,
            opening=f"各位观众朋友们大家好，今天我们来聊聊{topic.title}这个话题...",
            body=f"最近{topic.title}成为了热点中的热点。{topic.desc or '这个话题引起了广泛关注。'}让我们一起来深入分析一下这背后的原因和影响。\n\n首先，从数据角度来看，这个话题的播放量非常高，说明大家对这个内容非常感兴趣。\n\n其次，我们需要思考为什么这个话题会火起来？这反映了什么样的社会现象和用户心理？\n\n最后，这个话题对普通人有什么启示？我们又能从中学习到什么？",
            ending=f"以上就是关于{topic.title}的深度分析，感谢大家的观看。",
            ending_interaction="如果你对这个话题有什么看法，欢迎在评论区留言讨论。记得点赞投币支持一下！",
            estimated_duration=120,
            source_bvid=topic.bvid,
            source_title=topic.title,
            quality_score=0.7,
        )
    
    def _get_fallback_topics(self) -> List[HotTopic]:
        """Get fallback topics when API fails"""
        fallback_data = [
            {"title": "AI人工智能最新发展", "view": 1250000, "like": 85000, "coin": 25000, "favorite": 45000, "share": 12000, "reply": 5200},
            {"title": "B站热门视频合集", "view": 980000, "like": 72000, "coin": 18000, "favorite": 38000, "share": 9500, "reply": 4100},
            {"title": "Steam游戏推荐", "view": 850000, "like": 65000, "coin": 15000, "favorite": 32000, "share": 8000, "reply": 3800},
            {"title": "科技数码测评", "view": 720000, "like": 55000, "coin": 12000, "favorite": 28000, "share": 6500, "reply": 3200},
            {"title": "生活实用技巧", "view": 680000, "like": 48000, "coin": 10000, "favorite": 25000, "share": 5500, "reply": 2800},
        ]
        
        topics = []
        for i, data in enumerate(fallback_data):
            topic = HotTopic(
                bvid=f"BVfallback{i+1}",
                title=data["title"],
                desc="",
                author="",
                view=data["view"],
                like=data["like"],
                coin=data["coin"],
                favorite=data["favorite"],
                share=data["share"],
                reply=data["reply"],
                pubdate=int(datetime.now().timestamp()),
                duration="",
                pic="",
                rank=i+1,
            )
            topics.append(topic)
        
        return topics
    
    def _format_output(self, timestamp: str, topics, prompts: List[dict]) -> str:
        """Format output in simplified markdown"""
        lines = [
            f"# Prompt - {timestamp}",
            "",
            "## 热点话题",
            ""
        ]

        for i, topic in enumerate(topics[:10]):
            lines.append(f"{i+1}. {topic.title}")

        lines.extend(["", "## 生成 Prompt", ""])

        for i, item in enumerate(prompts):
            prompt = item["prompt"]
            lines.extend([
                f"### {i+1}. {item['topic']}",
                f"**类型**: {item['template_type']}",
                "",
                "**标题建议**",
                *[f"- {title}" for title in prompt.title_suggestions],
                "",
                "**脚本**",
                f"**开头**: {prompt.opening}",
                "",
                f"**主体**: {prompt.body[:300]}..." if len(prompt.body) > 300 else f"**主体**: {prompt.body}",
                "",
                f"**结尾**: {prompt.ending}",
                "",
                f"**互动**: {prompt.ending_interaction}",
                "",
                f"**时长**: ~{prompt.estimated_duration}秒",
                "",
                "---",
                ""
            ])

        return "\n".join(lines)
    
    def _save_prompts_json(self, prompts: List[dict]):
        """Save prompts to JSON for dashboard"""
        prompts_file = DATA_DIR / "prompts.json"
        
        data = []
        for item in prompts:
            prompt = item["prompt"]
            data.append({
                "topic": item["topic"],
                "template_type": item["template_type"],
                "title": prompt.title_suggestions[0] if prompt.title_suggestions else "",
                "quality_score": prompt.quality_score,
                "created_at": datetime.now().isoformat(),
                "opening": prompt.opening,
                "body": prompt.body,
                "ending": prompt.ending,
                "ending_interaction": prompt.ending_interaction,
                "estimated_duration": prompt.estimated_duration,
            })
        
        with open(prompts_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def run_scheduled_task():
    """Run the scheduled task"""
    generator = ScheduledPromptGenerator()
    return generator.run()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    run_scheduled_task()
