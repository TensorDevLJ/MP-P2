"""
Text analysis schemas
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class TextAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=10000)
    
    @validator('text')
    def validate_text_content(cls, v):
        # Remove excessive whitespace
        v = ' '.join(v.split())
        if len(v.strip()) < 10:
            raise ValueError('Text must be at least 10 characters after cleaning')
        return v

class TextAnalysisResponse(BaseModel):
    session_id: str
    depression_analysis: Dict[str, Any]
    sentiment_analysis: Dict[str, Any]
    anxiety_keywords: Dict[str, Any]
    safety_flags: Dict[str, Any]
    text_statistics: Dict[str, Any]
    recommendations: List[Dict[str, str]]

class TextInputCreate(BaseModel):
    content: str
    session_id: str

class TextInputResponse(BaseModel):
    id: str
    session_id: str
    sentiment_score: Optional[float]
    depression_score: Optional[float]
    created_at: datetime
    safety_flags: Optional[Dict[str, Any]]