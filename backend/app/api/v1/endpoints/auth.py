"""
Authentication endpoints
"""
from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import structlog

from app.core.config import settings
from app.core.database import get_db
from app.core.security import (
    verify_password, 
    get_password_hash, 
    create_access_token,
    get_current_user,
    generate_secure_token
)
from app.models.user import User
from app.schemas.auth import UserCreate, UserResponse, Token, UserUpdate

logger = structlog.get_logger(__name__)
router = APIRouter()

@router.post("/signup", response_model=UserResponse)
async def create_user(
    user_create: UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    """Create new user account"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_create.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_create.password)
    verification_token = generate_secure_token()
    
    db_user = User(
        email=user_create.email,
        password_hash=hashed_password,
        display_name=user_create.display_name,
        timezone=user_create.timezone,
        verification_token=verification_token,
        consent_research=user_create.consent_research,
        consent_data_sharing=user_create.consent_data_sharing,
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    logger.info("User created", user_id=str(db_user.id), email=db_user.email)
    
    return UserResponse(
        id=db_user.id,
        email=db_user.email,
        display_name=db_user.display_name,
        timezone=db_user.timezone,
        is_verified=db_user.is_verified,
        created_at=db_user.created_at
    )

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Any:
    """OAuth2 compatible token login"""
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )
    
    # Update last login
    user.last_login = func.now()
    db.commit()
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, 
        expires_delta=access_token_expires
    )
    
    logger.info("User logged in", user_id=str(user.id), email=user.email)
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse(
            id=user.id,
            email=user.email,
            display_name=user.display_name,
            timezone=user.timezone,
            is_verified=user.is_verified,
            created_at=user.created_at
        )
    )

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get current user profile"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        display_name=current_user.display_name,
        timezone=current_user.timezone,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at
    )

@router.put("/me", response_model=UserResponse)
async def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Update current user profile"""
    for field, value in user_update.dict(exclude_unset=True).items():
        if field == "password" and value:
            current_user.password_hash = get_password_hash(value)
        else:
            setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    logger.info("User profile updated", user_id=str(current_user.id))
    
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        display_name=current_user.display_name,
        timezone=current_user.timezone,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at
    )

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)) -> Any:
    """Logout user (client should delete token)"""
    logger.info("User logged out", user_id=str(current_user.id))
    return {"message": "Successfully logged out"}