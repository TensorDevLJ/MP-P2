"""
Healthcare provider models for nearby care feature
"""
from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.core.database import Base

class HealthcareProvider(Base):
    __tablename__ = "healthcare_providers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Provider details
    google_place_id = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    specialty = Column(String(100), nullable=False)  # psychiatrist, psychologist, etc.
    
    # Location
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(Text, nullable=False)
    
    # Contact
    phone = Column(String(50), nullable=True)
    website = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    
    # Google Places data
    rating = Column(Float, nullable=True)
    user_ratings_total = Column(Integer, nullable=True)
    price_level = Column(Integer, nullable=True)
    opening_hours = Column(JSON, nullable=True)
    photos = Column(JSON, nullable=True)
    
    # Cache metadata
    cached_at = Column(DateTime(timezone=True), server_default=func.now())
    cache_expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Status
    is_verified = Column(Boolean, default=False)
    is_accepting_patients = Column(Boolean, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<HealthcareProvider(id={self.id}, name={self.name})>"

class UserProviderBookmark(Base):
    __tablename__ = "user_provider_bookmarks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    provider_id = Column(UUID(as_uuid=True), nullable=False)
    
    # Bookmark metadata
    notes = Column(Text, nullable=True)
    contacted_at = Column(DateTime(timezone=True), nullable=True)
    appointment_scheduled = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<UserProviderBookmark(user_id={self.user_id}, provider_id={self.provider_id})>"