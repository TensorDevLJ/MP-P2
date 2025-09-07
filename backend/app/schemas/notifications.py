"""
Notification schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class PushSubscriptionCreate(BaseModel):
    endpoint: str
    p256dh_key: str
    auth_key: str
    user_agent: Optional[str] = None

class ScheduleReminderRequest(BaseModel):
    type: str = Field(..., description="Type of reminder")
    title: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1, max_length=1000)
    scheduled_for: datetime
    channels: List[str] = Field(default=["push"])
    payload: Optional[Dict[str, Any]] = None

class NotificationCreate(BaseModel):
    type: str
    title: str
    message: str
    channels: List[str] = ["push"]
    scheduled_for: Optional[datetime] = None
    payload: Optional[Dict[str, Any]] = None

class NotificationResponse(BaseModel):
    id: str
    type: str
    title: str
    message: str
    status: str
    scheduled_for: datetime
    sent_at: Optional[datetime]
    created_at: datetime