"""
Combined analysis endpoints (EEG + Text fusion)
"""
from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
import structlog

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.session import AnalysisSession, TextInput
from app.schemas.analysis import CombinedAnalysisRequest, CombinedAnalysisResponse
from app.services.ml.fusion_engine import FusionEngine
from app.tasks.celery_tasks import process_combined_analysis

logger = structlog.get_logger(__name__)
router = APIRouter()

@router.post("/combined", response_model=dict)
async def start_combined_analysis(
    request: CombinedAnalysisRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Start combined EEG + Text analysis"""
    
    if not request.file_key and not request.text_input:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either EEG file or text input is required"
        )
    
    # Create combined analysis session
    session = AnalysisSession(
        user_id=current_user.id,
        session_type="combined",
        file_key=request.file_key,
        sampling_rate=request.sampling_rate,
        channel=request.channel,
        epoch_length=request.epoch_length or 2.0,
        overlap=request.overlap or 0.5,
        status="pending"
    )
    
    db.add(session)
    db.commit()
    db.refresh(session)
    
    # Add text input if provided
    if request.text_input:
        import hashlib
        content_hash = hashlib.sha256(request.text_input.encode()).hexdigest()
        
        text_input = TextInput(
            session_id=session.id,
            content=request.text_input,  # TODO: Encrypt in production
            content_hash=content_hash
        )
        db.add(text_input)
        db.commit()
    
    # Queue background processing
    background_tasks.add_task(
        process_combined_analysis,
        session_id=str(session.id),
        user_id=str(current_user.id)
    )
    
    logger.info(
        "Combined analysis queued",
        session_id=str(session.id),
        user_id=str(current_user.id),
        has_eeg=bool(request.file_key),
        has_text=bool(request.text_input)
    )
    
    return {
        "job_id": str(session.id),
        "status": "queued",
        "message": "Combined analysis started"
    }

@router.get("/result/{job_id}", response_model=CombinedAnalysisResponse)
async def get_combined_result(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Get combined analysis results"""
    
    session = db.query(AnalysisSession).filter(
        AnalysisSession.id == job_id,
        AnalysisSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis session not found"
        )
    
    if session.status == "pending":
        return CombinedAnalysisResponse(
            session_id=job_id,
            status="pending",
            message="Analysis in progress"
        )
    
    if session.status == "failed":
        return CombinedAnalysisResponse(
            session_id=job_id,
            status="failed",
            message=session.error_message or "Analysis failed"
        )
    
    # Generate recommendations based on results
    from app.services.recommendations import RecommendationEngine
    recommender = RecommendationEngine()
    recommendations = recommender.generate_recommendations(
        emotion_results=session.emotion_results,
        anxiety_results=session.anxiety_results,
        depression_results=session.depression_results,
        fusion_results=session.fusion_results,
        user_preferences=current_user.preferences
    )
    
    return CombinedAnalysisResponse(
        session_id=job_id,
        status="completed",
        emotion_results=session.emotion_results,
        anxiety_results=session.anxiety_results,
        depression_results=session.depression_results,
        fusion_results=session.fusion_results,
        explanations=session.explanations,
        recommendations=recommendations,
        charts_data=session.eeg_features.get("charts") if session.eeg_features else None,
        processing_time=(
            session.processing_completed_at - session.processing_started_at
        ).total_seconds() if session.processing_completed_at else None,
    )

@router.get("/sessions")
async def get_user_sessions(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Get user's analysis sessions history"""
    
    sessions = db.query(AnalysisSession).filter(
        AnalysisSession.user_id == current_user.id
    ).order_by(
        AnalysisSession.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return {
        "sessions": [
            {
                "id": str(session.id),
                "type": session.session_type,
                "status": session.status,
                "created_at": session.created_at,
                "has_results": bool(session.fusion_results)
            }
            for session in sessions
        ],
        "total": db.query(AnalysisSession).filter(
            AnalysisSession.user_id == current_user.id
        ).count()
    }