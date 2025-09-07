"""
Notification management endpoints
"""
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import structlog
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.notification import Notification, PushSubscription
from app.schemas.notifications import (
    NotificationCreate, NotificationResponse, 
    PushSubscriptionCreate, ScheduleReminderRequest
)
from app.services.notifications import NotificationService

logger = structlog.get_logger(__name__)
router = APIRouter()

notification_service = NotificationService()

@router.post("/subscribe", response_model=dict)
async def subscribe_to_push(
    subscription: PushSubscriptionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Subscribe to push notifications"""
    
    # Check if subscription already exists
    existing = db.query(PushSubscription).filter(
        PushSubscription.user_id == current_user.id,
        PushSubscription.endpoint == subscription.endpoint
    ).first()
    
    if existing:
        # Update existing subscription
        existing.p256dh_key = subscription.p256dh_key
        existing.auth_key = subscription.auth_key
        existing.user_agent = subscription.user_agent
        existing.is_active = True
        existing.updated_at = datetime.utcnow()
    else:
        # Create new subscription
        push_sub = PushSubscription(
            user_id=current_user.id,
            endpoint=subscription.endpoint,
            p256dh_key=subscription.p256dh_key,
            auth_key=subscription.auth_key,
            user_agent=subscription.user_agent
        )
        db.add(push_sub)
    
    db.commit()
    
    logger.info("Push subscription created/updated", user_id=str(current_user.id))
    
    return {"message": "Push notifications enabled successfully"}

@router.post("/schedule-reminder")
async def schedule_reminder(
    request: ScheduleReminderRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Schedule a reminder notification"""
    
    # Calculate scheduled time based on user timezone
    import pytz
    user_tz = pytz.timezone(current_user.timezone)
    scheduled_time = request.scheduled_for.replace(tzinfo=user_tz)
    
    # Create notification
    notification = Notification(
        user_id=current_user.id,
        type=request.type,
        title=request.title,
        message=request.message,
        channels=request.channels,
        scheduled_for=scheduled_time,
        timezone=current_user.timezone,
        payload=request.payload
    )
    
    db.add(notification)
    db.commit()
    db.refresh(notification)
    
    logger.info("Reminder scheduled", 
               user_id=str(current_user.id),
               type=request.type,
               scheduled_for=scheduled_time)
    
    return {
        "notification_id": str(notification.id),
        "message": "Reminder scheduled successfully",
        "scheduled_for": scheduled_time
    }

@router.get("/", response_model=List[NotificationResponse])
async def get_notifications(
    skip: int = 0,
    limit: int = 50,
    status_filter: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Get user notifications"""
    
    query = db.query(Notification).filter(Notification.user_id == current_user.id)
    
    if status_filter:
        query = query.filter(Notification.status == status_filter)
    
    notifications = query.order_by(
        Notification.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return [
        NotificationResponse(
            id=str(notif.id),
            type=notif.type,
            title=notif.title,
            message=notif.message,
            status=notif.status,
            scheduled_for=notif.scheduled_for,
            sent_at=notif.sent_at,
            created_at=notif.created_at
        )
        for notif in notifications
    ]

@router.post("/test")
async def test_notification(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Send test notification to verify setup"""
    
    # Get user push subscriptions
    push_subs = db.query(PushSubscription).filter(
        PushSubscription.user_id == current_user.id,
        PushSubscription.is_active == True
    ).all()
    
    user_data = {
        'email': current_user.email,
        'display_name': current_user.display_name,
        'push_subscriptions': [
            {
                'endpoint': sub.endpoint,
                'p256dh_key': sub.p256dh_key,
                'auth_key': sub.auth_key
            }
            for sub in push_subs
        ]
    }
    
    # Send test notification
    results = await notification_service.send_notification(
        user_id=str(current_user.id),
        title="Test Notification",
        message="Your notification system is working correctly!",
        channels=["push", "email"],
        user_data=user_data,
        notification_type="test"
    )
    
    return {
        "message": "Test notification sent",
        "results": results
    }

@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Delete notification"""
    
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    db.delete(notification)
    db.commit()
    
    return {"message": "Notification deleted successfully"}