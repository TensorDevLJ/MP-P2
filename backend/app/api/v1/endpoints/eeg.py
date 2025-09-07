"""
EEG analysis endpoints
"""
from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
import structlog
import uuid

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.session import AnalysisSession
from app.schemas.eeg import EEGUploadResponse, EEGProcessRequest, EEGResultResponse
from app.services.ml.eeg_processor import EEGProcessor
from app.tasks.celery_tasks import process_eeg_file

logger = structlog.get_logger(__name__)
router = APIRouter()

@router.post("/upload", response_model=EEGUploadResponse)
async def upload_eeg_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Upload EEG file and return file key for processing"""
    
    # Validate file type
    if not file.filename.endswith(('.csv', '.txt')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV and TXT files are supported"
        )
    
    # Validate file size (max 50MB)
    if file.size > 50 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size must be less than 50MB"
        )
    
    try:
        # Generate unique file key
        file_key = f"eeg/{current_user.id}/{uuid.uuid4()}/{file.filename}"
        
        # TODO: Upload to S3 in production
        # For now, save locally for development
        import aiofiles
        local_path = f"uploads/{file_key}"
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        async with aiofiles.open(local_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Quick validation and metadata extraction
        processor = EEGProcessor()
        metadata = await processor.extract_metadata(local_path)
        
        logger.info(
            "EEG file uploaded",
            user_id=str(current_user.id),
            file_key=file_key,
            sampling_rate=metadata.get("sampling_rate"),
            channels=metadata.get("channels"),
        )
        
        return EEGUploadResponse(
            file_key=file_key,
            filename=file.filename,
            size_bytes=file.size,
            sampling_rate=metadata.get("sampling_rate"),
            channels=metadata.get("channels", []),
            duration_seconds=metadata.get("duration_seconds"),
        )
        
    except Exception as e:
        logger.error("EEG upload failed", user_id=str(current_user.id), error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to process EEG file: {str(e)}"
        )

@router.post("/process", response_model=dict)
async def process_eeg(
    request: EEGProcessRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Start EEG processing job"""
    
    # Create analysis session
    session = AnalysisSession(
        user_id=current_user.id,
        session_type="eeg",
        file_key=request.file_key,
        sampling_rate=request.sampling_rate,
        channel=request.channel,
        epoch_length=request.epoch_length,
        overlap=request.overlap,
        status="pending"
    )
    
    db.add(session)
    db.commit()
    db.refresh(session)
    
    # Queue background processing
    background_tasks.add_task(
        process_eeg_file,
        session_id=str(session.id),
        file_key=request.file_key,
        user_id=str(current_user.id),
        sampling_rate=request.sampling_rate,
        channel=request.channel,
        epoch_length=request.epoch_length,
        overlap=request.overlap
    )
    
    logger.info(
        "EEG processing queued",
        session_id=str(session.id),
        user_id=str(current_user.id),
        file_key=request.file_key
    )
    
    return {
        "job_id": str(session.id),
        "status": "queued",
        "message": "EEG processing started"
    }

@router.get("/result/{job_id}", response_model=EEGResultResponse)
async def get_eeg_result(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Get EEG processing results"""
    
    # Get session
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
        return EEGResultResponse(
            job_id=job_id,
            status="pending",
            message="Analysis in progress"
        )
    
    if session.status == "failed":
        return EEGResultResponse(
            job_id=job_id,
            status="failed",
            message=session.error_message or "Analysis failed"
        )
    
    # Return completed results
    return EEGResultResponse(
        job_id=job_id,
        status="completed",
        emotion_results=session.emotion_results,
        anxiety_results=session.anxiety_results,
        eeg_features=session.eeg_features,
        explanations=session.explanations,
        processing_time=(
            session.processing_completed_at - session.processing_started_at
        ).total_seconds() if session.processing_completed_at else None,
        charts_data=session.eeg_features.get("charts") if session.eeg_features else None,
    )

@router.delete("/session/{session_id}")
async def delete_eeg_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Delete EEG analysis session and associated data"""
    
    session = db.query(AnalysisSession).filter(
        AnalysisSession.id == session_id,
        AnalysisSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # TODO: Delete S3 files in production
    # Delete from database
    db.delete(session)
    db.commit()
    
    logger.info("EEG session deleted", session_id=session_id, user_id=str(current_user.id))
    
    return {"message": "Session deleted successfully"}