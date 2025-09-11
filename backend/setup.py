"""
Setup script for the simplified EEG Mental Health Assistant
"""
import os
import sqlite3
from pathlib import Path

def setup_database():
    """Initialize SQLite database"""
    print("Setting up database...")
    
    # Create database file
    db_path = "eeg_health.db"
    
    # Create tables using SQLAlchemy
    from app.core.database import create_tables
    create_tables()
    
    print(f"✅ Database created at {db_path}")

def setup_directories():
    """Create necessary directories"""
    print("Creating directories...")
    
    directories = [
        "uploads",
        "models", 
        "logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created {directory}/")

def main():
    """Main setup function"""
    print("🧠 EEG Mental Health Assistant - Setup")
    print("=" * 40)
    
    # Setup directories
    setup_directories()
    
    # Setup database
    setup_database()
    
    print("\n🎉 Setup completed!")
    print("\nNext steps:")
    print("1. Add your API keys to .env file")
    print("2. Run: python run.py")
    print("3. Visit: http://localhost:8000")

if __name__ == "__main__":
    main()