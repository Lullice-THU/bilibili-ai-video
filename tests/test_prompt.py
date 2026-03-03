"""
Unit tests for Prompt Generation Module (Henry-based)
"""
import pytest
import json
from unittest.mock import Mock, patch

from src.prompt import (
    PromptGenerator,
    generate_prompt,
    GeneratedPrompt,
    TemplateType,
    HenryClient,
    generate_prompt_with_henry,
)


class TestHenryConfig:
    """Test Henry configuration"""
    
    def test_default_config(self):
        """Test default configuration values"""
        client = HenryClient()
        assert client.api_url is not None
        assert client.timeout == 120


class TestTemplateTypes:
    """Test template type enum"""
    
    def test_template_types_exist(self):
        """Verify all template types exist"""
        assert TemplateType.HOT_INTERPRET.value == "hot_interpret"
        assert TemplateType.KNOWLEDGE.value == "knowledge"
        assert TemplateType.ROUNDUP.value == "roundup"


class TestPromptGenerator:
    """Test prompt generator"""
    
    def test_generator_init(self):
        """Test generator initialization"""
        generator = PromptGenerator()
        assert generator.henry_client is None
    
    def test_generator_with_client(self):
        """Test generator with custom client"""
        mock_client = Mock()
        generator = PromptGenerator(henry_client=mock_client)
        assert generator.henry_client is mock_client
    
    def test_template_type_selection(self):
        """Test template type selection based on weights"""
        generator = PromptGenerator()
        
        # Run multiple times to verify distribution
        counts = {t: 0 for t in TemplateType}
        iterations = 1000
        
        for _ in range(iterations):
            template_type = generator._select_template_type()
            counts[template_type] += 1
        
        # Verify distribution is roughly correct (within 20% margin)
        assert counts[TemplateType.HOT_INTERPRET] / iterations > 0.4
        assert counts[TemplateType.KNOWLEDGE] / iterations > 0.15
        assert counts[TemplateType.ROUNDUP] / iterations > 0.05
    
    def test_quality_score_calculation(self):
        """Test quality score calculation"""
        generator = PromptGenerator()
        
        # Perfect score
        data = {
            "title_suggestions": ["a", "b", "c"],
            "core_viewpoints": ["1", "2", "3"],
            "opening": "open",
            "body": "body",
            "ending": "end",
            "ending_interaction": "互动",
            "estimated_duration": 120,
        }
        score = generator._calculate_quality_score(data)
        assert score == 1.0
        
        # Low score
        data = {
            "title_suggestions": ["a"],  # Only 1
            "core_viewpoints": ["1"],  # Only 1
            "opening": "open",
        }
        score = generator._calculate_quality_score(data)
        assert score < 1.0


class TestGeneratedPrompt:
    """Test GeneratedPrompt model"""
    
    def test_create_prompt(self):
        """Test creating a GeneratedPrompt"""
        prompt = GeneratedPrompt(
            template_type=TemplateType.HOT_INTERPRET,
            title_suggestions=["标题1", "标题2", "标题3"],
            core_viewpoints=["观点1", "观点2", "观点3"],
            opening="开场",
            body="主体",
            ending="结尾",
            ending_interaction="互动话术",
            estimated_duration=120,
        )
        
        assert prompt.template_type == TemplateType.HOT_INTERPRET
        assert len(prompt.title_suggestions) == 3
        assert prompt.quality_score is None
    
    def test_prompt_with_source(self):
        """Test prompt with source info"""
        prompt = GeneratedPrompt(
            template_type=TemplateType.KNOWLEDGE,
            title_suggestions=["A", "B", "C"],
            core_viewpoints=["1", "2", "3"],
            opening="o",
            body="b",
            ending="e",
            ending_interaction="i",
            estimated_duration=180,
            source_bvid="BV1xx411c7mD",
            source_title="原始标题",
        )
        
        assert prompt.source_bvid == "BV1xx411c7mD"
        assert prompt.source_title == "原始标题"
    
    def test_prompt_validation(self):
        """Test prompt validation"""
        with pytest.raises(Exception):
            # Missing required field
            GeneratedPrompt(
                template_type=TemplateType.HOT_INTERPRET,
                title_suggestions=["a"],  # Need 3
                core_viewpoints=["1"],
                opening="o",
                body="b",
                ending="e",
                ending_interaction="i",
                estimated_duration=120,
            )


class TestHenryClient:
    """Test Henry client"""
    
    def test_build_henry_prompt(self):
        """Test prompt building for Henry"""
        client = HenryClient()
        prompt = client._build_henry_prompt("测试标题", "测试描述")
        
        assert "测试标题" in prompt
        assert "测试描述" in prompt
        assert "B站热点话题" in prompt
    
    def test_fallback_prompt_generation(self):
        """Test fallback prompt generation"""
        client = HenryClient()
        result = client._generate_fallback_prompt("测试标题", "测试描述")
        
        assert "title_suggestions" in result
        assert "core_viewpoints" in result
        assert "opening" in result
        assert "body" in result
        assert "ending" in result
        assert "ending_interaction" in result
        assert "estimated_duration" in result
    
    def test_generate_prompt_with_henry(self):
        """Test convenience function"""
        result = generate_prompt_with_henry("测试标题", "测试描述")
        
        assert isinstance(result, dict)
        assert "title_suggestions" in result


class TestMockGeneration:
    """Test prompt generation with mocked Henry client"""
    
    def test_generate_with_mock(self):
        """Test generation with mocked Henry client"""
        mock_response = {
            "title_suggestions": ["测试标题1", "测试标题2", "测试标题3"],
            "core_viewpoints": ["观点1", "观点2", "观点3"],
            "opening": "开场白",
            "body": "主体内容",
            "ending": "结尾",
            "ending_interaction": "欢迎评论",
            "estimated_duration": 120,
        }
        
        mock_client = Mock()
        mock_client.generate_prompt.return_value = mock_response
        
        # Create a mock HotTopic
        mock_topic = Mock()
        mock_topic.title = "测试标题"
        mock_topic.desc = "测试描述"
        mock_topic.author = "测试作者"
        mock_topic.view = 10000
        mock_topic.like = 1000
        mock_topic.coin = 100
        mock_topic.favorite = 50
        mock_topic.share = 10
        mock_topic.bvid = "BVtest123"
        
        generator = PromptGenerator(henry_client=mock_client)
        result = generator.generate(mock_topic, TemplateType.HOT_INTERPRET)
        
        assert result.template_type == TemplateType.HOT_INTERPRET
        assert len(result.title_suggestions) == 3
        assert result.quality_score is not None
        assert result.quality_score > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
