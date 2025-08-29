from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional
import uuid
import pandas as pd
import json
from datetime import datetime

from app.api import deps
from app.models.user import User, Session as DBSession
from app.schemas.analysis import (
    EEGUploadResponse, 
    AnalysisRequest, 
    AnalysisResponse,
    TextAnalysisRequest,
    CombinedAnalysisRequest
)
from app.services.ml.eeg_processor import EEGProcessor, EEGModelInference
from app.services.ml.text_classifier import TextAnalyzer
from app.services.ml.fusion_engine import FusionEngine
from app.core.config import settings
import app.tasks.celery_tasks as tasks

router = APIRouter()

@router.post("/eeg/upload", response_model=EEGUploadResponse)
async def upload_eeg_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Upload and validate EEG CSV file"""
    
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    # Check file size (max 50MB)
    if file.size > 50 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 50MB)")
    
    try:
        # Read and validate CSV
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode('utf-8')))
        
        # Validate EEG data
        processor = EEGProcessor()
        validation_result = processor.validate_eeg_data(df)
        
        if not validation_result['valid']:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid EEG data: {'; '.join(validation_result['messages'])}"
            )
        
        # Generate unique file key
        file_key = f"eeg_{current_user.id}_{uuid.uuid4()}.csv"
        
        # Save file to storage (implement your storage logic)
        # For demo, we'll process directly
        
        # Create session record
        session = DBSession(
            user_id=current_user.id,
            file_key=file_key,
            sampling_rate=validation_result['detected_sr'],
            channels=','.join(validation_result['channels']),
            started_at=datetime.utcnow()
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        
        # Queue processing task
        task = tasks.process_eeg_file.delay(
            str(session.id), 
            content.decode('utf-8'),
            validation_result['detected_sr']
        )
        
        return EEGUploadResponse(
            session_id=str(session.id),
            file_key=file_key,
            task_id=task.id,
            validation=validation_result,
            estimated_time=30  # seconds
        )
        
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="Empty or invalid CSV file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/eeg/result/{session_id}")
async def get_eeg_result(
    session_id: str,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Get EEG analysis results"""
    
    # Get session
    session = db.query(DBSession).filter(
        DBSession.id == session_id,
        DBSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if not session.completed_at:
        return {
            "status": "processing",
            "message": "Analysis in progress..."
        }
    
    return {
        "status": "completed",
        "session_id": session_id,
        "results": {
            "emotion": session.emotion_result,
            "anxiety": session.anxiety_result,
            "explanation": session.explanation,
            "charts": {
                "bands": f"/api/v1/charts/bands/{session_id}",
                "spectrogram": f"/api/v1/charts/spectrogram/{session_id}"
            }
        }
    }

@router.post("/text/analyze")
async def analyze_text(
    request: TextAnalysisRequest,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Analyze text for depression and anxiety indicators"""
    
    if not request.text or len(request.text.strip()) < 5:
        raise HTTPException(status_code=400, detail="Text too short for analysis")
    
    try:
        # Analyze text
        analyzer = TextAnalyzer()
        results = analyzer.analyze_text(request.text)
        
        # Create session record for text analysis
        session = DBSession(
            user_id=current_user.id,
            text_input=request.text,
            depression_result=results.get('depression'),
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow()
        )
        db.add(session)
        db.commit()
        
        return {
            "session_id": str(session.id),
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text analysis failed: {str(e)}")

@router.post("/combined", response_model=AnalysisResponse)
async def combined_analysis(
    request: CombinedAnalysisRequest,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Perform combined EEG and text analysis"""
    
    eeg_results = None
    text_results = None
    
    try:
        # Get EEG results if session provided
        if request.eeg_session_id:
            eeg_session = db.query(DBSession).filter(
                DBSession.id == request.eeg_session_id,
                DBSession.user_id == current_user.id
            ).first()
            
            if eeg_session and eeg_session.completed_at:
                eeg_results = {
                    'emotion': eeg_session.emotion_result,
                    'anxiety': eeg_session.anxiety_result
                }
        
        # Analyze text if provided
        if request.text:
            analyzer = TextAnalyzer()
            text_results = analyzer.analyze_text(request.text)
        
        if not eeg_results and not text_results:
            raise HTTPException(
                status_code=400, 
                detail="No valid EEG session or text provided"
            )
        
        # Perform fusion analysis
        fusion_engine = FusionEngine()
        fusion_results = fusion_engine.fuse_predictions(
            eeg_results or {}, 
            text_results
        )
        
        # Create combined session record
        session = DBSession(
            user_id=current_user.id,
            text_input=request.text,
            emotion_result=eeg_results.get('emotion') if eeg_results else None,
            anxiety_result=eeg_results.get('anxiety') if eeg_results else None,
            depression_result=text_results.get('depression') if text_results else None,
            fusion_result=fusion_results,
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow()
        )
        db.add(session)
        db.commit()
        
        return AnalysisResponse(
            session_id=str(session.id),
            fusion_results=fusion_results,
            eeg_results=eeg_results,
            text_results=text_results,
            recommendations=fusion_results.get('recommendations', []),
            next_actions=fusion_results.get('next_actions', [])
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Combined analysis failed: {str(e)}")

@router.post("/chat")
async def chat_with_assistant(
    request: dict,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Chat with health assistant"""
    
    message = request.get('message', '').strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        # Get user's latest analysis for context
        latest_session = db.query(DBSession).filter(
            DBSession.user_id == current_user.id,
            DBSession.completed_at.isnot(None)
        ).order_by(DBSession.completed_at.desc()).first()
        
        user_context = None
        if latest_session and latest_session.fusion_result:
            user_context = {
                'risk_level': latest_session.fusion_result.get('risk_level'),
                'recent_analysis': latest_session.fusion_result
            }
        
        # Initialize chatbot (you'll need to implement this based on your LLM choice)
        from app.services.chatbot import HealthChatbot
        chatbot = HealthChatbot(settings.OPENAI_API_KEY)  # Replace with your API key
        
        response = chatbot.generate_response(message, user_context)
        
        # Log conversation (optional)
        # You can store chat history in database if needed
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")