"""
Simplified analysis endpoints
"""
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
import structlog
import aiofiles
import os

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.session import AnalysisSession
from app.services.depression_classifier import DepressionClassifier
from app.core.config import settings

logger = structlog.get_logger(__name__)
router = APIRouter()

@router.post("/text")
async def analyze_text(
    text: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Analyze text for depression indicators"""
    
    if len(text.strip()) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text must be at least 10 characters long"
        )
    
    try:
        # Create session
        session = AnalysisSession(
            user_id=current_user.id,
            text_input=text,
            status="processing"
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        
        # Analyze text
        classifier = DepressionClassifier()
        result = classifier.analyze_text(text)
        
        # Update session with results
        session.depression_result = result['depression_level']
        session.confidence_score = result['confidence']
        session.detailed_analysis = result
        session.status = "completed"
        session.completed_at = func.now()
        
        db.commit()
        
        logger.info("Text analysis completed", 
                   session_id=session.id,
                   result=result['depression_level'])
        
        return {
            'session_id': session.id,
            'depression_level': result['depression_level'],
            'confidence': result['confidence'],
            'explanation': result['explanation'],
            'stage': _get_depression_stage(result['depression_level']),
            'recommendations': _get_recommendations(result['depression_level'])
        }
        
    except Exception as e:
        logger.error("Text analysis failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )

@router.get("/sessions")
async def get_user_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Get user's analysis history"""
    
    sessions = db.query(AnalysisSession).filter(
        AnalysisSession.user_id == current_user.id
    ).order_by(AnalysisSession.created_at.desc()).limit(20).all()
    
    return {
        'sessions': [
            {
                'id': session.id,
                'depression_level': session.depression_result,
                'confidence': session.confidence_score,
                'created_at': session.created_at,
                'status': session.status
            }
            for session in sessions
        ]
    }

def _get_depression_stage(level: str) -> str:
    """Convert level to stage description"""
    stages = {
        'not_depressed': 'No Depression',
        'mild': 'Mild Depression - Early Stage',
        'moderate': 'Moderate Depression - Intervention Needed',
        'severe': 'Severe Depression - Immediate Support Required'
    }
    return stages.get(level, 'Unknown')

def _get_recommendations(level: str) -> list:
    """Get recommendations based on depression level"""
    
    recommendations = {
        'not_depressed': [
            "Continue with healthy habits and regular self-care",
            "Practice gratitude and maintain social connections",
            "Keep up with regular exercise and good sleep"
        ],
        'mild': [
            "Try daily meditation or mindfulness exercises",
            "Increase physical activity and outdoor time",
            "Consider talking to a counselor if symptoms persist"
        ],
        'moderate': [
            "Schedule an appointment with a mental health professional",
            "Practice stress management techniques daily",
            "Reach out to trusted friends or family for support"
        ],
        'severe': [
            "Seek immediate professional help from a psychiatrist or therapist",
            "Contact crisis support if having thoughts of self-harm",
            "Consider intensive treatment options with professional guidance"
        ]
    }
    
    return recommendations.get(level, ["Consult with a healthcare professional"])