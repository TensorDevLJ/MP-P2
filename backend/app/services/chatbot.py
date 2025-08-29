import openai
from typing import Dict, List, Optional
import json
import re
from datetime import datetime
import logging

class HealthChatbot:
    def __init__(self, api_key: str):
        # Configure your preferred LLM API
        # Using OpenAI as example - replace with your preferred provider
        openai.api_key = api_key
        
        self.system_prompt = """
        You are a supportive mental health assistant. You provide empathetic, 
        evidence-based information and support, but you are NOT a replacement 
        for professional medical care.
        
        Key guidelines:
        1. Always be supportive and non-judgmental
        2. Provide helpful information about mental health
        3. NEVER provide medical diagnoses
        4. Encourage professional help when appropriate
        5. If someone mentions self-harm, provide crisis resources immediately
        6. Keep responses concise but caring
        7. Focus on evidence-based coping strategies
        
        Crisis resources:
        - National Suicide Prevention Lifeline: 988 (US)
        - Crisis Text Line: Text HOME to 741741
        - International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/
        """
        
        self.safety_triggers = [
            'suicide', 'kill myself', 'end my life', 'self harm',
            'hurt myself', 'want to die', 'no point living'
        ]
        
        self.conversation_context = []
    
    def generate_response(self, message: str, user_context: Optional[Dict] = None) -> Dict:
        """Generate chatbot response with safety checks"""
        
        # Safety check
        safety_check = self._check_safety(message)
        if safety_check['is_crisis']:
            return safety_check
        
        try:
            # Prepare conversation context
            context = self._prepare_context(message, user_context)
            
            # Generate response using OpenAI API
            # Replace this with your preferred LLM provider
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    *context,
                    {"role": "user", "content": message}
                ],
                max_tokens=300,
                temperature=0.7,
                presence_penalty=0.2,
                frequency_penalty=0.1
            )
            
            bot_response = response.choices[0].message.content.strip()
            
            # Add to conversation context
            self.conversation_context.append({
                "user": message,
                "bot": bot_response,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            # Keep only last 5 exchanges
            if len(self.conversation_context) > 5:
                self.conversation_context.pop(0)
            
            return {
                'response': bot_response,
                'type': 'normal',
                'confidence': 0.8,
                'suggestions': self._generate_suggestions(message)
            }
            
        except Exception as e:
            logging.error(f"Chatbot error: {str(e)}")
            return {
                'response': "I'm sorry, I'm having trouble responding right now. If you're in crisis, please contact a mental health professional or emergency services.",
                'type': 'error',
                'confidence': 0.0
            }
    
    def _check_safety(self, message: str) -> Dict:
        """Check for crisis indicators"""
        message_lower = message.lower()
        
        for trigger in self.safety_triggers:
            if trigger in message_lower:
                return {
                    'response': """I'm very concerned about what you've shared. Your life has value and there are people who want to help.
                    
🚨 **Immediate Help:**
- National Suicide Prevention Lifeline: 988
- Crisis Text Line: Text HOME to 741741
- Emergency Services: 911
                    
Please reach out to one of these resources right now. You don't have to go through this alone.""",
                    'type': 'crisis',
                    'is_crisis': True,
                    'confidence': 1.0,
                    'requires_followup': True
                }
        
        return {'is_crisis': False}
    
    def _prepare_context(self, message: str, user_context: Optional[Dict]) -> List[Dict]:
        """Prepare conversation context for LLM"""
        context = []
        
        # Add user context if available
        if user_context:
            risk_level = user_context.get('risk_level', 'unknown')
            recent_analysis = user_context.get('recent_analysis', {})
            
            context_message = f"User context: Current risk level is {risk_level}."
            if recent_analysis:
                context_message += f" Recent analysis shows: {json.dumps(recent_analysis)}"
            
            context.append({
                "role": "system", 
                "content": context_message
            })
        
        # Add recent conversation history
        for exchange in self.conversation_context[-3:]:  # Last 3 exchanges
            context.extend([
                {"role": "user", "content": exchange["user"]},
                {"role": "assistant", "content": exchange["bot"]}
            ])
        
        return context
    
    def _generate_suggestions(self, message: str) -> List[str]:
        """Generate follow-up suggestions"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['anxious', 'anxiety', 'worry', 'nervous']):
            return [
                "Tell me about breathing exercises",
                "How to manage anxiety at work?",
                "What are grounding techniques?"
            ]
        elif any(word in message_lower for word in ['sad', 'depressed', 'down', 'hopeless']):
            return [
                "What helps with depression?",
                "How to build a daily routine?",
                "Tell me about mood tracking"
            ]
        elif any(word in message_lower for word in ['sleep', 'insomnia', 'tired']):
            return [
                "Sleep hygiene tips please",
                "How does sleep affect mood?",
                "Relaxation techniques for bedtime"
            ]
        else:
            return [
                "How can I improve my mood?",
                "What are healthy coping strategies?",
                "Tell me about stress management"
            ]

# Example usage in endpoint:
"""
# In your FastAPI endpoint:
@app.post("/chat")
async def chat_endpoint(request: ChatRequest, current_user = Depends(get_current_user)):
    chatbot = HealthChatbot(settings.OPENAI_API_KEY)
    
    # Get user context from recent analysis
    user_context = {
        'risk_level': 'moderate',  # from recent analysis
        'recent_analysis': {...}   # recent results
    }
    
    response = chatbot.generate_response(request.message, user_context)
    
    # Save chat log to database
    # ... save logic here
    
    return response
"""