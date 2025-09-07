"""
Chat schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: Optional[str] = None
    context: Optional[dict] = None

class ChatResponse(BaseModel):
    response: str
    crisis_detected: bool = False
    emergency_resources: bool = False
    disclaimer: str
    suggestions: Optional[List[str]] = None
    error: bool = False