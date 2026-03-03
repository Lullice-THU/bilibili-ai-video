"""
Dashboard API Tests - M6.3 Integration Tests
"""
import pytest
from fastapi.testclient import TestClient

from src.dashboard.api import app

client = TestClient(app)


def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_hot_topics():
    """Test hot topics endpoint."""
    response = client.get("/api/hot-topics")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10


def test_hot_topics_with_limit():
    """Test hot topics with custom limit."""
    response = client.get("/api/hot-topics?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5


def test_videos():
    """Test videos endpoint."""
    response = client.get("/api/videos")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_videos_with_limit():
    """Test videos with custom limit."""
    response = client.get("/api/videos?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_stats():
    """Test stats endpoint."""
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    
    # Check required fields
    assert "total_videos" in data
    assert "total_views" in data
    assert "total_likes" in data
    assert "total_coins" in data
    assert "total_favorites" in data
    assert "follower_count" in data
    assert "fan_growth_rate" in data
    assert "avg_view_count" in data
    assert "avg_like_rate" in data
    
    # Check data types
    assert isinstance(data["total_videos"], int)
    assert isinstance(data["total_views"], int)
    assert isinstance(data["fan_growth_rate"], float)


def test_prompts():
    """Test prompts endpoint."""
    response = client.get("/api/prompts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_prompts_with_limit():
    """Test prompts with custom limit."""
    response = client.get("/api/prompts?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_dashboard():
    """Test dashboard combined endpoint."""
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    
    # Check all sections
    assert "hot_topics" in data
    assert "prompts" in data
    assert "videos" in data
    assert "stats" in data
    
    # Check hot topics structure
    for topic in data["hot_topics"]:
        assert "rank" in topic
        assert "title" in topic
        assert "bvid" in topic
        assert "view_count" in topic
        assert "heat_score" in topic
    
    # Check stats structure
    stats = data["stats"]
    assert "total_videos" in stats
    assert "total_views" in stats


def test_dashboard_hot_topics_sorted():
    """Test that hot topics are sorted by rank."""
    response = client.get("/api/hot-topics")
    data = response.json()
    
    ranks = [topic["rank"] for topic in data]
    assert ranks == sorted(ranks)


def test_stats_non_negative():
    """Test that all stats are non-negative."""
    response = client.get("/api/stats")
    data = response.json()
    
    assert data["total_videos"] >= 0
    assert data["total_views"] >= 0
    assert data["total_likes"] >= 0
    assert data["total_coins"] >= 0
    assert data["total_favorites"] >= 0
    assert data["follower_count"] >= 0
