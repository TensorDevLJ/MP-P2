"""
Data seeding script for development and testing
"""
import sys
import os
from pathlib import Path
import asyncio
from datetime import datetime, timedelta
import uuid

# Add backend to Python path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.core.security import get_password_hash
from app.models.user import User
from app.models.session import AnalysisSession, TextInput
from app.models.notification import Notification
from app.models.provider import HealthcareProvider
import structlog

logger = structlog.get_logger(__name__)

def create_sample_users():
    """Create sample users for testing"""
    
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        logger.info("Creating sample users...")
        
        # Test user 1
        user1 = User(
            email="test@example.com",
            password_hash=get_password_hash("password123"),
            display_name="Test User",
            timezone="America/New_York",
            is_verified=True,
            consent_research=True,
            consent_data_sharing=False
        )
        
        # Test user 2
        user2 = User(
            email="demo@example.com",
            password_hash=get_password_hash("demo123"),
            display_name="Demo User",
            timezone="Europe/London",
            is_verified=True,
            consent_research=False,
            consent_data_sharing=True
        )
        
        db.add(user1)
        db.add(user2)
        db.commit()
        db.refresh(user1)
        db.refresh(user2)
        
        logger.info(f"Created sample users: {user1.email}, {user2.email}")
        
        return [user1, user2]
        
    except Exception as e:
        logger.error(f"Failed to create sample users: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

def create_sample_sessions(users):
    """Create sample analysis sessions"""
    
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        logger.info("Creating sample analysis sessions...")
        
        sessions_data = [
            {
                'user': users[0],
                'session_type': 'combined',
                'emotion_results': {
                    'label': 'stressed',
                    'probabilities': {'stressed': 0.75, 'neutral': 0.15, 'happy': 0.10},
                    'confidence': 0.75
                },
                'anxiety_results': {
                    'label': 'moderate',
                    'probabilities': {'moderate': 0.65, 'high': 0.25, 'low': 0.10},
                    'confidence': 0.65
                },
                'fusion_results': {
                    'risk_level': 'moderate',
                    'confidence': 0.70
                },
                'status': 'completed'
            },
            {
                'user': users[0],
                'session_type': 'text',
                'depression_results': {
                    'label': 'moderate',
                    'probabilities': {'moderate': 0.60, 'severe': 0.25, 'not_depressed': 0.15},
                    'confidence': 0.60
                },
                'fusion_results': {
                    'risk_level': 'mild',
                    'confidence': 0.55
                },
                'status': 'completed'
            },
            {
                'user': users[1],
                'session_type': 'eeg',
                'emotion_results': {
                    'label': 'relaxed',
                    'probabilities': {'relaxed': 0.80, 'neutral': 0.15, 'happy': 0.05},
                    'confidence': 0.80
                },
                'anxiety_results': {
                    'label': 'low',
                    'probabilities': {'low': 0.85, 'moderate': 0.10, 'high': 0.05},
                    'confidence': 0.85
                },
                'fusion_results': {
                    'risk_level': 'stable',
                    'confidence': 0.82
                },
                'status': 'completed'
            }
        ]
        
        created_sessions = []
        for session_data in sessions_data:
            session = AnalysisSession(
                user_id=session_data['user'].id,
                session_type=session_data['session_type'],
                emotion_results=session_data.get('emotion_results'),
                anxiety_results=session_data.get('anxiety_results'),
                depression_results=session_data.get('depression_results'),
                fusion_results=session_data['fusion_results'],
                status=session_data['status'],
                processing_completed_at=datetime.utcnow() - timedelta(hours=1)
            )
            
            db.add(session)
            created_sessions.append(session)
        
        db.commit()
        
        # Add sample text inputs
        for session in created_sessions[:2]:  # First two sessions have text
            text_content = {
                'combined': "I've been feeling quite stressed lately with work pressure. Having trouble sleeping and feeling anxious about upcoming deadlines.",
                'text': "Feeling down and unmotivated recently. Things that used to bring me joy don't seem as appealing anymore."
            }.get(session.session_type, "Sample text input")
            
            text_input = TextInput(
                session_id=session.id,
                content=text_content,
                content_hash=f"hash_{session.id}",
                sentiment_score=0.3 if 'down' in text_content else 0.6,
                depression_score=0.6 if session.session_type == 'text' else 0.3
            )
            db.add(text_input)
        
        db.commit()
        
        logger.info(f"Created {len(created_sessions)} sample analysis sessions")
        
        return created_sessions
        
    except Exception as e:
        logger.error(f"Failed to create sample sessions: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

def create_sample_providers():
    """Create sample healthcare providers for testing"""
    
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        logger.info("Creating sample healthcare providers...")
        
        providers_data = [
            {
                'google_place_id': 'sample_place_1',
                'name': 'MindCare Psychiatry',
                'specialty': 'psychiatrist',
                'latitude': 37.7749,
                'longitude': -122.4194,
                'address': '123 Mental Health St, San Francisco, CA 94102',
                'phone': '+1-555-0123',
                'website': 'https://mindcare.example.com',
                'rating': 4.8,
                'user_ratings_total': 124,
                'price_level': 3
            },
            {
                'google_place_id': 'sample_place_2',
                'name': 'Wellness Psychology Center',
                'specialty': 'psychologist',
                'latitude': 37.7849,
                'longitude': -122.4094,
                'address': '456 Therapy Ave, San Francisco, CA 94103',
                'phone': '+1-555-0124',
                'rating': 4.6,
                'user_ratings_total': 89,
                'price_level': 2
            },
            {
                'google_place_id': 'sample_place_3',
                'name': 'Holistic Counseling Services',
                'specialty': 'therapist',
                'latitude': 37.7649,
                'longitude': -122.4294,
                'address': '789 Healing Blvd, San Francisco, CA 94104',
                'phone': '+1-555-0125',
                'website': 'https://holistic-counseling.example.com',
                'rating': 4.9,
                'user_ratings_total': 67,
                'price_level': 2
            }
        ]
        
        for provider_data in providers_data:
            provider = HealthcareProvider(**provider_data)
            db.add(provider)
        
        db.commit()
        
        logger.info(f"Created {len(providers_data)} sample healthcare providers")
        
    except Exception as e:
        logger.error(f"Failed to create sample providers: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

def create_sample_notifications(users):
    """Create sample notifications for testing"""
    
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        logger.info("Creating sample notifications...")
        
        notifications_data = [
            {
                'user': users[0],
                'type': 'reminder',
                'title': 'Daily Check-in Reminder',
                'message': 'Time for your daily mental health check-in. How are you feeling today?',
                'scheduled_for': datetime.utcnow() + timedelta(hours=1),
                'channels': ['push', 'email']
            },
            {
                'user': users[0],
                'type': 'recommendation',
                'title': 'Breathing Exercise',
                'message': 'Based on your recent analysis, try a 5-minute breathing exercise to help with stress.',
                'scheduled_for': datetime.utcnow() + timedelta(hours=2),
                'channels': ['push']
            },
            {
                'user': users[1],
                'type': 'follow_up',
                'title': 'Weekly Progress Update',
                'message': 'Your mental wellness journey this week shows positive trends. Keep up the good work!',
                'scheduled_for': datetime.utcnow() + timedelta(days=1),
                'channels': ['email']
            }
        ]
        
        for notif_data in notifications_data:
            notification = Notification(
                user_id=notif_data['user'].id,
                type=notif_data['type'],
                title=notif_data['title'],
                message=notif_data['message'],
                scheduled_for=notif_data['scheduled_for'],
                timezone=notif_data['user'].timezone,
                channels=notif_data['channels']
            )
            db.add(notification)
        
        db.commit()
        
        logger.info(f"Created {len(notifications_data)} sample notifications")
        
    except Exception as e:
        logger.error(f"Failed to create sample notifications: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

def main():
    """Main seeding function"""
    
    logger.info("Starting database seeding...")
    
    try:
        # Create sample users
        users = create_sample_users()
        
        # Create sample analysis sessions
        sessions = create_sample_sessions(users)
        
        # Create sample providers
        create_sample_providers()
        
        # Create sample notifications
        create_sample_notifications(users)
        
        logger.info("Database seeding completed successfully!")
        
        print("\nSample data created:")
        print(f"  👥 Users: {len(users)}")
        print(f"  📊 Analysis Sessions: {len(sessions)}")
        print(f"  🏥 Healthcare Providers: 3")
        print(f"  🔔 Notifications: 3")
        print("\nLogin credentials:")
        print("  Email: test@example.com, Password: password123")
        print("  Email: demo@example.com, Password: demo123")
        
    except Exception as e:
        logger.error(f"Database seeding failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()