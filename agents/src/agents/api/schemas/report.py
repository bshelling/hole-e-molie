"""Report schemas (placeholder for Phase 3)"""

from pydantic import BaseModel
from datetime import datetime


class ReportBase(BaseModel):
    """Base report schema (placeholder for Phase 3)"""
    location: str
    description: str


class ReportResponse(BaseModel):
    """Report response (placeholder for Phase 3)"""
    report_id: str
    status: str
    created_at: datetime
