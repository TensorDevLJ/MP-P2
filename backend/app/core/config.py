"""
Configuration settings for the EEG Mental Health Assistant API
"""
import os
from typing import List, Optional, Any
from pydantic_settings import BaseSettings
from pydantic import Field, validator

class Settings(BaseSettings):
    """Application settings with validation and defaults"""
    
    # Application
    APP_NAME: str = "EEG Mental Health Assistant"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    
    # Security
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    ALGORITHM: str = "HS256"
    
    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    
    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"], 
        env="BACKEND_CORS_ORIGINS"
    )
    
    # Trusted hosts
    ALLOWED_HOSTS: List[str] = Field(
        default=["localhost", "127.0.0.1"], 
        env="ALLOWED_HOSTS"
    )
    
    # File Storage (Local for Render)
    UPLOAD_DIR: str = Field(default="/tmp/uploads", env="UPLOAD_DIR")
    MAX_FILE_SIZE: int = Field(default=50 * 1024 * 1024, env="MAX_FILE_SIZE")  # 50MB
    
    # Free AI APIs
    COHERE_API_KEY: Optional[str] = Field(default=None, env="COHERE_API_KEY")
    GROQ_API_KEY: Optional[str] = Field(default=None, env="GROQ_API_KEY")
    GEMINI_API_KEY: Optional[str] = Field(default=None, env="GEMINI_API_KEY")
    
    # Google Maps
    GOOGLE_MAPS_API_KEY: Optional[str] = Field(default=None, env="GOOGLE_MAPS_API_KEY")
    
    # Notifications
    SENDGRID_API_KEY: Optional[str] = Field(default=None, env="SENDGRID_API_KEY")
    TWILIO_ACCOUNT_SID: Optional[str] = Field(default=None, env="TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN: Optional[str] = Field(default=None, env="TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER: Optional[str] = Field(default=None, env="TWILIO_PHONE_NUMBER")
    
    # Firebase Cloud Messaging
    FCM_SERVER_KEY: Optional[str] = Field(default=None, env="FCM_SERVER_KEY")
    
    # Monitoring
    SENTRY_DSN: Optional[str] = Field(default=None, env="SENTRY_DSN")
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=100, env="RATE_LIMIT_PER_MINUTE")
    
    # ML Model Configuration
    MODEL_BASE_PATH: str = Field(default="ml_models/saved_models", env="MODEL_BASE_PATH")
    EEG_MODEL_PATH: str = Field(default="ml_models/saved_models/eeg_cnn_lstm.pth", env="EEG_MODEL_PATH")
    TEXT_MODEL_PATH: str = Field(default="ml_models/saved_models/roberta_depression", env="TEXT_MODEL_PATH")
    
    # EEG Processing
    DEFAULT_SAMPLING_RATE: int = Field(default=128, env="DEFAULT_SAMPLING_RATE")
    DEFAULT_EPOCH_LENGTH: float = Field(default=2.0, env="DEFAULT_EPOCH_LENGTH")
    DEFAULT_OVERLAP: float = Field(default=0.5, env="DEFAULT_OVERLAP")
    
    # Render specific settings
    PORT: int = Field(default=8000, env="PORT")
    RENDER_EXTERNAL_URL: Optional[str] = Field(default=None, env="RENDER_EXTERNAL_URL")
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Any) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    @validator("ALLOWED_HOSTS", pre=True)
    def assemble_allowed_hosts(cls, v: Any) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()