"""
EEG analysis schemas
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class EEGUploadResponse(BaseModel):
    file_key: str
    filename: str
    size_bytes: int
    sampling_rate: Optional[int]
    channels: List[str]
    duration_seconds: Optional[float]

class EEGProcessRequest(BaseModel):
    file_key: str
    sampling_rate: Optional[int] = 128
    channel: Optional[str] = "EEG.AF3"
    epoch_length: Optional[float] = 2.0
    overlap: Optional[float] = 0.5
    
    @validator('epoch_length')
    def validate_epoch_length(cls, v):
        if v <= 0 or v > 10:
            raise ValueError('Epoch length must be between 0 and 10 seconds')
        return v
    
    @validator('overlap')
    def validate_overlap(cls, v):
        if v < 0 or v >= 1:
            raise ValueError('Overlap must be between 0 and 1')
        return v

class EEGResultResponse(BaseModel):
    job_id: str
    status: str
    message: Optional[str] = None
    
    # Results (when completed)
    emotion_results: Optional[Dict[str, Any]] = None
    anxiety_results: Optional[Dict[str, Any]] = None
    eeg_features: Optional[Dict[str, Any]] = None
    explanations: Optional[List[str]] = None
    charts_data: Optional[Dict[str, Any]] = None
    processing_time: Optional[float] = None