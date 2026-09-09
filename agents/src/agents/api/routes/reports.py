"""Report endpoints (placeholder for Phase 3)"""

from fastapi import APIRouter, HTTPException
from agents.api.schemas import ReportResponse

router = APIRouter()


@router.get("/reports")
async def list_reports():
    """
    List user's reports (placeholder for Phase 3)

    TODO: Connect to DynamoDB in Phase 3
    """
    return {
        "reports": [],
        "message": "Report storage not yet implemented (Phase 3)"
    }


@router.get("/reports/{report_id}")
async def get_report(report_id: str):
    """
    Get specific report by ID (placeholder for Phase 3)

    TODO: Connect to DynamoDB in Phase 3
    """
    raise HTTPException(
        status_code=501,
        detail="Report storage not yet implemented (Phase 3)"
    )


@router.get("/reports/{report_id}/status")
async def get_report_status(report_id: str):
    """
    Get report status (placeholder for Phase 3)

    TODO: Connect to DynamoDB and NOLA-311 in Phase 3
    """
    raise HTTPException(
        status_code=501,
        detail="Status checking not yet implemented (Phase 3)"
    )
