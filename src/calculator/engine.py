"""
Heat Score Calculator Engine
"""
import math
from typing import List, Optional
from datetime import datetime, timedelta

from src.collector.models import HotTopic


class HeatCalculator:
    """热度计算引擎"""
    
    # 热度权重配置
    WEIGHTS = {
        "view": 1.0,        # 播放量权重
        "like": 3.0,       # 点赞权重
        "coin": 5.0,       # 投币权重
        "favorite": 4.0,  # 收藏权重
        "share": 4.0,      # 分享权重
        "reply": 2.0,      # 评论权重
    }
    
    # 时间衰减因子 (每小时衰减)
    TIME_DECAY_HOUR = 24
    
    def __init__(self, weights: Optional[dict] = None):
        """
        初始化热度计算器
        
        Args:
            weights: 自定义权重，不传则使用默认权重
        """
        self.weights = weights or self.WEIGHTS
    
    def calculate_heat_score(self, topic: HotTopic) -> float:
        """
        计算单个话题的热度分数
        
        Args:
            topic: 热门话题
        
        Returns:
            热度分数
        """
        # 基础分数 = 各维度加权求和
        base_score = (
            self.weights["view"] * math.log1p(topic.view) +
            self.weights["like"] * math.log1p(topic.like) +
            self.weights["coin"] * math.log1p(topic.coin) +
            self.weights["favorite"] * math.log1p(topic.favorite) +
            self.weights["share"] * math.log1p(topic.share) +
            self.weights["reply"] * math.log1p(topic.reply)
        )
        
        # 时间衰减
        time_factor = self._calculate_time_decay(topic.pubdate)
        
        # 综合热度分数
        heat_score = base_score * time_factor
        return round(heat_score, 2)
    
    def _calculate_time_decay(self, pubdate: Optional[int]) -> float:
        """
        计算时间衰减因子
        
        Args:
            pubdate: 发布时间戳
        
        Returns:
            衰减因子 (0-1)
        """
        if not pubdate:
            return 1.0
        
        now = int(datetime.now().timestamp())
        hours_elapsed = (now - pubdate) / 3600
        
        # 指数衰减: e^(-hours / decay_hours)
        decay = math.exp(-hours_elapsed / self.TIME_DECAY_HOUR)
        return max(decay, 0.1)  # 最低保留 10% 热度
    
    def calculate_batch(self, topics: List[HotTopic]) -> List[HotTopic]:
        """
        批量计算热度分数
        
        Args:
            topics: 话题列表
        
        Returns:
            按热度排序的话题列表
        """
        for topic in topics:
            topic.hot_score = self.calculate_heat_score(topic)
        
        # 按热度分数降序排序
        return sorted(topics, key=lambda t: t.hot_score, reverse=True)
    
    def get_top_topics(self, topics: List[HotTopic], n: int = 10) -> List[HotTopic]:
        """
        获取热度最高的N个话题
        
        Args:
            topics: 话题列表
            n: 返回数量
        
        Returns:
            热度最高的N个话题
        """
        sorted_topics = self.calculate_batch(topics)
        return sorted_topics[:n]
    
    def rank_topics(self, topics: List[HotTopic]) -> List[HotTopic]:
        """
        重新计算排名
        
        Args:
            topics: 话题列表
        
        Returns:
            按热度重新排名的话题列表
        """
        sorted_topics = self.calculate_batch(topics)
        for idx, topic in enumerate(sorted_topics):
            topic.rank = idx + 1
        return sorted_topics


def get_default_calculator() -> HeatCalculator:
    """获取默认热度计算器"""
    return HeatCalculator()
