"""
Chatbot endpoints for health Q&A
"""
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import structlog

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.session import AnalysisSession
from app.services.chatbot import HealthChatbot
from app.schemas.chat import ChatRequest, ChatResponse

logger = structlog.get_logger(__name__)
router = APIRouter()

# Initialize chatbot
chatbot = HealthChatbot()

@router.post("/message", response_model=ChatResponse)
async def send_chat_message(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Send message to health chatbot"""
    
    logger.info("Chat message received", 
               user_id=str(current_user.id),
               message_length=len(request.message))
    
    try:
        # Get user context from recent analyses
        user_context = await _get_user_context(current_user.id, db)
        
        # Process chat message
        response = await chatbot.chat(
            message=request.message,
            user_context=user_context,
            session_id=request.session_id
        )
        
        return ChatResponse(
            response=response['response'],
            crisis_detected=response.get('crisis_detected', False),
            emergency_resources=response.get('emergency_resources', False),
            disclaimer=response['disclaimer'],
            suggestions=_generate_follow_up_suggestions(request.message, response)
        )
        
    except Exception as e:
        logger.error("Chat processing failed", 
                    user_id=str(current_user.id), 
                    error=str(e))
        
        return ChatResponse(
            response="I'm experiencing technical difficulties. Please try again or contact support.",
            error=True,
            disclaimer="This assistant provides supportive information only."
        )

@router.post("/explain-results")
async def explain_analysis_results(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Get chatbot explanation of analysis results"""
    
    # Get analysis session
    session = db.query(AnalysisSession).filter(
        AnalysisSession.id == session_id,
        AnalysisSession.user_id == current_user.id
    ).first()
    
    if not session or session.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Completed analysis session not found"
        )
    
    # Prepare analysis results
    analysis_results = {
        'risk_level': session.fusion_results.get('risk_level') if session.fusion_results else 'unknown',
        'emotion_fusion': session.emotion_results,
        'anxiety_fusion': session.anxiety_results,
        'depression_results': session.depression_results
    }
    
    # Generate explanation
    explanation = chatbot.get_explanation_for_results(analysis_results)
    
    return {
        'explanation': explanation,
        'session_id': session_id,
        'disclaimer': chatbot._get_disclaimer()
    }

async def _get_user_context(user_id: str, db: Session) -> Dict[str, Any]:
    """Get user context from recent analyses"""
    
    # Get most recent completed analysis
    recent_session = db.query(AnalysisSession).filter(
        AnalysisSession.user_id == user_id,
        AnalysisSession.status == "completed"
    ).order_by(AnalysisSession.created_at.desc()).first()
    
    if recent_session and recent_session.fusion_results:
        return {
            'recent_analysis': {
                'risk_level': recent_session.fusion_results.get('risk_level'),
                'session_date': recent_session.created_at.isoformat(),
                'has_eeg': bool(recent_session.file_key),
                'has_text': bool(recent_session.text_inputs)
            }
        }
    
    return {}

def _generate_follow_up_suggestions(message: str, response: Dict[str, Any]) -> List[str]:
    """Generate contextual follow-up suggestions"""
    
    suggestions = []
    
    message_lower = message.lower()
    
    if 'eeg' in message_lower or 'analysis' in message_lower:
        suggestions.extend([
            "Can you explain my EEG results in simple terms?",
            "What do the different brain wave patterns mean?",
            "How can I improve my mental wellness?"
        ])
    
    elif any(word in message_lower for word in ['anxious', 'anxiety', 'stressed']):
        suggestions.extend([
            "What breathing exercises can help with anxiety?",
            "How can I manage stress better?",
            "When should I consider professional help?"
        ])
    
    elif any(word in message_lower for word in ['sad', 'depressed', 'down']):
        suggestions.extend([
            "What self-care activities might help?",
            "How do I know if I need professional support?",
            "What are signs of depression to watch for?"
        ])
    
    else:
        suggestions.extend([
            "Tell me about my recent analysis results",
            "What wellness activities do you recommend?",
            "How can I track my mental health progress?"
        ])
    
    return suggestions[:3]  # Return top 3 suggestions