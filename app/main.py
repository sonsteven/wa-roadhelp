from fastapi import FastAPI
from app.api import traffic, lookups, stats
from typing import Dict
import logging

from app.core.logging import setup_logging


# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)
logger.info("Server started and health endpoint ready.")

# Initialize FastAPI app
app = FastAPI(
    title="SEA-RoadInfo API",
    description="Backend service for ingesting, normalizing, and querying Seattle traffic collision data.",
    version="0.1.0",
)

# Include API routes
app.include_router(traffic.router)
app.include_router(lookups.router)
app.include_router(stats.router)

# Health check endpoint
@app.get("/health", tags=["Health"])
def health_check() -> Dict[str, str]:
    """Simple health check endpoint"""
    logger.info("Health check requested")
    return {
        "status": "ok",
        "service": "sea-roadinfo",
    }