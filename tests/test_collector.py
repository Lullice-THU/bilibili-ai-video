"""
Unit tests for Bilibili Collector
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.collector.bilibili import BilibiliCollector
from src.collector.models import HotTopic


class TestBilibiliCollector:
    """Test cases for BilibiliCollector"""
    
    @pytest.fixture
    def collector(self):
        """Create a collector instance for testing"""
        return BilibiliCollector(timeout=10)
    
    def test_parse_topics(self, collector):
        """Test parsing raw data into HotTopic models"""
        raw_list = [
            {
                "bvid": "BV1xx411c7mD",
                "title": "Test Video 1",
                "desc": "Description 1",
                "owner": {"name": "Test Author"},
                "stat": {
                    "view": 100000,
                    "like": 5000,
                    "coin": 1000,
                    "favorite": 2000,
                    "share": 500,
                    "reply": 100
                },
                "pubdate": 1706745600,
                "duration": "10:30",
                "pic": "https://example.com/pic.jpg"
            },
            {
                "bvid": "BV1yy411c7mD",
                "title": "Test Video 2",
                "desc": "Description 2",
                "owner": {"name": "Test Author 2"},
                "stat": {
                    "view": 50000,
                    "like": 2500,
                    "coin": 500,
                    "favorite": 1000,
                    "share": 250,
                    "reply": 50
                },
                "pubdate": 1706659200,
                "duration": "05:20",
                "pic": "https://example.com/pic2.jpg"
            }
        ]
        
        topics = collector._parse_topics(raw_list)
        
        assert len(topics) == 2
        assert topics[0].bvid == "BV1xx411c7mD"
        assert topics[0].title == "Test Video 1"
        assert topics[0].view == 100000
        assert topics[0].rank == 1
        assert topics[1].rank == 2
    
    def test_parse_topics_with_missing_fields(self, collector):
        """Test parsing data with missing fields"""
        raw_list = [
            {
                "bvid": "BV1xx411c7mD",
                "title": "Test Video",
            }
        ]
        
        topics = collector._parse_topics(raw_list)
        
        assert len(topics) == 1
        assert topics[0].bvid == "BV1xx411c7mD"
        assert topics[0].view == 0
        assert topics[0].like == 0
    
    def test_pubdate_str(self, collector):
        """Test pubdate string formatting"""
        raw_list = [
            {
                "bvid": "BV1xx411c7mD",
                "title": "Test Video",
                "pubdate": 1706745600  # 2024-02-01 00:00:00
            }
        ]
        
        topics = collector._parse_topics(raw_list)
        
        assert "2024-02-01" in topics[0].pubdate_str


class TestHotTopic:
    """Test cases for HotTopic model"""
    
    def test_hot_topic_creation(self):
        """Test creating a HotTopic instance"""
        topic = HotTopic(
            bvid="BV1xx411c7mD",
            title="Test Title",
            view=100000,
            like=5000,
            hot_score=1000.5,
            rank=1
        )
        
        assert topic.bvid == "BV1xx411c7mD"
        assert topic.title == "Test Title"
        assert topic.view == 100000
        assert topic.hot_score == 1000.5
        assert topic.rank == 1
    
    def test_hot_topic_defaults(self):
        """Test default values"""
        topic = HotTopic(title="Test")
        
        assert topic.bvid is None
        assert topic.view == 0
        assert topic.hot_score == 0
        assert topic.rank == 0
    
    def test_hot_topic_json_schema(self):
        """Test JSON schema generation"""
        schema = HotTopic.model_json_schema()
        
        assert "title" in schema
        assert "properties" in schema
        assert "bvid" in schema["properties"]
        assert "view" in schema["properties"]
