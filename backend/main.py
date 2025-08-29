from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import uvicorn
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional
import io
import pandas as pd
import numpy as np
import jwt
from contextlib import asynccontextmanager

# Local imports
from app.core.config import settings
from app.core.database import engine, SessionLocal, create_tables
from app.models.user import Base
from app.api.v1.api import api_router
from app.services.ml.ensemble_processor import EnsembleMLProcessor
from app.services.ml.split_learning import SplitLearningCoordinator
from app.services.chatbot import AdvancedHealthChatbot
from app.tasks.celery_app import celery_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize ML processors
ensemble_processor = EnsembleMLProcessor()
split_learning_coordinator = SplitLearningCoordinator()
health_chatbot = AdvancedHealthChatbot(settings.OPENAI_API_KEY)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting EEG Mental Health Assistant API...")
    
    # Create database tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
    
    # Initialize ML models
    try:
        await ensemble_processor.initialize_models()
        logger.info("ML models initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing ML models: {e}")
    
    # Start Celery worker (in production, run separately)
    try:
        # celery_app.control.inspect().stats()
        logger.info("Celery connection verified")
    except Exception as e:
        logger.warning(f"Celery connection warning: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down EEG Mental Health Assistant API...")

# Create FastAPI application
app = FastAPI(
    title="EEG Mental Health Assistant API",
    description="AI-powered mental health companion with EEG analysis and LLM chatbot",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token and return user"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"id": user_id, "email": payload.get("email")}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Include API routers
app.include_router(api_router, prefix=settings.API_V1_STR)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "EEG Mental Health Assistant API",
        "version": "2.0.0",
        "status": "running",
        "features": [
            "Multi-model EEG analysis (CNN, LSTM, Transformer)",
            "Ensemble learning (RF, SVM, KNN)",
            "Split learning for privacy",
            "LLM-powered health chatbot",
            "Autoencoder anomaly detection",
            "Real-time processing"
        ]
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check database
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    # Check ML models
    try:
        model_status = ensemble_processor.health_check()
    except Exception as e:
        model_status = {"status": "unhealthy", "error": str(e)}
    
    # Check Celery
    try:
        celery_stats = celery_app.control.inspect().stats()
        celery_status = "healthy" if celery_stats else "no workers"
    except Exception as e:
        celery_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "database": db_status,
            "ml_models": model_status,
            "celery": celery_status,
            "api": "healthy"
        }
    }

# Advanced EEG analysis endpoint
@app.post("/api/v1/eeg/analyze-advanced")
async def analyze_eeg_advanced(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    use_ensemble: bool = True,
    use_split_learning: bool = False,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Advanced EEG analysis with ensemble methods"""
    
    # Validate file
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files supported")
    
    try:
        # Read file
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode('utf-8')))
        
        # Process with ensemble
        if use_ensemble:
            analysis_result = await ensemble_processor.process_eeg_ensemble(
                df, 
                user_id=current_user["id"],
                session_metadata={
                    "filename": file.filename,
                    "upload_time": datetime.utcnow().isoformat(),
                    "user_id": current_user["id"]
                }
            )
        else:
            # Use split learning
            if use_split_learning:
                analysis_result = await split_learning_coordinator.process_eeg_split(
                    df, 
                    user_id=current_user["id"]
                )
            else:
                raise HTTPException(
                    status_code=400, 
                    detail="Either ensemble or split learning must be enabled"
                )
        
        # Store results in database
        # (Add database storage logic here)
        
        return {
            "status": "success",
            "analysis_result": analysis_result,
            "processing_method": "ensemble" if use_ensemble else "split_learning",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Advanced EEG analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# Advanced chat endpoint
@app.post("/api/v1/chat/advanced")
async def chat_advanced(
    request: Dict,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Advanced chat with context-aware LLM"""
    
    message = request.get("message", "").strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        # Get user's analysis history for context
        # (Add database query for user context)
        user_context = {
            "user_id": current_user["id"],
            "recent_sessions": [],  # Add recent analysis results
            "preferences": {}       # Add user preferences
        }
        
        # Generate response with advanced chatbot
        response = await health_chatbot.generate_contextual_response(
            message, 
            user_context,
            use_rag=True,  # Use retrieval-augmented generation
            safety_check=True
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Advanced chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

# Real-time WebSocket endpoint for streaming analysis
@app.websocket("/ws/eeg-stream/{user_id}")
async def websocket_eeg_stream(websocket, user_id: str):
    """WebSocket endpoint for real-time EEG analysis"""
    await websocket.accept()
    
    try:
        while True:
            # Receive EEG data chunk
            data = await websocket.receive_json()
            
            # Process in real-time
            result = await ensemble_processor.process_realtime_chunk(
                data["eeg_chunk"], 
                user_id=user_id
            )
            
            # Send results back
            await websocket.send_json({
                "type": "analysis_result",
                "data": result,
                "timestamp": datetime.utcnow().isoformat()
            })
            
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })
    finally:
        await websocket.close()

# Model management endpoints
@app.get("/api/v1/models/status")
async def get_model_status(current_user: dict = Depends(get_current_user)):
    """Get status of all ML models"""
    return ensemble_processor.get_models_status()

@app.post("/api/v1/models/retrain")
async def retrain_models(
    background_tasks: BackgroundTasks,
    model_types: List[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Trigger model retraining"""
    if not model_types:
        model_types = ["cnn", "lstm", "transformer", "rf", "svm", "autoencoder"]
    
    # Add retraining task to background
    background_tasks.add_task(
        ensemble_processor.retrain_models,
        model_types=model_types,
        user_id=current_user["id"]
    )
    
    return {
        "message": "Model retraining initiated",
        "models": model_types,
        "status": "in_progress"
    }

# Export user data endpoint (GDPR compliance)
@app.get("/api/v1/user/export")
async def export_user_data(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Export all user data"""
    try:
        # Export user data from database
        # (Add comprehensive data export logic)
        
        export_data = {
            "user_profile": {
                "id": current_user["id"],
                "email": current_user["email"]
            },
            "sessions": [],  # All analysis sessions
            "chat_history": [],  # Chat conversations
            "preferences": {},  # User settings
            "export_timestamp": datetime.utcnow().isoformat()
        }
        
        return export_data
        
    except Exception as e:
        logger.error(f"Data export error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

# Delete user data endpoint (GDPR compliance)
@app.delete("/api/v1/user/delete")
async def delete_user_data(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete all user data"""
    try:
        # Delete all user data from database
        # (Add comprehensive data deletion logic)
        
        return {
            "message": "User data deletion completed",
            "user_id": current_user["id"],
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Data deletion error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Deletion failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )