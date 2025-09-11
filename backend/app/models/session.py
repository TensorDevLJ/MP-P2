"""
Simplified analysis session model
"""
from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON, Integer, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base

class AnalysisSession(Base):
    __tablename__ = "analysis_sessions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # Session data
    text_input = Column(Text, nullable=True)
    file_path = Column(String(255), nullable=True)
    
    # Results
    depression_result = Column(String(50), nullable=True)  # "not_depressed", "mild", "moderate", "severe"
    confidence_score = Column(Float, nullable=True)
    detailed_analysis = Column(JSON, nullable=True)
    
    # Status
    status = Column(String(50), default="pending")  # pending, completed, failed
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", backref="sessions")
    
    def __repr__(self):
        return f"<AnalysisSession(id={self.id}, result={self.depression_result})>"