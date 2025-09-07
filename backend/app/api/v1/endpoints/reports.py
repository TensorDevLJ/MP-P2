"""
Data export and reporting endpoints
"""
import csv
import json
from io import StringIO
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from sqlalchemy.orm import Session
import structlog
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.session import AnalysisSession
from app.schemas.reports import ReportRequest, UserDataExport

logger = structlog.get_logger(__name__)
router = APIRouter()

@router.get("/sessions/export")
async def export_sessions(
    format: str = Query("json", regex="^(json|csv)$"),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Export user's analysis sessions"""
    
    logger.info("Exporting user sessions", 
               user_id=str(current_user.id),
               format=format)
    
    # Build query
    query = db.query(AnalysisSession).filter(
        AnalysisSession.user_id == current_user.id
    )
    
    if start_date:
        query = query.filter(AnalysisSession.created_at >= start_date)
    if end_date:
        query = query.filter(AnalysisSession.created_at <= end_date)
    
    sessions = query.order_by(AnalysisSession.created_at.desc()).all()
    
    # Prepare export data
    export_data = []
    for session in sessions:
        session_data = {
            'session_id': str(session.id),
            'type': session.session_type,
            'created_at': session.created_at.isoformat(),
            'status': session.status,
            'emotion_result': session.emotion_results.get('label') if session.emotion_results else None,
            'anxiety_result': session.anxiety_results.get('label') if session.anxiety_results else None,
            'depression_result': session.depression_results.get('label') if session.depression_results else None,
            'risk_level': session.fusion_results.get('risk_level') if session.fusion_results else None,
            'confidence': session.fusion_results.get('confidence') if session.fusion_results else None
        }
        export_data.append(session_data)
    
    if format == "json":
        return {
            'exported_at': datetime.utcnow().isoformat(),
            'user_id': str(current_user.id),
            'total_sessions': len(export_data),
            'sessions': export_data
        }
    
    elif format == "csv":
        # Generate CSV
        output = StringIO()
        if export_data:
            writer = csv.DictWriter(output, fieldnames=export_data[0].keys())
            writer.writeheader()
            writer.writerows(export_data)
        
        csv_content = output.getvalue()
        output.close()
        
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=sessions_export.csv"}
        )

@router.get("/trends")
async def get_trends_summary(
    days: int = Query(30, ge=7, le=365),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Get trends summary for the past N days"""
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    sessions = db.query(AnalysisSession).filter(
        AnalysisSession.user_id == current_user.id,
        AnalysisSession.created_at >= start_date,
        AnalysisSession.status == "completed"
    ).order_by(AnalysisSession.created_at.asc()).all()
    
    # Prepare trend data
    trend_data = {
        'period_start': start_date.isoformat(),
        'period_end': datetime.utcnow().isoformat(),
        'total_sessions': len(sessions),
        'risk_levels': [],
        'emotions': [],
        'anxiety_levels': [],
        'eeg_features': {'alpha': [], 'beta': [], 'theta': []},
        'weekly_summary': {}
    }
    
    for session in sessions:
        date_str = session.created_at.date().isoformat()
        
        # Risk levels over time
        if session.fusion_results:
            trend_data['risk_levels'].append({
                'date': date_str,
                'level': session.fusion_results.get('risk_level'),
                'confidence': session.fusion_results.get('confidence')
            })
        
        # Emotions over time
        if session.emotion_results:
            trend_data['emotions'].append({
                'date': date_str,
                'emotion': session.emotion_results.get('label'),
                'confidence': session.emotion_results.get('confidence')
            })
        
        # Anxiety levels over time
        if session.anxiety_results:
            trend_data['anxiety_levels'].append({
                'date': date_str,
                'level': session.anxiety_results.get('label'),
                'confidence': session.anxiety_results.get('confidence')
            })
        
        # EEG features over time (if available)
        if session.eeg_features:
            band_powers = session.eeg_features.get('features', {}).get('band_powers', {}).get('mean', {})
            if band_powers:
                for band in ['alpha', 'beta', 'theta']:
                    if band in band_powers:
                        trend_data['eeg_features'][band].append({
                            'date': date_str,
                            'power': band_powers[band]
                        })
    
    # Generate weekly summaries
    from collections import defaultdict
    weekly_data = defaultdict(lambda: {'sessions': 0, 'high_risk': 0, 'total_risk_score': 0})
    
    for session in sessions:
        week_start = session.created_at.date() - timedelta(days=session.created_at.weekday())
        week_key = week_start.isoformat()
        
        weekly_data[week_key]['sessions'] += 1
        
        if session.fusion_results:
            risk_level = session.fusion_results.get('risk_level')
            if risk_level == 'high':
                weekly_data[week_key]['high_risk'] += 1
            
            # Convert risk to numeric score for averaging
            risk_scores = {'stable': 1, 'mild': 2, 'moderate': 3, 'high': 4}
            weekly_data[week_key]['total_risk_score'] += risk_scores.get(risk_level, 1)
    
    # Convert weekly data to summary
    for week, data in weekly_data.items():
        if data['sessions'] > 0:
            avg_risk_score = data['total_risk_score'] / data['sessions']
            trend_data['weekly_summary'][week] = {
                'sessions': data['sessions'],
                'high_risk_sessions': data['high_risk'],
                'avg_risk_score': round(avg_risk_score, 2),
                'risk_percentage': round((data['high_risk'] / data['sessions']) * 100, 1)
            }
    
    return trend_data

@router.get("/user-data-export", response_model=UserDataExport)
async def export_all_user_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Export all user data for GDPR compliance"""
    
    logger.info("Full data export requested", user_id=str(current_user.id))
    
    # Get all user sessions
    sessions = db.query(AnalysisSession).filter(
        AnalysisSession.user_id == current_user.id
    ).all()
    
    # Get all notifications
    notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).all()
    
    # Get push subscriptions
    push_subs = db.query(PushSubscription).filter(
        PushSubscription.user_id == current_user.id
    ).all()
    
    export = UserDataExport(
        user_profile={
            'id': str(current_user.id),
            'email': current_user.email,
            'display_name': current_user.display_name,
            'timezone': current_user.timezone,
            'created_at': current_user.created_at,
            'last_login': current_user.last_login,
            'consent_research': current_user.consent_research,
            'consent_data_sharing': current_user.consent_data_sharing,
            'preferences': current_user.preferences
        },
        analysis_sessions=[
            {
                'id': str(session.id),
                'type': session.session_type,
                'created_at': session.created_at,
                'status': session.status,
                'results': {
                    'emotion': session.emotion_results,
                    'anxiety': session.anxiety_results,
                    'depression': session.depression_results,
                    'fusion': session.fusion_results
                }
            }
            for session in sessions
        ],
        notifications=[
            {
                'id': str(notif.id),
                'type': notif.type,
                'title': notif.title,
                'scheduled_for': notif.scheduled_for,
                'status': notif.status,
                'created_at': notif.created_at
            }
            for notif in notifications
        ],
        export_metadata={
            'exported_at': datetime.utcnow(),
            'export_version': '1.0',
            'total_sessions': len(sessions),
            'account_age_days': (datetime.utcnow() - current_user.created_at).days
        }
    )
    
    return export

@router.delete("/user-data")
async def delete_all_user_data(
    confirmation: str = Query(..., description="Must be 'DELETE_ALL_DATA'"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Delete all user data (GDPR Right to be Forgotten)"""
    
    if confirmation != "DELETE_ALL_DATA":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid confirmation. Must be 'DELETE_ALL_DATA'"
        )
    
    logger.warning("Full data deletion requested", user_id=str(current_user.id))
    
    try:
        # Delete in correct order due to foreign key constraints
        
        # Delete notifications
        db.query(Notification).filter(Notification.user_id == current_user.id).delete()
        
        # Delete push subscriptions
        db.query(PushSubscription).filter(PushSubscription.user_id == current_user.id).delete()
        
        # Delete analysis sessions (cascade will handle text_inputs)
        db.query(AnalysisSession).filter(AnalysisSession.user_id == current_user.id).delete()
        
        # TODO: Delete S3 files in production
        
        # Delete user account
        db.delete(current_user)
        
        db.commit()
        
        logger.info("User data deletion completed", user_id=str(current_user.id))
        
        return {"message": "All user data has been permanently deleted"}
        
    except Exception as e:
        db.rollback()
        logger.error("Data deletion failed", user_id=str(current_user.id), error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Data deletion failed"
        )