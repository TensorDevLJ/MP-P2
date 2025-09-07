"""
Notification and reminder models
"""
from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Notification details
    type = Column(String(50), nullable=False)  # reminder, alert, recommendation, emergency
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    
    # Delivery channels
    channels = Column(JSON, default=["push"])  # ["push", "email", "sms"]
    
    # Schedule
    scheduled_for = Column(DateTime(timezone=True), nullable=False)
    timezone = Column(String(50), default="UTC")
    
    # Status
    status = Column(String(50), default="pending")  # pending, sent, failed, cancelled
    sent_at = Column(DateTime(timezone=True), nullable=True)
    
    # Delivery tracking
    push_sent = Column(Boolean, default=False)
    email_sent = Column(Boolean, default=False)
    sms_sent = Column(Boolean, default=False)
    
    # Payload for dynamic content
    payload = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="notifications")
    
    def __repr__(self):
        return f"<Notification(id={self.id}, type={self.type}, status={self.status})>"

class PushSubscription(Base):
    __tablename__ = "push_subscriptions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Web Push subscription details
    endpoint = Column(Text, nullable=False)
    p256dh_key = Column(Text, nullable=False)
    auth_key = Column(Text, nullable=False)
    
    # Device info
    user_agent = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="push_subscriptions")
    
    def __repr__(self):
        return f"<PushSubscription(id={self.id}, user_id={self.user_id})>"