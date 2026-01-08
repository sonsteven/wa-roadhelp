from fastapi import FastAPI
from app.api import traffic
from typing import Dict
import logging

from app.core.logging import setup_logging


# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)
logger.info("Server started and health endpoint ready.")

# Initialize FastAPI app
app = FastAPI(
    title="WA RoadWatch API",
    description="Backend service for ingesting and querying Washington State traffic collision data.",
    version="0.1.0",
)

# Include traffic routes
app.include_router(traffic.router)

# Health check endpoint
@app.get("/health", tags=["Health"])
def health_check() -> Dict[str, str]:
    """Simple health check endpoint"""
    logger.info("Health check requested")
    return {
        "status": "ok",
        "service": "wa-roadwatch",
    }