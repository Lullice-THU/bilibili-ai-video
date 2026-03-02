"""
Unit tests for Heat Calculator
"""
import pytest
from datetime import datetime, timedelta
from src.calculator.engine import HeatCalculator
from src.collector.models import HotTopic


class TestHeatCalculator:
    """Test cases for HeatCalculator"""
    
    @pytest.fixture
    def calculator(self):
        """Create a calculator instance"""
        return HeatCalculator()
    
    def test_calculate_heat_score_basic(self, calculator):
        """Test basic heat score calculation"""
        topic = HotTopic(
            bvid="BV1test",
            title="Test Video",
            view=10000,
            like=1000,
            coin=500,
            favorite=300,
            share=200,
            reply=100
        )
        
        score = calculator.calculate_heat_score(topic)
        
        assert score > 0
        assert isinstance(score, float)
    
    def test_calculate_heat_score_zero_values(self, calculator):
        """Test heat score with all zero values"""
        topic = HotTopic(
            bvid="BV1test",
            title="Test Video",
            view=0,
            like=0,
            coin=0,
            favorite=0,
            share=0,
            reply=0
        )
        
        score = calculator.calculate_heat_score(topic)
        
        assert score == 0.0
    
    def test_higher_engagement_higher_score(self, calculator):
        """Test that higher engagement results in higher score"""
        topic_low = HotTopic(
            bvid="BV1low",
            title="Low Engagement",
            view=100,
            like=10,
            coin=5,
            favorite=3,
            share=2,
            reply=1
        )
        
        topic_high = HotTopic(
            bvid="BV1high",
            title="High Engagement",
            view=10000,
            like=1000,
            coin=500,
            favorite=300,
            share=200,
            reply=100
        )
        
        score_low = calculator.calculate_heat_score(topic_low)
        score_high = calculator.calculate_heat_score(topic_high)
        
        assert score_high > score_low
    
    def test_weight_customization(self):
        """Test custom weights"""
        custom_weights = {
            "view": 1.0,
            "like": 10.0,   # 更高的点赞权重
            "coin": 1.0,
            "favorite": 1.0,
            "share": 1.0,
            "reply": 1.0
        }
        
        calculator = HeatCalculator(weights=custom_weights)
        
        topic = HotTopic(
            bvid="BV1test",
            title="Test",
            view=100,
            like=1000,
            coin=100,
            favorite=100,
            share=100,
            reply=100
        )
        
        score = calculator.calculate_heat_score(topic)
        
        # 由于点赞权重高，分数应该更高
        assert score > 0
    
    def test_calculate_time_decay(self, calculator):
        """Test time decay calculation"""
        # 刚刚发布的话题
        now = int(datetime.now().timestamp())
        topic_recent = HotTopic(
            bvid="BV1recent",
            title="Recent",
            pubdate=now - 3600,  # 1小时前
            view=1000
        )
        
        # 24小时前发布的话题
        topic_old = HotTopic(
            bvid="BV1old",
            title="Old",
            pubdate=now - 86400,  # 24小时前
            view=1000
        )
        
        score_recent = calculator.calculate_heat_score(topic_recent)
        score_old = calculator.calculate_heat_score(topic_old)
        
        # 最近发布的话题分数应该更高
        assert score_recent > score_old
    
    def test_calculate_batch(self, calculator):
        """Test batch heat score calculation"""
        topics = [
            HotTopic(bvid="BV1a", title="A", view=100, like=10),
            HotTopic(bvid="BV1b", title="B", view=1000, like=100),
            HotTopic(bvid="BV1c", title="C", view=10000, like=1000),
        ]
        
        sorted_topics = calculator.calculate_batch(topics)
        
        # 应该按热度降序排序
        assert sorted_topics[0].hot_score >= sorted_topics[1].hot_score
        assert sorted_topics[1].hot_score >= sorted_topics[2].hot_score
    
    def test_get_top_topics(self, calculator):
        """Test getting top N topics"""
        topics = [
            HotTopic(bvid="BV1a", title="A", view=100),
            HotTopic(bvid="BV1b", title="B", view=1000),
            HotTopic(bvid="BV1c", title="C", view=500),
            HotTopic(bvid="BV1d", title="D", view=2000),
            HotTopic(bvid="BV1e", title="E", view=800),
        ]
        
        top3 = calculator.get_top_topics(topics, n=3)
        
        assert len(top3) == 3
        # B和D应该是前3
        assert any(t.bvid == "BV1b" for t in top3)
        assert any(t.bvid == "BV1d" for t in top3)
    
    def test_rank_topics(self, calculator):
        """Test ranking topics"""
        topics = [
            HotTopic(bvid="BV1a", title="A", rank=3, view=100),
            HotTopic(bvid="BV1b", title="B", rank=1, view=1000),
            HotTopic(bvid="BV1c", title="C", rank=2, view=500),
        ]
        
        ranked = calculator.rank_topics(topics)
        
        # 排名应该被重新计算
        assert ranked[0].rank == 1  # B
        assert ranked[1].rank == 2  # C
        assert ranked[2].rank == 3  # A


class TestHeatCalculatorEdgeCases:
    """Test edge cases"""
    
    def test_no_pubdate(self):
        """Test topic without pubdate"""
        calculator = HeatCalculator()
        topic = HotTopic(
            bvid="BV1test",
            title="Test",
            pubdate=None,
            view=1000
        )
        
        score = calculator.calculate_heat_score(topic)
        
        # 没有pubdate应该使用默认时间因子
        assert score > 0
    
    def test_log_scale(self):
        """Test that log scale is used"""
        calculator = HeatCalculator()
        
        # 10倍播放量
        topic1 = HotTopic(bvid="BV1a", title="A", view=100)
        topic2 = HotTopic(bvid="BV1b", title="B", view=1000)
        
        score1 = calculator.calculate_heat_score(topic1)
        score2 = calculator.calculate_heat_score(topic2)
        
        # 不是10倍，而是对数级差异
        ratio = score2 / score1
        assert 1 < ratio < 10
