"""
Healthcare provider schemas
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

class ProviderSearchRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    specialty: str = Field(default="mental health")
    radius_km: float = Field(default=10, ge=1, le=50)
    max_results: int = Field(default=20, ge=1, le=50)

class ProviderResponse(BaseModel):
    id: Optional[str] = None
    google_place_id: str
    name: str
    specialty: str
    latitude: float
    longitude: float
    address: str
    phone: Optional[str] = None
    website: Optional[str] = None
    rating: Optional[float] = None
    user_ratings_total: Optional[int] = None
    price_level: Optional[int] = None
    opening_hours: Optional[List[str]] = None
    distance_km: float
    open_now: bool = False

class BookmarkRequest(BaseModel):
    provider_id: str
    notes: Optional[str] = None

class BookmarkResponse(BaseModel):
    id: str
    provider: ProviderResponse
    notes: Optional[str]
    bookmarked_at: datetime
    contacted_at: Optional[datetime] = None
    appointment_scheduled: bool = False