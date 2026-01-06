from fastapi import FastAPI
import logging

from app.core.logging import setup_logging

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="WA RoadWatch API",
    description="Backend service for ingesting and querying Washington State traffic collision data.",
    version="0.1.0",
)

@app.get("/health", tags=["Health"])
def health_check():
    """Simple health check endpoint"""
    logger.info("Health check requested")
    return {
        "status": "ok",
        "service": "wa-roadwatch",
    }