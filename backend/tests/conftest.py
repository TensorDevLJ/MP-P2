"""
PyTest configuration and fixtures
"""
import pytest
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient
import tempfile
import os

from app.main import app
from app.core.database import Base, get_db
from app.core.config import settings

# Test database URL
TEST_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
engine = create_engine(
    TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override database dependency
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Set up test database"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Clean up
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test.db"):
        os.unlink("./test.db")

@pytest.fixture
def client():
    """Create test client"""
    return AsyncClient(app=app, base_url="http://test")

@pytest.fixture
def auth_headers():
    """Create authentication headers for testing"""
    # This would be implemented with actual authentication
    # For now, return mock headers
    return {"Authorization": "Bearer test_token"}

@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "display_name": "Test User",
        "timezone": "UTC",
        "consent_research": True,
        "consent_data_sharing": False
    }

@pytest.fixture
def temp_csv_file():
    """Create temporary CSV file for testing uploads"""
    import pandas as pd
    import numpy as np
    
    # Generate synthetic EEG data
    fs = 128
    duration = 5
    t = np.linspace(0, duration, fs * duration)
    signal = np.sin(2 * np.pi * 10 * t) + 0.1 * np.random.randn(len(t))
    
    df = pd.DataFrame({
        'Time': t,
        'EEG.AF3': signal
    })
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        df.to_csv(f.name, index=False)
        temp_file = f.name
    
    yield temp_file
    
    # Cleanup
    if os.path.exists(temp_file):
        os.unlink(temp_file)