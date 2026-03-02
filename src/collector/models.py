"""
Bilibili Hot Topic Data Models
"""
from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, Field, field_validator


class HotTopic(BaseModel):
    """B站热门话题数据模型"""
    bvid: Optional[str] = Field(None, description="视频BV号")
    title: str = Field(..., description="标题")
    desc: str = Field("", description="描述")
    author: str = Field("", description="作者")
    view: int = Field(0, description="播放量")
    like: int = Field(0, description="点赞数")
    coin: int = Field(0, description="投币数")
    favorite: int = Field(0, description="收藏数")
    share: int = Field(0, description="分享数")
    reply: int = Field(0, description="评论数")
    pubdate: Optional[int] = Field(None, description="发布时间戳")
    duration: Optional[Union[str, int]] = Field(None, description="视频时长")
    pic: Optional[str] = Field(None, description="封面图片URL")
    
    # 计算字段
    hot_score: float = Field(0, description="热度分数")
    rank: int = Field(0, description="排名")
    
    @field_validator('duration', mode='before')
    @classmethod
    def parse_duration(cls, v):
        """将秒数转换为时长字符串"""
        if isinstance(v, int):
            minutes, seconds = divmod(v, 60)
            hours, minutes = divmod(minutes, 60)
            if hours > 0:
                return f"{hours}:{minutes:02d}:{seconds:02d}"
            return f"{minutes}:{seconds:02d}"
        return v
    
    @property
    def pubdate_str(self) -> str:
        """格式化发布时间"""
        if self.pubdate:
            return datetime.fromtimestamp(self.pubdate).strftime("%Y-%m-%d %H:%M:%S")
        return ""
    
    class Config:
        json_schema_extra = {
            "example": {
                "bvid": "BV1xx411c7mD",
                "title": "示例视频标题",
                "view": 100000,
                "like": 5000
            }
        }
