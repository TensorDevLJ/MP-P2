"""
User database models
"""
from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    display_name = Column(String(100), nullable=True)
    timezone = Column(String(50), default="UTC")
    
    # Profile and preferences
    date_of_birth = Column(DateTime, nullable=True)
    emergency_contact = Column(Text, nullable=True)
    medical_history = Column(JSON, nullable=True)  # Encrypted JSON
    preferences = Column(JSON, nullable=True)  # Notification preferences, language, etc.
    
    # Account status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String(255), nullable=True)
    
    # Privacy and consent
    consent_research = Column(Boolean, default=False)
    consent_data_sharing = Column(Boolean, default=False)
    data_retention_days = Column(String(20), default="365")  # 1 year default
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"