"""
Database migration script for EEG Mental Health Assistant
"""
import sys
import os
from pathlib import Path

# Add backend to Python path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.exc import SQLAlchemyError
import structlog
from app.core.config import settings
from app.core.database import Base, engine
from app.models import user, session, notification, provider

logger = structlog.get_logger(__name__)

def create_all_tables():
    """Create all database tables"""
    
    try:
        logger.info("Creating database tables...")
        
        # Import all models to register them
        from app.models.user import User
        from app.models.session import AnalysisSession, TextInput
        from app.models.notification import Notification, PushSubscription
        from app.models.provider import HealthcareProvider, UserProviderBookmark
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        logger.info("Database tables created successfully")
        
        # Verify tables exist
        with engine.connect() as conn:
            result = conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'"))
            tables = [row[0] for row in result]
            
        logger.info(f"Created tables: {', '.join(tables)}")
        
    except SQLAlchemyError as e:
        logger.error(f"Database migration failed: {str(e)}")
        raise

def create_indexes():
    """Create additional indexes for performance"""
    
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);",
        "CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);",
        "CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON analysis_sessions(user_id);",
        "CREATE INDEX IF NOT EXISTS idx_sessions_created_at ON analysis_sessions(created_at);",
        "CREATE INDEX IF NOT EXISTS idx_sessions_status ON analysis_sessions(status);",
        "CREATE INDEX IF NOT EXISTS idx_text_inputs_session_id ON text_inputs(session_id);",
        "CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);",
        "CREATE INDEX IF NOT EXISTS idx_notifications_scheduled_for ON notifications(scheduled_for);",
        "CREATE INDEX IF NOT EXISTS idx_notifications_status ON notifications(status);",
        "CREATE INDEX IF NOT EXISTS idx_providers_location ON healthcare_providers USING gist(ll_to_earth(latitude, longitude));",
        "CREATE INDEX IF NOT EXISTS idx_providers_specialty ON healthcare_providers(specialty);",
    ]
    
    try:
        with engine.connect() as conn:
            for index_sql in indexes:
                try:
                    conn.execute(text(index_sql))
                    logger.info(f"Index created: {index_sql.split('idx_')[1].split(' ')[0] if 'idx_' in index_sql else 'unknown'}")
                except Exception as e:
                    logger.warning(f"Index creation failed or already exists: {str(e)}")
            
            conn.commit()
        
        logger.info("Database indexes created successfully")
        
    except SQLAlchemyError as e:
        logger.error(f"Index creation failed: {str(e)}")
        raise

def setup_row_level_security():
    """Set up row level security policies"""
    
    rls_policies = [
        # Users table - users can only access their own data
        "ALTER TABLE users ENABLE ROW LEVEL SECURITY;",
        """CREATE POLICY users_own_data ON users 
           FOR ALL TO eeg_user 
           USING (id = COALESCE(current_setting('app.current_user_id', true)::uuid, '00000000-0000-0000-0000-000000000000'));""",
        
        # Analysis sessions - users can only access their own sessions
        "ALTER TABLE analysis_sessions ENABLE ROW LEVEL SECURITY;",
        """CREATE POLICY sessions_own_data ON analysis_sessions 
           FOR ALL TO eeg_user 
           USING (user_id = COALESCE(current_setting('app.current_user_id', true)::uuid, '00000000-0000-0000-0000-000000000000'));""",
        
        # Text inputs - accessible through session ownership
        "ALTER TABLE text_inputs ENABLE ROW LEVEL SECURITY;",
        """CREATE POLICY text_inputs_own_data ON text_inputs 
           FOR ALL TO eeg_user 
           USING (session_id IN (
               SELECT id FROM analysis_sessions 
               WHERE user_id = COALESCE(current_setting('app.current_user_id', true)::uuid, '00000000-0000-0000-0000-000000000000')
           ));""",
        
        # Notifications - users can only access their own notifications
        "ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;",
        """CREATE POLICY notifications_own_data ON notifications 
           FOR ALL TO eeg_user 
           USING (user_id = COALESCE(current_setting('app.current_user_id', true)::uuid, '00000000-0000-0000-0000-000000000000'));""",
        
        # Push subscriptions - users can only access their own subscriptions
        "ALTER TABLE push_subscriptions ENABLE ROW LEVEL SECURITY;",
        """CREATE POLICY push_subscriptions_own_data ON push_subscriptions 
           FOR ALL TO eeg_user 
           USING (user_id = COALESCE(current_setting('app.current_user_id', true)::uuid, '00000000-0000-0000-0000-000000000000'));""",
        
        # Healthcare providers - publicly readable for discovery
        "ALTER TABLE healthcare_providers ENABLE ROW LEVEL SECURITY;",
        """CREATE POLICY healthcare_providers_public_read ON healthcare_providers 
           FOR SELECT TO eeg_user 
           USING (true);""",
        
        # User provider bookmarks - users can only access their own bookmarks
        "ALTER TABLE user_provider_bookmarks ENABLE ROW LEVEL SECURITY;",
        """CREATE POLICY bookmarks_own_data ON user_provider_bookmarks 
           FOR ALL TO eeg_user 
           USING (user_id = COALESCE(current_setting('app.current_user_id', true)::uuid, '00000000-0000-0000-0000-000000000000'));""",
    ]
    
    try:
        with engine.connect() as conn:
            for policy_sql in rls_policies:
                try:
                    conn.execute(text(policy_sql))
                except Exception as e:
                    if "already exists" not in str(e).lower():
                        logger.warning(f"RLS policy creation failed: {str(e)}")
            
            conn.commit()
        
        logger.info("Row Level Security policies configured")
        
    except SQLAlchemyError as e:
        logger.error(f"RLS setup failed: {str(e)}")
        raise

def main():
    """Run all migration steps"""
    
    logger.info("Starting database migration...")
    
    try:
        # Create all tables
        create_all_tables()
        
        # Create performance indexes
        create_indexes()
        
        # Set up security policies
        setup_row_level_security()
        
        logger.info("Database migration completed successfully!")
        
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()