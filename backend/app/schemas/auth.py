"""
Authentication schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
import uuid

class UserBase(BaseModel):
    email: EmailStr
    display_name: Optional[str] = None
    timezone: str = "UTC"

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)
    consent_research: bool = False
    consent_data_sharing: bool = False
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    timezone: Optional[str] = None
    password: Optional[str] = None
    consent_research: Optional[bool] = None
    consent_data_sharing: Optional[bool] = None
    preferences: Optional[dict] = None

class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    display_name: Optional[str]
    timezone: str
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: UserResponse

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[datetime] = None