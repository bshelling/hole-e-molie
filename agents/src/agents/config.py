"""Configuration management for HoleeMoly API"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # AWS Configuration
    bedrock_model: str
    aws_default_profile: str = "default"
    aws_region: str = "us-east-1"

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True

    # CORS Configuration
    cors_origins: str = "http://localhost:3000"

    # DynamoDB Configuration (for Phase 3)
    dynamodb_table: str = "holeemoly-data"
    dynamodb_endpoint: Optional[str] = None  # For dynamodb-local

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
