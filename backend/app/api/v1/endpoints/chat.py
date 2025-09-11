"""
Simplified chat endpoints
"""
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import structlog

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.session import AnalysisSession
from app.services.chatbot import HealthChatbot

logger = structlog.get_logger(__name__)
router = APIRouter()

@router.post("/message")
async def send_message(
    message: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Send message to health chatbot"""
    
    if len(message.strip()) < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty"
        )
    
    try:
        # Get user context from recent analysis
        recent_session = db.query(AnalysisSession).filter(
            AnalysisSession.user_id == current_user.id,
            AnalysisSession.status == "completed"
        ).order_by(AnalysisSession.created_at.desc()).first()
        
        user_context = None
        if recent_session:
            user_context = {
                'recent_analysis': {
                    'depression_level': recent_session.depression_result,
                    'confidence': recent_session.confidence_score
                }
            }
        
        # Process message
        chatbot = HealthChatbot()
        response = await chatbot.chat(message, user_context)
        
        return response
        
    except Exception as e:
        logger.error("Chat processing failed", error=str(e))
        return {
            'response': "I'm having technical difficulties. Please try again or contact support.",
            'crisis_detected': False,
            'disclaimer': "This assistant provides supportive information only."
        }