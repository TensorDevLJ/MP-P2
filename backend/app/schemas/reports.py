"""
Report and data export schemas
"""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class ReportRequest(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    include_raw_data: bool = False
    format: str = "json"

class UserDataExport(BaseModel):
    user_profile: Dict[str, Any]
    analysis_sessions: List[Dict[str, Any]]
    notifications: List[Dict[str, Any]]
    export_metadata: Dict[str, Any]

class TrendsSummary(BaseModel):
    period_start: datetime
    period_end: datetime
    total_sessions: int
    risk_distribution: Dict[str, int]
    emotion_distribution: Dict[str, int]
    weekly_averages: Dict[str, float]