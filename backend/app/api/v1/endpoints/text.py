"""
Text analysis endpoints for depression severity assessment
"""
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import structlog

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.session import AnalysisSession, TextInput
from app.schemas.text import TextAnalysisRequest, TextAnalysisResponse
from app.services.ml.text_classifier import TextClassifier

logger = structlog.get_logger(__name__)
router = APIRouter()

@router.post("/analyze", response_model=TextAnalysisResponse)
async def analyze_text(
    request: TextAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Analyze text for depression, anxiety, and sentiment indicators"""
    
    logger.info("Text analysis requested", 
               user_id=str(current_user.id),
               text_length=len(request.text))
    
    try:
        # Create session for text-only analysis
        session = AnalysisSession(
            user_id=current_user.id,
            session_type="text",
            status="processing"
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        
        # Store text input
        import hashlib
        content_hash = hashlib.sha256(request.text.encode()).hexdigest()
        
        text_input = TextInput(
            session_id=session.id,
            content=request.text,  # TODO: Encrypt in production
            content_hash=content_hash
        )
        db.add(text_input)
        
        # Initialize text classifier
        text_classifier = TextClassifier()
        
        # Analyze text
        results = text_classifier.analyze_text(request.text)
        
        # Update session with results
        session.depression_results = results['depression']
        session.status = "completed"
        session.processing_completed_at = datetime.utcnow()
        
        # Store text analysis results
        text_input.sentiment_score = results['sentiment']['score']
        text_input.depression_score = results['depression']['probabilities'].get('severe', 0)
        text_input.anxiety_keywords = results['anxiety_keywords']
        text_input.safety_flags = results['safety_flags']
        
        db.commit()
        
        logger.info("Text analysis completed", 
                   session_id=str(session.id),
                   depression_label=results['depression']['label'])
        
        return TextAnalysisResponse(
            session_id=str(session.id),
            depression_analysis=results['depression'],
            sentiment_analysis=results['sentiment'],
            anxiety_keywords=results['anxiety_keywords'],
            safety_flags=results['safety_flags'],
            text_statistics=results['text_stats'],
            recommendations=_generate_text_recommendations(results)
        )
        
    except Exception as e:
        logger.error("Text analysis failed", 
                    user_id=str(current_user.id),
                    error=str(e))
        
        # Update session status
        if 'session' in locals():
            session.status = "failed"
            session.error_message = str(e)
            db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Text analysis failed: {str(e)}"
        )

@router.get("/history")
async def get_text_analysis_history(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Get user's text analysis history"""
    
    sessions = db.query(AnalysisSession).filter(
        AnalysisSession.user_id == current_user.id,
        AnalysisSession.session_type == "text"
    ).order_by(
        AnalysisSession.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    history = []
    for session in sessions:
        if session.text_inputs:
            text_input = session.text_inputs[0]
            history.append({
                'session_id': str(session.id),
                'created_at': session.created_at,
                'depression_label': session.depression_results.get('label') if session.depression_results else None,
                'sentiment_score': text_input.sentiment_score,
                'word_count': len(text_input.content.split()) if text_input.content else 0,
                'safety_flags': text_input.safety_flags
            })
    
    return {
        'history': history,
        'total': db.query(AnalysisSession).filter(
            AnalysisSession.user_id == current_user.id,
            AnalysisSession.session_type == "text"
        ).count()
    }

def _generate_text_recommendations(analysis_results: Dict[str, Any]) -> List[Dict[str, str]]:
    """Generate immediate recommendations based on text analysis"""
    
    recommendations = []
    
    # Safety-first recommendations
    if analysis_results['safety_flags']['has_crisis_indicators']:
        recommendations.extend([
            {
                'title': 'Immediate Support',
                'description': 'Please reach out to a mental health professional or crisis hotline immediately',
                'urgency': 'critical',
                'action': 'seek_help'
            },
            {
                'title': 'Emergency Resources',
                'description': 'Call 988 (US) or your local emergency services',
                'urgency': 'critical',
                'action': 'emergency'
            }
        ])
        return recommendations
    
    # Depression-based recommendations
    depression_label = analysis_results['depression']['label']
    if depression_label == 'severe':
        recommendations.append({
            'title': 'Professional Support',
            'description': 'Consider scheduling an appointment with a mental health professional',
            'urgency': 'high',
            'action': 'find_providers'
        })
    elif depression_label == 'moderate':
        recommendations.append({
            'title': 'Self-Care Focus',
            'description': 'Try daily mood tracking and gentle self-care activities',
            'urgency': 'medium',
            'action': 'self_care'
        })
    
    # Anxiety-based recommendations
    anxiety_level = analysis_results['anxiety_keywords']['level']
    if anxiety_level == 'high':
        recommendations.append({
            'title': 'Breathing Exercise',
            'description': '5-minute box breathing can help reduce immediate anxiety',
            'urgency': 'medium',
            'action': 'breathing_exercise'
        })
    
    # General wellness
    if not recommendations:
        recommendations.append({
            'title': 'Mindful Check-in',
            'description': 'Continue regular self-reflection and maintain healthy habits',
            'urgency': 'low',
            'action': 'maintain_wellness'
        })
    
    return recommendations