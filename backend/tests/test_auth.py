"""
Authentication endpoint tests
"""
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_user_signup():
    """Test user registration"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        user_data = {
            "email": "test@example.com",
            "password": "TestPassword123!",
            "display_name": "Test User",
            "consent_research": True
        }
        
        response = await client.post("/api/v1/auth/signup", json=user_data)
        
        # Should succeed or fail if user exists
        assert response.status_code in [200, 400]
        
        if response.status_code == 200:
            data = response.json()
            assert data["email"] == user_data["email"]
            assert "id" in data

@pytest.mark.asyncio
async def test_user_login():
    """Test user login"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First, ensure user exists
        await client.post("/api/v1/auth/signup", json={
            "email": "login_test@example.com",
            "password": "TestPassword123!",
            "display_name": "Login Test"
        })
        
        # Test login
        login_data = {
            "username": "login_test@example.com",
            "password": "TestPassword123!"
        }
        
        response = await client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_invalid_credentials():
    """Test login with invalid credentials"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        login_data = {
            "username": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        
        response = await client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 401

@pytest.mark.asyncio
async def test_protected_endpoint():
    """Test accessing protected endpoint without auth"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/auth/me")
        assert response.status_code == 401