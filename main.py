"""
Bilibili AI Video - Main Entry Point
"""
import logging
import argparse
from datetime import datetime, timedelta
import time
import threading

from config import LOG_LEVEL, SCHEDULED_HOURS
from scheduler import run_scheduled_task

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_scheduler():
    """Run the scheduler in the background"""
    logger.info(f"Starting scheduler for hours: {SCHEDULED_HOURS}")
    
    while True:
        now = datetime.now()
        next_run = None
        
        for hour in SCHEDULED_HOURS:
            candidate = now.replace(hour=hour, minute=0, second=0, microsecond=0)
            if candidate > now:
                if next_run is None or candidate < next_run:
                    next_run = candidate
        
        # If no time today, schedule for tomorrow
        if next_run is None:
            next_run = now.replace(hour=SCHEDULED_HOURS[0], minute=0, second=0, microsecond=0) + timedelta(days=1)
        
        wait_seconds = (next_run - now).total_seconds()
        logger.info(f"Next scheduled run at {next_run}, waiting {wait_seconds:.0f} seconds")
        
        time.sleep(wait_seconds)
        
        # Run the task
        try:
            logger.info("Running scheduled prompt generation...")
            result = run_scheduled_task()
            logger.info(f"Scheduled task result: {result}")
        except Exception as e:
            logger.error(f"Error in scheduled task: {e}")


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="Bilibili AI Video Prompt Generator")
    parser.add_argument("--run-now", action="store_true", help="Run prompt generation now")
    parser.add_argument("--schedule", action="store_true", help="Run scheduler in background")
    
    args = parser.parse_args()
    
    logger.info("Bilibili AI Video Prompt Generator starting...")
    
    if args.run_now:
        logger.info("Running prompt generation now...")
        result = run_scheduled_task()
        logger.info(f"Result: {result}")
    elif args.schedule:
        run_scheduler()
    else:
        # Default: run once
        logger.info("Running prompt generation once...")
        result = run_scheduled_task()
        logger.info(f"Result: {result}")


if __name__ == "__main__":
    main()
