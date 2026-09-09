"""Data models for pothole reports and status"""

from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, Literal
import re


class Location(BaseModel):
    """Location information for a pothole"""

    address: str = Field(..., min_length=5, max_length=500, description="Street address")
    cross_street: Optional[str] = Field(None, max_length=200, description="Nearest cross street")
    landmark: Optional[str] = Field(None, max_length=200, description="Nearby landmark")
    coordinates: Optional[dict] = Field(None, description="GPS coordinates {lat, lng}")

    @validator('address')
    def validate_address(cls, v):
        """Ensure address is not just whitespace"""
        if not v or not v.strip():
            raise ValueError("Address cannot be empty")
        return v.strip()

    @validator('coordinates')
    def validate_coordinates(cls, v):
        """Validate coordinate format if provided"""
        if v is not None:
            if 'lat' not in v or 'lng' not in v:
                raise ValueError("Coordinates must have 'lat' and 'lng' keys")

            lat = v['lat']
            lng = v['lng']

            # Basic validation for New Orleans area
            # Latitude: ~29-30, Longitude: ~-90 to -89
            if not (28.5 <= lat <= 30.5):
                raise ValueError(f"Latitude {lat} outside New Orleans area")
            if not (-91 <= lng <= -88):
                raise ValueError(f"Longitude {lng} outside New Orleans area")

        return v


class PotholeReport(BaseModel):
    """Complete pothole report data"""

    location: Location
    description: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Detailed description of the pothole"
    )
    severity: Literal["low", "medium", "high"] = Field(
        default="medium",
        description="Severity level"
    )

    # Reporter information
    reporter_name: str = Field(..., min_length=2, max_length=100, description="Reporter's name")
    email: EmailStr = Field(..., description="Reporter's email")
    phone: Optional[str] = Field(None, description="Reporter's phone number")

    # Optional metadata
    date_noticed: Optional[datetime] = Field(None, description="When the pothole was noticed")
    photo_url: Optional[str] = Field(None, description="URL to uploaded photo")

    @validator('description')
    def validate_description(cls, v):
        """Ensure description is meaningful"""
        if not v or not v.strip():
            raise ValueError("Description cannot be empty")

        # Remove excessive whitespace
        v = ' '.join(v.split())

        if len(v) < 10:
            raise ValueError("Description must be at least 10 characters")

        return v

    @validator('reporter_name')
    def validate_name(cls, v):
        """Validate reporter name"""
        if not v or not v.strip():
            raise ValueError("Reporter name cannot be empty")

        # Remove excessive whitespace
        v = ' '.join(v.split())

        if len(v) < 2:
            raise ValueError("Name must be at least 2 characters")

        return v

    @validator('phone')
    def validate_phone(cls, v):
        """Validate US phone number format if provided"""
        if v is None:
            return v

        # Remove common formatting characters
        digits = re.sub(r'[^\d]', '', v)

        # US phone numbers should be 10 digits (or 11 with country code)
        if len(digits) == 10:
            # Format as (XXX) XXX-XXXX
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits[0] == '1':
            # Format as +1 (XXX) XXX-XXXX
            return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        else:
            raise ValueError(f"Invalid US phone number format: {v}")

    class Config:
        json_schema_extra = {
            "example": {
                "location": {
                    "address": "1234 Magazine St, New Orleans, LA 70130",
                    "cross_street": "Napoleon Ave",
                    "landmark": "Near Whole Foods"
                },
                "description": "Large pothole in right lane, approximately 2 feet wide and 6 inches deep",
                "severity": "high",
                "reporter_name": "Jane Doe",
                "email": "jane@example.com",
                "phone": "(504) 555-1234"
            }
        }


class StatusResult(BaseModel):
    """Result of status check"""

    reference_number: str = Field(..., description="NOLA-311 reference number")
    status: Literal["submitted", "in_progress", "resolved", "duplicate", "closed", "unknown"] = Field(
        ...,
        description="Normalized status"
    )
    raw_status: str = Field(..., description="Original status from NOLA-311")
    notes: str = Field(default="", description="Status notes or updates")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update time")

    class Config:
        json_schema_extra = {
            "example": {
                "reference_number": "311-2026-0908-001",
                "status": "in_progress",
                "raw_status": "Assigned",
                "notes": "Crew assigned for repair on Sept 10",
                "updated_at": "2026-09-08T15:30:00Z"
            }
        }


class SubmissionResult(BaseModel):
    """Result of form submission"""

    success: bool = Field(..., description="Whether submission succeeded")
    reference_number: Optional[str] = Field(None, description="NOLA-311 reference number if successful")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    submitted_at: datetime = Field(default_factory=datetime.utcnow, description="Submission timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "reference_number": "311-2026-0908-001",
                "error_message": None,
                "submitted_at": "2026-09-08T14:25:00Z"
            }
        }
