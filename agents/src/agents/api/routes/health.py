"""Health check endpoints"""

from fastapi import APIRouter
from agents.config import get_settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "holeemoly-api",
        "version": "0.1.0"
    }


@router.get("/config")
async def config_info():
    """Configuration info (non-sensitive values only)"""
    settings = get_settings()
    return {
        "model": settings.bedrock_model,
        "region": settings.aws_region,
        "cors_origins": settings.cors_origins_list,
        "api_port": settings.api_port
    }
