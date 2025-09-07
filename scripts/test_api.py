#!/usr/bin/env python3
"""
Comprehensive API testing script for EEG Mental Health Assistant
"""
import requests
import json
import time
import os
from datetime import datetime
import uuid

# Configuration
BASE_URL = "http://localhost:8000"
TEST_USER = {
    "email": "api_test@example.com",
    "password": "TestPassword123!",
    "display_name": "API Test User"
}

class APITester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.auth_token = None
        
    def test_health_check(self):
        """Test basic connectivity"""
        print("🔍 Testing health check...")
        
        response = self.session.get(f"{self.base_url}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        
        print("✅ Health check passed")
        return data
    
    def test_authentication(self):
        """Test user registration and login"""
        print("🔐 Testing authentication...")
        
        # Try to register new user
        signup_data = {
            **TEST_USER,
            "consent_research": True,
            "consent_data_sharing": False
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/auth/signup",
            json=signup_data
        )
        
        # User might already exist from previous tests
        if response.status_code == 400 and "already registered" in response.text:
            print("📝 User already exists, proceeding with login...")
        elif response.status_code == 200:
            print("📝 User registration successful")
        else:
            raise Exception(f"Signup failed: {response.text}")
        
        # Login
        login_data = {
            "username": TEST_USER["email"],
            "password": TEST_USER["password"]
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/auth/login",
            data=login_data  # OAuth2PasswordRequestForm expects form data
        )
        
        assert response.status_code == 200
        auth_data = response.json()
        
        self.auth_token = auth_data["access_token"]
        self.session.headers.update({
            "Authorization": f"Bearer {self.auth_token}"
        })
        
        print("✅ Authentication successful")
        return auth_data
    
    def test_text_analysis(self):
        """Test text analysis endpoint"""
        print("📝 Testing text analysis...")
        
        sample_texts = [
            {
                "text": "I'm feeling really good today! Had a great workout and feeling positive about life.",
                "expected_sentiment": "positive"
            },
            {
                "text": "Been feeling down lately. Not much motivation and sleeping too much. Nothing seems fun anymore.",
                "expected_depression": "moderate"
            },
            {
                "text": "Feeling anxious about the presentation tomorrow. Heart racing and can't focus on anything else.",
                "expected_anxiety": "moderate"
            }
        ]
        
        results = []
        
        for sample in sample_texts:
            response = self.session.post(
                f"{self.base_url}/api/v1/text/analyze",
                json={"text": sample["text"]}
            )
            
            assert response.status_code == 200
            result = response.json()
            
            # Verify response structure
            assert "depression_analysis" in result
            assert "sentiment_analysis" in result
            assert "safety_flags" in result
            
            results.append(result)
            print(f"  📊 Analyzed: '{sample['text'][:50]}...'")
            print(f"      Depression: {result['depression_analysis']['label']}")
            print(f"      Sentiment: {result['sentiment_analysis']['label']}")
        
        print("✅ Text analysis tests passed")
        return results
    
    def test_eeg_upload_simulation(self):
        """Test EEG upload with synthetic data"""
        print("🧠 Testing EEG upload (synthetic data)...")
        
        # Generate synthetic EEG CSV data
        import numpy as np
        import pandas as pd
        
        # Create 30 seconds of synthetic EEG at 128 Hz
        fs = 128
        duration = 30
        t = np.linspace(0, duration, fs * duration)
        
        # Generate realistic EEG-like signal
        eeg_data = (
            0.5 * np.sin(2 * np.pi * 10 * t) +      # Alpha
            0.3 * np.sin(2 * np.pi * 6 * t) +       # Theta  
            0.2 * np.sin(2 * np.pi * 20 * t) +      # Beta
            0.1 * np.random.randn(len(t))           # Noise
        )
        
        # Create DataFrame
        df = pd.DataFrame({
            'Time': t,
            'EEG.AF3': eeg_data,
            'EEG.F7': eeg_data + 0.1 * np.random.randn(len(t)),
            'EEG.F3': eeg_data + 0.05 * np.random.randn(len(t))
        })
        
        # Save to temporary CSV
        csv_file = f"/tmp/test_eeg_{uuid.uuid4().hex[:8]}.csv"
        df.to_csv(csv_file, index=False)
        
        # Upload file
        with open(csv_file, 'rb') as f:
            files = {'file': ('test_eeg.csv', f, 'text/csv')}
            response = self.session.post(
                f"{self.base_url}/api/v1/eeg/upload",
                files=files
            )
        
        # Clean up
        os.unlink(csv_file)
        
        assert response.status_code == 200
        upload_result = response.json()
        
        assert "file_key" in upload_result
        assert upload_result["sampling_rate"] == fs
        assert "EEG.AF3" in upload_result["channels"]
        
        print("✅ EEG upload successful")
        print(f"  📁 File key: {upload_result['file_key']}")
        print(f"  📊 Sampling rate: {upload_result['sampling_rate']} Hz")
        print(f"  🎛️ Channels: {', '.join(upload_result['channels'])}")
        
        return upload_result
    
    def test_eeg_processing(self, file_key):
        """Test EEG processing pipeline"""
        print("⚙️ Testing EEG processing...")
        
        # Start processing
        process_request = {
            "file_key": file_key,
            "sampling_rate": 128,
            "channel": "EEG.AF3",
            "epoch_length": 2.0,
            "overlap": 0.5
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/eeg/process",
            json=process_request
        )
        
        assert response.status_code == 200
        process_result = response.json()
        job_id = process_result["job_id"]
        
        print(f"  🔄 Processing started: {job_id}")
        
        # Poll for results
        max_attempts = 30  # 30 seconds max
        for attempt in range(max_attempts):
            response = self.session.get(f"{self.base_url}/api/v1/eeg/result/{job_id}")
            assert response.status_code == 200
            
            result = response.json()
            
            if result["status"] == "completed":
                print("✅ EEG processing completed")
                
                # Verify result structure
                assert "emotion_results" in result
                assert "anxiety_results" in result
                assert "eeg_features" in result
                
                print(f"  😊 Emotion: {result['emotion_results']['label']}")
                print(f"  😰 Anxiety: {result['anxiety_results']['label']}")
                
                return result
            
            elif result["status"] == "failed":
                raise Exception(f"EEG processing failed: {result.get('message', 'Unknown error')}")
            
            time.sleep(1)
        
        raise Exception("EEG processing timeout")
    
    def test_combined_analysis(self, file_key):
        """Test combined EEG + text analysis"""
        print("🔗 Testing combined analysis...")
        
        combined_request = {
            "file_key": file_key,
            "text_input": "Feeling quite stressed today with work deadlines approaching. Having trouble concentrating and feeling overwhelmed.",
            "sampling_rate": 128,
            "channel": "EEG.AF3"
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/analysis/combined",
            json=combined_request
        )
        
        assert response.status_code == 200
        process_result = response.json()
        job_id = process_result["job_id"]
        
        # Poll for results
        for attempt in range(30):
            response = self.session.get(
                f"{self.base_url}/api/v1/analysis/result/{job_id}"
            )
            assert response.status_code == 200
            
            result = response.json()
            
            if result["status"] == "completed":
                print("✅ Combined analysis completed")
                
                # Verify fusion results
                assert "fusion_results" in result
                assert "recommendations" in result
                
                fusion = result["fusion_results"]
                print(f"  ⚖️ Risk Level: {fusion.get('risk_level', 'unknown')}")
                print(f"  🎯 Confidence: {fusion.get('confidence', 0):.2f}")
                print(f"  💡 Recommendations: {len(result.get('recommendations', []))}")
                
                return result
            
            elif result["status"] == "failed":
                raise Exception(f"Combined analysis failed: {result.get('message')}")
            
            time.sleep(1)
        
        raise Exception("Combined analysis timeout")
    
    def test_chatbot(self):
        """Test chatbot functionality"""
        print("🤖 Testing chatbot...")
        
        test_messages = [
            "Hello, can you help me understand my EEG results?",
            "I'm feeling anxious, what breathing exercises do you recommend?",
            "What do elevated beta waves mean for my mental state?"
        ]
        
        responses = []
        
        for message in test_messages:
            response = self.session.post(
                f"{self.base_url}/api/v1/chat/message",
                json={"message": message}
            )
            
            assert response.status_code == 200
            chat_result = response.json()
            
            assert "response" in chat_result
            assert "disclaimer" in chat_result
            assert len(chat_result["response"]) > 10  # Meaningful response
            
            responses.append(chat_result)
            print(f"  💬 Q: {message}")
            print(f"     A: {chat_result['response'][:100]}...")
        
        print("✅ Chatbot tests passed")
        return responses
    
    def test_notifications(self):
        """Test notification system"""
        print("🔔 Testing notifications...")
        
        # Schedule a test reminder
        reminder_request = {
            "type": "test_reminder",
            "title": "API Test Reminder",
            "message": "This is a test reminder from the API testing script",
            "scheduled_for": (datetime.utcnow() + timedelta(minutes=1)).isoformat(),
            "channels": ["push"]
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/notifications/schedule-reminder",
            json=reminder_request
        )
        
        assert response.status_code == 200
        schedule_result = response.json()
        
        assert "notification_id" in schedule_result
        
        # Get notifications list
        response = self.session.get(f"{self.base_url}/api/v1/notifications/")
        assert response.status_code == 200
        
        notifications = response.json()
        assert len(notifications) >= 1
        
        print("✅ Notification tests passed")
        return schedule_result
    
    def test_user_profile(self):
        """Test user profile management"""
        print("👤 Testing user profile...")
        
        # Get current profile
        response = self.session.get(f"{self.base_url}/api/v1/auth/me")
        assert response.status_code == 200
        
        profile = response.json()
        original_name = profile["display_name"]
        
        # Update profile
        update_data = {
            "display_name": f"{original_name} (Updated)",
            "timezone": "America/Los_Angeles"
        }
        
        response = self.session.put(
            f"{self.base_url}/api/v1/auth/me",
            json=update_data
        )
        
        assert response.status_code == 200
        updated_profile = response.json()
        
        assert updated_profile["display_name"] == update_data["display_name"]
        assert updated_profile["timezone"] == update_data["timezone"]
        
        print("✅ User profile tests passed")
        return updated_profile

def run_comprehensive_test():
    """Run all API tests"""
    
    print("🧠 EEG Mental Health Assistant - API Test Suite")
    print("=" * 60)
    
    tester = APITester(BASE_URL)
    
    try:
        # Basic connectivity
        health_data = tester.test_health_check()
        
        # Authentication flow
        auth_data = tester.test_authentication()
        
        # User profile management
        profile_data = tester.test_user_profile()
        
        # Text analysis
        text_results = tester.test_text_analysis()
        
        # EEG upload and processing
        upload_result = tester.test_eeg_upload_simulation()
        eeg_result = tester.test_eeg_processing(upload_result["file_key"])
        
        # Combined analysis
        combined_result = tester.test_combined_analysis(upload_result["file_key"])
        
        # Chatbot
        chat_results = tester.test_chatbot()
        
        # Notifications
        notification_result = tester.test_notifications()
        
        # Summary
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
        
        print(f"✅ Health Check: {health_data['status']}")
        print(f"✅ Authentication: Token obtained")
        print(f"✅ Text Analysis: {len(text_results)} samples processed")
        print(f"✅ EEG Processing: Emotion={eeg_result['emotion_results']['label']}")
        print(f"✅ Combined Analysis: Risk={combined_result['fusion_results']['risk_level']}")
        print(f"✅ Chatbot: {len(chat_results)} conversations")
        print(f"✅ Notifications: Scheduled successfully")
        
        print("\n📊 Test Summary:")
        print(f"   Total API calls: ~{15 + len(text_results) + len(chat_results)}")
        print(f"   Authentication: Working")
        print(f"   ML Pipeline: Functional") 
        print(f"   Safety Systems: Active")
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    exit(0 if success else 1)