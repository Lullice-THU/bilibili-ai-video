"""
Bilibili AI Video - Configuration
"""
import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/bilibili_ai_video.db")

# Bilibili API
BILIBILI_API_BASE = "https://api.bilibili.com"
BILIBILI_POPULAR_ENDPOINT = "/x/web-interface/popular"
BILIBILI_TOP_LIST_ENDPOINT = "/x/web-interface/popular/series/one"

# API settings
REQUEST_TIMEOUT = 30
MAX_TOPICS = 50

# Video settings
VIDEO_OUTPUT_DIR = DATA_DIR / "videos"
VIDEO_OUTPUT_DIR.mkdir(exist_ok=True)

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
