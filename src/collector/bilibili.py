"""
Bilibili API Client
"""
import logging
from typing import List, Optional
import httpx

from config import BILIBILI_API_BASE, BILIBILI_POPULAR_ENDPOINT, REQUEST_TIMEOUT, MAX_TOPICS
from .models import HotTopic

logger = logging.getLogger(__name__)


class BilibiliCollector:
    """B站数据采集器"""
    
    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com",
        "Origin": "https://www.bilibili.com"
    }
    
    def __init__(self, timeout: int = REQUEST_TIMEOUT):
        self.base_url = BILIBILI_API_BASE
        self.timeout = timeout
        self.client = httpx.Client(timeout=timeout, headers=self.DEFAULT_HEADERS)
    
    def get_popular_list(self, pn: int = 1, ps: int = MAX_TOPICS) -> List[HotTopic]:
        """
        获取B站热门视频列表
        
        Args:
            pn: 页码
            ps: 每页数量
        
        Returns:
            热门话题列表
        """
        url = f"{self.base_url}{BILIBILI_POPULAR_ENDPOINT}"
        params = {
            "pn": pn,
            "ps": ps
        }
        
        try:
            response = self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") != 0:
                logger.error(f"API error: {data.get('message')}")
                return []
            
            return self._parse_topics(data.get("data", {}).get("list", []))
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            return []
        except Exception as e:
            logger.error(f"Error fetching popular list: {e}")
            return []
    
    def get_popular_series(self, number: Optional[int] = None) -> List[HotTopic]:
        """
        获取B站热门排行榜系列
        
        Args:
            number: 排行榜期数，不传则获取最新
        
        Returns:
            热门视频列表
        """
        endpoint = f"{self.base_url}/x/web-interface/popular/series/one"
        params = {}
        if number:
            params["number"] = number
        
        try:
            response = self.client.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") != 0:
                logger.error(f"API error: {data.get('message')}")
                return []
            
            # 获取当前期数信息
            series_data = data.get("data", {})
            logger.info(f"Got series {series_data.get('number')}: {series_data.get('title')}")
            
            # 返回列表数据
            return self._parse_topics(series_data.get("list", []))
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            return []
        except Exception as e:
            logger.error(f"Error fetching popular series: {e}")
            return []
    
    def _parse_topics(self, raw_list: List[dict]) -> List[HotTopic]:
        """解析原始数据为HotTopic模型列表"""
        topics = []
        for idx, item in enumerate(raw_list):
            try:
                topic = HotTopic(
                    bvid=item.get("bvid"),
                    title=item.get("title", ""),
                    desc=item.get("desc", ""),
                    author=item.get("author", ""),
                    view=item.get("view", 0),
                    like=item.get("like", 0),
                    coin=item.get("coin", 0),
                    favorite=item.get("favorite", 0),
                    share=item.get("share", 0),
                    reply=item.get("reply", 0),
                    pubdate=item.get("pubdate"),
                    duration=item.get("duration"),
                    pic=item.get("pic"),
                    rank=idx + 1
                )
                topics.append(topic)
            except Exception as e:
                logger.warning(f"Failed to parse topic: {e}")
                continue
        
        return topics
    
    def collect_topics(self, limit: int = MAX_TOPICS) -> List[HotTopic]:
        """
        采集热门话题
        
        Args:
            limit: 返回数量限制
        
        Returns:
            热门话题列表
        """
        topics = self.get_popular_list(ps=limit)
        logger.info(f"Collected {len(topics)} topics from Bilibili")
        return topics
    
    def close(self):
        """关闭HTTP客户端"""
        self.client.close()


def get_bilibili_collector() -> BilibiliCollector:
    """获取B站采集器实例"""
    return BilibiliCollector()
