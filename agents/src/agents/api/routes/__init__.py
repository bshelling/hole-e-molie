"""API routes"""

from .chat import router as chat_router
from .reports import router as reports_router
from .health import router as health_router

__all__ = ["chat_router", "reports_router", "health_router"]
