"""
Dashboard API - Simplified for Prompt Display Only
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

app = FastAPI(title="Bilibili AI Video Dashboard", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Data models
class PromptItem(BaseModel):
    id: str
    topic: str
    template_type: str
    title: str
    quality_score: float
    created_at: str
    opening: Optional[str] = None
    body: Optional[str] = None
    ending: Optional[str] = None
    ending_interaction: Optional[str] = None
    estimated_duration: Optional[int] = None


class DashboardData(BaseModel):
    prompts: List[PromptItem]
    last_updated: str


def load_prompt_data() -> List[Dict[str, Any]]:
    """Load prompt data from JSON file."""
    prompt_file = DATA_DIR / "prompts.json"
    if prompt_file.exists():
        with open(prompt_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def get_latest_prompts_file() -> Optional[Path]:
    """Get the latest daily prompts file."""
    daily_prompts_dir = DATA_DIR / "daily_prompts"
    if not daily_prompts_dir.exists():
        return None
    
    md_files = list(daily_prompts_dir.glob("*.md"))
    if not md_files:
        return None
    
    return max(md_files, key=lambda f: f.stat().st_mtime)


# API Endpoints
@app.get("/")
async def root():
    """Dashboard root endpoint."""
    return {"message": "Bilibili AI Video Prompt Dashboard", "version": "1.0.0"}


@app.get("/api/dashboard", response_model=DashboardData)
async def get_dashboard():
    """Get all dashboard data (prompts only)."""
    prompt_data = load_prompt_data()
    
    prompts = [
        PromptItem(
            id=f"prompt_{i}",
            topic=p.get("topic", ""),
            template_type=p.get("template_type", "HOT_INTERPRET"),
            title=p.get("title", ""),
            quality_score=p.get("quality_score", 0.0),
            created_at=p.get("created_at", datetime.now().isoformat()),
            opening=p.get("opening"),
            body=p.get("body"),
            ending=p.get("ending"),
            ending_interaction=p.get("ending_interaction"),
            estimated_duration=p.get("estimated_duration"),
        )
        for i, p in enumerate(prompt_data)
    ]
    
    # Get last updated time
    latest_file = get_latest_prompts_file()
    last_updated = datetime.now().isoformat()
    if latest_file:
        last_updated = datetime.fromtimestamp(latest_file.stat().st_mtime).isoformat()
    
    return DashboardData(
        prompts=prompts,
        last_updated=last_updated,
    )


@app.get("/api/prompts", response_model=List[PromptItem])
async def get_prompts(limit: int = 10):
    """Get generated prompts list."""
    prompt_data = load_prompt_data()[:limit]
    return [
        PromptItem(
            id=f"prompt_{i}",
            topic=p.get("topic", ""),
            template_type=p.get("template_type", "HOT_INTERPRET"),
            title=p.get("title", ""),
            quality_score=p.get("quality_score", 0.0),
            created_at=p.get("created_at", datetime.now().isoformat()),
            opening=p.get("opening"),
            body=p.get("body"),
            ending=p.get("ending"),
            ending_interaction=p.get("ending_interaction"),
            estimated_duration=p.get("estimated_duration"),
        )
        for i, p in enumerate(prompt_data)
    ]


@app.get("/api/prompt/{prompt_id}")
async def get_prompt_detail(prompt_id: int):
    """Get detailed prompt by ID."""
    prompt_data = load_prompt_data()
    
    if prompt_id < 0 or prompt_id >= len(prompt_data):
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    p = prompt_data[prompt_id]
    return PromptItem(
        id=f"prompt_{prompt_id}",
        topic=p.get("topic", ""),
        template_type=p.get("template_type", "HOT_INTERPRET"),
        title=p.get("title", ""),
        quality_score=p.get("quality_score", 0.0),
        created_at=p.get("created_at", datetime.now().isoformat()),
        opening=p.get("opening"),
        body=p.get("body"),
        ending=p.get("ending"),
        ending_interaction=p.get("ending_interaction"),
        estimated_duration=p.get("estimated_duration"),
    )


@app.post("/api/generate")
async def generate_prompts():
    """Trigger prompt generation manually."""
    from scheduler import run_scheduled_task
    
    try:
        result = run_scheduled_task()
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
