"""
Load testing script using Locust for performance testing
"""
from locust import HttpUser, task, between
import json
import random
import uuid

class EEGHealthUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Setup user session"""
        # Register and login
        user_data = {
            "email": f"load_test_{uuid.uuid4().hex[:8]}@example.com",
            "password": "LoadTest123!",
            "display_name": f"Load Test User {random.randint(1, 1000)}",
            "consent_research": random.choice([True, False])
        }
        
        # Register
        response = self.client.post("/api/v1/auth/signup", json=user_data)
        
        if response.status_code == 400:
            # User exists, try login
            pass
        
        # Login
        login_data = {
            "username": user_data["email"],
            "password": user_data["password"]
        }
        
        response = self.client.post("/api/v1/auth/login", data=login_data)
        
        if response.status_code == 200:
            auth_data = response.json()
            self.client.headers.update({
                "Authorization": f"Bearer {auth_data['access_token']}"
            })
        
    @task(3)
    def check_health(self):
        """Test health endpoint"""
        self.client.get("/health")
    
    @task(2)
    def get_user_profile(self):
        """Test user profile retrieval"""
        self.client.get("/api/v1/auth/me")
    
    @task(5) 
    def analyze_text(self):
        """Test text analysis with random samples"""
        
        sample_texts = [
            "Having a great day today, feeling positive and energetic!",
            "Feeling a bit stressed with work deadlines approaching soon.",
            "Not sleeping well lately and feeling quite tired all the time.",
            "Really excited about the weekend plans with friends and family.",
            "Feeling overwhelmed with everything going on right now."
        ]
        
        text = random.choice(sample_texts)
        
        response = self.client.post(
            "/api/v1/text/analyze",
            json={"text": text},
            name="/api/v1/text/analyze"
        )
    
    @task(1)
    def chat_with_bot(self):
        """Test chatbot interactions"""
        
        messages = [
            "Hello, how are you today?",
            "Can you explain what alpha waves mean?", 
            "I'm feeling anxious, what should I do?",
            "What breathing exercises do you recommend?",
            "How can I improve my sleep?"
        ]
        
        message = random.choice(messages)
        
        self.client.post(
            "/api/v1/chat/message", 
            json={"message": message},
            name="/api/v1/chat/message"
        )
    
    @task(1)
    def get_session_history(self):
        """Test session history retrieval"""
        self.client.get("/api/v1/analysis/sessions")
    
    @task(1)
    def get_notifications(self):
        """Test notifications endpoint"""
        self.client.get("/api/v1/notifications/")

# Custom load test scenarios
class HighLoadUser(HttpUser):
    """Simulate high-frequency usage"""
    wait_time = between(0.5, 1)
    
    @task
    def rapid_text_analysis(self):
        texts = [
            "Quick mood check - feeling okay today",
            "Stressed but managing",
            "Good energy this morning"
        ]
        
        self.client.post(
            "/api/v1/text/analyze",
            json={"text": random.choice(texts)}
        )

class ChatBotStressTest(HttpUser):
    """Focus on chatbot performance"""
    wait_time = between(2, 5)
    
    @task
    def chat_conversation(self):
        """Simulate realistic chat conversations"""
        
        conversation_flows = [
            [
                "Hello, I just got my EEG results",
                "Can you explain what they mean?", 
                "What should I do about elevated beta waves?"
            ],
            [
                "I'm feeling anxious today",
                "What breathing exercises can help?",
                "How long should I practice them?"
            ],
            [
                "My sleep has been poor lately",
                "Could this affect my brain patterns?",
                "What sleep hygiene tips do you have?"
            ]
        ]
        
        conversation = random.choice(conversation_flows)
        
        for message in conversation:
            response = self.client.post(
                "/api/v1/chat/message",
                json={"message": message}
            )
            
            if response.status_code == 200:
                # Simulate reading response time
                self.wait()

# Run with: locust -f scripts/load_test.py --host=http://localhost:8000