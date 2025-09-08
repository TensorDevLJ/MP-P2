"""
Advanced fusion analysis endpoints
"""
from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
import structlog

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.session import AnalysisSession
from app.services.ml.fusion_engine import AdvancedFusionEngine
from app.services.ml.explainability import generate_comprehensive_explanation

logger = structlog.get_logger(__name__)
router = APIRouter()

@router.post("/analyze")
async def fusion_analysis(
    session_id: str,
    fusion_method: str = "attention",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Run advanced fusion analysis on existing session"""
    
    # Get session
    session = db.query(AnalysisSession).filter(
        AnalysisSession.id == session_id,
        AnalysisSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis session not found"
        )
    
    if session.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session must be completed before fusion analysis"
        )
    
    try:
        # Initialize advanced fusion engine
        fusion_engine = AdvancedFusionEngine()
        
        # Prepare results for fusion
        eeg_results = {
            'emotion': session.emotion_results,
            'anxiety': session.anxiety_results
        } if session.emotion_results else None
        
        text_results = None
        if session.text_inputs:
            # Get text analysis results from session
            text_input = session.text_inputs[0]
            text_results = {
                'depression': session.depression_results,
                'sentiment': {'label': 'neutral', 'score': text_input.sentiment_score or 0.5},
                'anxiety_keywords': text_input.anxiety_keywords or {},
                'safety_flags': text_input.safety_flags or {}
            }
        
        # Run advanced fusion
        fusion_results = fusion_engine.fuse_predictions(
            eeg_results=eeg_results,
            text_results=text_results,
            fusion_method=fusion_method
        )
        
        # Update session with fusion results
        session.fusion_results = fusion_results
        db.commit()
        
        logger.info("Advanced fusion analysis completed", 
                   session_id=session_id,
                   method=fusion_method,
                   risk_level=fusion_results.get('risk_level'))
        
        return {
            'session_id': session_id,
            'fusion_method': fusion_method,
            'results': fusion_results,
            'status': 'completed'
        }
        
    except Exception as e:
        logger.error("Fusion analysis failed", 
                    session_id=session_id, 
                    error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fusion analysis failed: {str(e)}"
        )

@router.get("/explain/{session_id}")
async def get_fusion_explanation(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Get comprehensive explanation of fusion results"""
    
    # Get session
    session = db.query(AnalysisSession).filter(
        AnalysisSession.id == session_id,
        AnalysisSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis session not found"
        )
    
    try:
        # Prepare data for explanation
        eeg_results = {
            'emotion': session.emotion_results,
            'anxiety': session.anxiety_results
        } if session.emotion_results else None
        
        text_results = None
        text_data = None
        if session.text_inputs:
            text_input = session.text_inputs[0]
            text_data = text_input.content
            text_results = {
                'depression': session.depression_results,
                'sentiment': {'label': 'neutral', 'score': text_input.sentiment_score or 0.5}
            }
        
        # Generate comprehensive explanation
        explanations = await generate_comprehensive_explanation(
            eeg_results=eeg_results,
            text_results=text_results,
            fusion_results=session.fusion_results,
            text_data=text_data
        )
        
        return {
            'session_id': session_id,
            'explanations': explanations,
            'risk_level': session.fusion_results.get('risk_level') if session.fusion_results else 'unknown'
        }
        
    except Exception as e:
        logger.error("Explanation generation failed", 
                    session_id=session_id, 
                    error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Explanation generation failed: {str(e)}"
        )

@router.get("/methods")
async def get_fusion_methods() -> Any:
    """Get available fusion methods and their descriptions"""
    
    return {
        'methods': [
            {
                'name': 'attention',
                'display_name': 'Attention Fusion',
                'description': 'Uses learned attention weights to combine EEG and text predictions',
                'best_for': 'Balanced analysis with confidence-based weighting'
            },
            {
                'name': 'bayesian',
                'display_name': 'Bayesian Fusion',
                'description': 'Combines predictions using Bayesian inference with population priors',
                'best_for': 'Conservative analysis incorporating population statistics'
            },
            {
                'name': 'ensemble',
                'display_name': 'Ensemble Fusion',
                'description': 'Combines multiple fusion methods for robust predictions',
                'best_for': 'Maximum accuracy when computational resources allow'
            }
        ],
        'default_method': 'attention',
        'recommended_method': 'ensemble'
    }

@router.post("/calibrate")
async def calibrate_fusion_weights(
    session_ids: list[str],
    target_outcomes: list[str],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Calibrate fusion weights based on user feedback"""
    
    if len(session_ids) != len(target_outcomes):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Number of sessions and outcomes must match"
        )
    
    try:
        # Get user sessions
        sessions = db.query(AnalysisSession).filter(
            AnalysisSession.id.in_(session_ids),
            AnalysisSession.user_id == current_user.id
        ).all()
        
        if len(sessions) != len(session_ids):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Some sessions not found"
            )
        
        # Simple calibration (in practice, use more sophisticated methods)
        calibration_data = []
        for session, outcome in zip(sessions, target_outcomes):
            if session.fusion_results:
                predicted = session.fusion_results.get('risk_level', 'stable')
                calibration_data.append({
                    'predicted': predicted,
                    'actual': outcome,
                    'eeg_confidence': session.emotion_results.get('confidence', 0.5) if session.emotion_results else 0.5,
                    'text_confidence': 0.7 if session.text_inputs else 0.5
                })
        
        # Calculate new weights (simplified)
        eeg_accuracy = sum(1 for d in calibration_data if d['predicted'] == d['actual'] and d['eeg_confidence'] > 0.6) / len(calibration_data)
        text_accuracy = sum(1 for d in calibration_data if d['predicted'] == d['actual'] and d['text_confidence'] > 0.6) / len(calibration_data)
        
        # Normalize weights
        total_accuracy = eeg_accuracy + text_accuracy
        if total_accuracy > 0:
            new_weights = {
                'eeg_weight': eeg_accuracy / total_accuracy,
                'text_weight': text_accuracy / total_accuracy
            }
        else:
            new_weights = {'eeg_weight': 0.6, 'text_weight': 0.4}
        
        # Store calibration in user preferences
        if not current_user.preferences:
            current_user.preferences = {}
        
        current_user.preferences['fusion_calibration'] = new_weights
        current_user.preferences['calibration_sessions'] = len(calibration_data)
        
        db.commit()
        
        logger.info("Fusion weights calibrated", 
                   user_id=str(current_user.id),
                   sessions_used=len(calibration_data),
                   new_weights=new_weights)
        
        return {
            'message': 'Fusion weights calibrated successfully',
            'new_weights': new_weights,
            'sessions_used': len(calibration_data),
            'accuracy_improvement': 'Weights optimized based on your feedback'
        }
        
    except Exception as e:
        logger.error("Calibration failed", 
                    user_id=str(current_user.id), 
                    error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Calibration failed: {str(e)}"
        )