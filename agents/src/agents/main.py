"""HoleeMoly API - FastAPI application"""

from fastapi import FastAPI
from agents.api.routes import chat_router, reports_router, health_router
from agents.api.middleware import setup_cors
from agents.config import get_settings
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="HoleeMoly API",
    description="NOLA pothole reporting and tracking agent API",
    version="0.1.0",
)

# Setup CORS
setup_cors(app)

# Include routers
app.include_router(health_router, prefix="/api", tags=["health"])
app.include_router(chat_router, prefix="/api", tags=["chat"])
app.include_router(reports_router, prefix="/api", tags=["reports"])


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    settings = get_settings()
    logger.info("Starting HoleeMoly API")
    logger.info(f"Model: {settings.bedrock_model}")
    logger.info(f"Region: {settings.aws_region}")
    logger.info(f"CORS origins: {settings.cors_origins_list}")
    logger.info(f"API server will run on {settings.api_host}:{settings.api_port}")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("Shutting down HoleeMoly API")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "HoleeMoly API - NOLA Pothole Reporting Agent",
        "docs": "/docs",
        "health": "/api/health",
        "websocket": "ws://localhost:8000/api/chat"
    }


def run():
    """Run the FastAPI application"""
    import uvicorn
    settings = get_settings()

    uvicorn.run(
        "agents.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        log_level=settings.log_level.lower()
    )


if __name__ == "__main__":
    run()
