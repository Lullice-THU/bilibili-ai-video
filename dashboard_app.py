"""
Dashboard Main Entry - Simplified for Prompt Display
Serves both the API and the frontend
"""
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

# Create main app
app = FastAPI(title="Bilibili AI Video Dashboard", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get dashboard directory
DASHBOARD_DIR = Path(__file__).parent / "dashboard"


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main dashboard page."""
    index_file = DASHBOARD_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return HTMLResponse("<h1>Dashboard not found</h1>", status_code=404)


# Include API routes
from src.dashboard.api import (
    get_dashboard,
    get_prompts,
    get_prompt_detail,
    generate_prompts,
)

app.add_api_route("/api/dashboard", get_dashboard)
app.add_api_route("/api/prompts", get_prompts)
app.add_api_route("/api/prompt/{prompt_id}", get_prompt_detail)
app.add_api_route("/api/generate", generate_prompts, methods=["POST"])


if __name__ == "__main__":
    import uvicorn
    print("Starting Dashboard at http://localhost:5000")
    uvicorn.run(app, host="0.0.0.0", port=5000)
