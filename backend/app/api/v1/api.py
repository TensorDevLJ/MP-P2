"""
API v1 router aggregating all endpoints
"""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, eeg, text, analysis, chat, care, notifications, reports

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(eeg.router, prefix="/eeg", tags=["eeg-analysis"])
api_router.include_router(text.router, prefix="/text", tags=["text-analysis"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["combined-analysis"])
api_router.include_router(chat.router, prefix="/chat", tags=["chatbot"])
api_router.include_router(care.router, prefix="/care", tags=["healthcare-providers"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports-export"])