"""
Background tasks for ML processing using Celery
"""
from celery import Celery
from sqlalchemy.orm import Session
from datetime import datetime
import structlog
import traceback

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.session import AnalysisSession
from app.services.ml.eeg_processor import EEGProcessor
from app.services.ml.text_classifier import TextClassifier
from app.services.ml.fusion_engine import FusionEngine
from app.services.ml.eeg_cnn_lstm import EEGModelInference

logger = structlog.get_logger(__name__)

# Initialize Celery
celery_app = Celery(
    "eeg_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_time_limit=300,  # 5 minutes max per task
    task_soft_time_limit=240,  # 4 minutes soft limit
)

def process_eeg_file(
    session_id: str,
    file_key: str,
    user_id: str,
    sampling_rate: int = 128,
    channel: str = "EEG.AF3",
    epoch_length: float = 2.0,
    overlap: float = 0.5
):
    """Background task to process EEG file"""
    
    db = SessionLocal()
    
    try:
        logger.info("Starting EEG processing task", 
                   session_id=session_id, 
                   file_key=file_key)
        
        # Update session status
        session = db.query(AnalysisSession).filter(
            AnalysisSession.id == session_id
        ).first()
        
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.status = "processing"
        session.processing_started_at = datetime.utcnow()
        db.commit()
        
        # Process EEG data
        processor = EEGProcessor(sampling_rate=sampling_rate)
        
        # Convert file_key to local path for development
        file_path = f"uploads/{file_key}"
        
        eeg_results = await processor.process_eeg_data(
            file_path=file_path,
            channel=channel,
            epoch_length=epoch_length,
            overlap=overlap
        )
        
        # Run EEG model inference
        model_inference = EEGModelInference(settings.EEG_MODEL_PATH)
        predictions = model_inference.predict(eeg_results['features'])
        
        # Update session with results
        session.emotion_results = predictions['emotion']
        session.anxiety_results = predictions['anxiety']
        session.eeg_features = eeg_results
        session.eeg_model_version = predictions.get('model_version', '1.0.0')
        
        # Generate explanations
        explanations = _generate_eeg_explanations(eeg_results, predictions)
        session.explanations = explanations
        
        session.status = "completed"
        session.processing_completed_at = datetime.utcnow()
        db.commit()
        
        logger.info("EEG processing completed", session_id=session_id)
        
    except Exception as e:
        logger.error("EEG processing failed", 
                    session_id=session_id, 
                    error=str(e),
                    traceback=traceback.format_exc())
        
        # Update session with error
        session.status = "failed"
        session.error_message = str(e)
        session.processing_completed_at = datetime.utcnow()
        db.commit()
        
    finally:
        db.close()

def process_combined_analysis(session_id: str, user_id: str):
    """Background task for combined EEG + Text analysis"""
    
    db = SessionLocal()
    
    try:
        logger.info("Starting combined analysis", session_id=session_id)
        
        # Get session
        session = db.query(AnalysisSession).filter(
            AnalysisSession.id == session_id
        ).first()
        
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.status = "processing"
        session.processing_started_at = datetime.utcnow()
        db.commit()
        
        eeg_results = None
        text_results = None
        
        # Process EEG if file provided
        if session.file_key:
            processor = EEGProcessor(sampling_rate=session.sampling_rate or 128)
            file_path = f"uploads/{session.file_key}"
            
            eeg_data = await processor.process_eeg_data(
                file_path=file_path,
                channel=session.channel or "EEG.AF3",
                epoch_length=session.epoch_length,
                overlap=session.overlap
            )
            
            # Run EEG model
            model_inference = EEGModelInference(settings.EEG_MODEL_PATH)
            eeg_results = model_inference.predict(eeg_data['features'])
            
            # Store EEG features for charts
            session.eeg_features = eeg_data
        
        # Process text if provided
        text_inputs = session.text_inputs
        if text_inputs:
            text_classifier = TextClassifier()
            text_analysis = text_classifier.analyze_text(text_inputs[0].content)
            text_results = text_analysis
        
        # Fusion
        fusion_engine = FusionEngine()
        fusion_results = fusion_engine.fuse_predictions(eeg_results, text_results)
        
        # Update session with all results
        session.emotion_results = eeg_results.get('emotion') if eeg_results else None
        session.anxiety_results = eeg_results.get('anxiety') if eeg_results else None
        session.depression_results = text_results.get('depression') if text_results else None
        session.fusion_results = fusion_results
        
        # Generate comprehensive explanations
        explanations = _generate_combined_explanations(eeg_results, text_results, fusion_results)
        session.explanations = explanations
        
        session.status = "completed"
        session.processing_completed_at = datetime.utcnow()
        db.commit()
        
        logger.info("Combined analysis completed", session_id=session_id)
        
    except Exception as e:
        logger.error("Combined analysis failed",
                    session_id=session_id,
                    error=str(e),
                    traceback=traceback.format_exc())
        
        session.status = "failed"
        session.error_message = str(e)
        session.processing_completed_at = datetime.utcnow()
        db.commit()
        
    finally:
        db.close()

def _generate_eeg_explanations(eeg_data: Dict[str, Any], predictions: Dict[str, Any]) -> List[str]:
    """Generate natural language explanations for EEG results"""
    
    explanations = []
    
    # Band power explanations
    features = eeg_data.get('features', {})
    band_powers = features.get('band_powers', {}).get('mean', {})
    
    if band_powers:
        alpha_power = band_powers.get('alpha', 0)
        beta_power = band_powers.get('beta', 0)
        
        if alpha_power > beta_power:
            explanations.append(
                f"Alpha waves ({alpha_power:.2f}) are higher than beta waves ({beta_power:.2f}), "
                "suggesting a more relaxed mental state."
            )
        else:
            explanations.append(
                f"Beta waves ({beta_power:.2f}) are elevated compared to alpha ({alpha_power:.2f}), "
                "which may indicate active thinking or mild stress."
            )
    
    # Emotion explanation
    emotion = predictions.get('emotion', {})
    if emotion:
        explanations.append(
            f"EEG patterns suggest a {emotion.get('label')} emotional state "
            f"with {emotion.get('confidence', 0)*100:.0f}% confidence."
        )
    
    return explanations

def _generate_combined_explanations(
    eeg_results: Optional[Dict[str, Any]],
    text_results: Optional[Dict[str, Any]], 
    fusion_results: Dict[str, Any]
) -> List[str]:
    """Generate explanations for combined analysis"""
    
    explanations = []
    
    if fusion_results.get('safety_override'):
        explanations.extend(fusion_results.get('explanation', []))
        return explanations
    
    # Combined findings
    risk_level = fusion_results.get('risk_level', 'stable')
    explanations.append(
        f"Combined analysis indicates a {risk_level} risk level "
        f"with {fusion_results.get('confidence', 0)*100:.0f}% confidence."
    )
    
    # Agreement between modalities
    if eeg_results and text_results:
        emotion_fusion = fusion_results.get('emotion_fusion', {})
        anxiety_fusion = fusion_results.get('anxiety_fusion', {})
        
        if emotion_fusion.get('agreement') and anxiety_fusion.get('agreement'):
            explanations.append("EEG signals and text analysis show consistent findings.")
        else:
            explanations.append("Some differences detected between EEG and text analyses.")
    
    # Specific findings
    if text_results:
        depression = text_results.get('depression', {})
        if depression.get('label') != 'not_depressed':
            explanations.append(
                f"Text analysis suggests {depression.get('label')} depression indicators."
            )
    
    return explanations

# Utility function for async tasks
async def process_eeg_file_async(*args, **kwargs):
    """Async wrapper for EEG processing"""
    return process_eeg_file(*args, **kwargs)

async def process_combined_analysis_async(*args, **kwargs):
    """Async wrapper for combined analysis"""
    return process_combined_analysis(*args, **kwargs)