"""
Combined analysis schemas
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any

class CombinedAnalysisRequest(BaseModel):
    file_key: Optional[str] = None
    text_input: Optional[str] = None
    sampling_rate: Optional[int] = 128
    channel: Optional[str] = "EEG.AF3"
    epoch_length: Optional[float] = 2.0
    overlap: Optional[float] = 0.5
    
    @validator('text_input')
    def validate_text_input(cls, v):
        if v and len(v.strip()) < 10:
            raise ValueError('Text input must be at least 10 characters long')
        return v

class RecommendationItem(BaseModel):
    id: str
    title: str
    description: str
    duration_minutes: int
    type: str
    evidence_level: str
    instructions: List[str]
    tags: List[str]
    priority: Optional[str] = None

class CombinedAnalysisResponse(BaseModel):
    session_id: str
    status: str
    message: Optional[str] = None
    
    # Results (when completed)
    emotion_results: Optional[Dict[str, Any]] = None
    anxiety_results: Optional[Dict[str, Any]] = None
    depression_results: Optional[Dict[str, Any]] = None
    fusion_results: Optional[Dict[str, Any]] = None
    explanations: Optional[List[str]] = None
    recommendations: Optional[List[RecommendationItem]] = None
    charts_data: Optional[Dict[str, Any]] = None
    processing_time: Optional[float] = None