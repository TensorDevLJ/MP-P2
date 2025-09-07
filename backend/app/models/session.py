"""
EEG analysis session models
"""
from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON, Integer, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base

class AnalysisSession(Base):
    __tablename__ = "analysis_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Session metadata
    session_type = Column(String(50), nullable=False)  # "eeg", "text", "combined"
    file_key = Column(String(255), nullable=True)  # S3 key for EEG file
    sampling_rate = Column(Integer, nullable=True)
    channel = Column(String(50), nullable=True)
    epoch_length = Column(Float, default=2.0)
    overlap = Column(Float, default=0.5)
    
    # Model versions for reproducibility
    eeg_model_version = Column(String(50), nullable=True)
    text_model_version = Column(String(50), nullable=True)
    fusion_version = Column(String(50), nullable=True)
    
    # Analysis results
    emotion_results = Column(JSON, nullable=True)  # {label, probabilities, confidence}
    anxiety_results = Column(JSON, nullable=True)
    depression_results = Column(JSON, nullable=True)
    fusion_results = Column(JSON, nullable=True)
    
    # Features and explanations
    eeg_features = Column(JSON, nullable=True)  # Band powers, asymmetry, etc.
    explanations = Column(JSON, nullable=True)  # Natural language explanations
    
    # Processing status
    status = Column(String(50), default="pending")  # pending, processing, completed, failed
    error_message = Column(Text, nullable=True)
    processing_started_at = Column(DateTime(timezone=True), nullable=True)
    processing_completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="analysis_sessions")
    
    def __repr__(self):
        return f"<AnalysisSession(id={self.id}, user_id={self.user_id}, status={self.status})>"

class TextInput(Base):
    __tablename__ = "text_inputs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("analysis_sessions.id"), nullable=False)
    
    # Text content (encrypted)
    content = Column(Text, nullable=False)
    content_hash = Column(String(64), nullable=False)  # For deduplication
    
    # Analysis results
    sentiment_score = Column(Float, nullable=True)
    depression_score = Column(Float, nullable=True)
    anxiety_keywords = Column(JSON, nullable=True)
    safety_flags = Column(JSON, nullable=True)  # Crisis detection flags
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    session = relationship("AnalysisSession", backref="text_inputs")
    
    def __repr__(self):
        return f"<TextInput(id={self.id}, session_id={self.session_id})>"