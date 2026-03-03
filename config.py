"""
Bilibili AI Video - Configuration
"""
import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

# Daily prompts output directory
DAILY_PROMPTS_DIR = DATA_DIR / "daily_prompts"
DAILY_PROMPTS_DIR.mkdir(exist_ok=True)

# Database (for potential future use)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/bilibili_ai_video.db")

# Bilibili API (read-only for data collection)
BILIBILI_API_BASE = "https://api.bilibili.com"
BILIBILI_POPULAR_ENDPOINT = "/x/web-interface/popular"
BILIBILI_TOP_LIST_ENDPOINT = "/x/web-interface/popular/series/one"

# API settings
REQUEST_TIMEOUT = 30
MAX_TOPICS = 50

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Scheduler settings
SCHEDULED_HOURS = [8, 20]  # Run at 08:00 and 20:00 daily
