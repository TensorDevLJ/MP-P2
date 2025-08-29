from sqlalchemy import Column, String, DateTime, Boolean, JSON, Float, Integer, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    display_name = Column(String, nullable=True)
    timezone = Column(String, default="Asia/Kolkata")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    sessions = relationship("Session", back_populates="user")
    notifications = relationship("Notification", back_populates="user")

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    file_key = Column(String, nullable=True)
    text_input = Column(Text, nullable=True)
    
    # Analysis results
    emotion_result = Column(JSON, nullable=True)
    anxiety_result = Column(JSON, nullable=True)
    depression_result = Column(JSON, nullable=True)
    fusion_result = Column(JSON, nullable=True)
    explanation = Column(JSON, nullable=True)
    
    # Metadata
    sampling_rate = Column(Integer, nullable=True)
    channels = Column(String, nullable=True)
    model_version = Column(String, nullable=True)
    
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="sessions")

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    type = Column(String, nullable=False)  # reminder, alert, info
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default="pending")  # pending, sent, failed
    payload = Column(JSON, nullable=True)
    
    user = relationship("User", back_populates="notifications")