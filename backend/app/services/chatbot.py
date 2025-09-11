"""
Simple chatbot using free AI APIs
"""
import google.generativeai as genai
import cohere
from typing import Dict, Any, Optional
import structlog

from app.core.config import settings

logger = structlog.get_logger(__name__)

class HealthChatbot:
    """Simple health chatbot using free APIs"""
    
    def __init__(self):
        # Initialize free API clients
        self.gemini_model = None
        self.cohere_client = None
        
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel('gemini-pro')
        
        if settings.COHERE_API_KEY:
            self.cohere_client = cohere.Client(settings.COHERE_API_KEY)
        
        # Crisis keywords
        self.crisis_keywords = [
            'suicide', 'kill myself', 'end my life', 'hurt myself', 'self harm'
        ]
        
        self.system_prompt = """You are a supportive mental health assistant. Provide helpful, empathetic responses about mental wellness, but always remind users that you're not a replacement for professional medical care. 

If someone mentions self-harm or suicide, immediately provide crisis resources:
- National Suicide Prevention Lifeline: 988
- Crisis Text Line: Text HOME to 741741
- Emergency Services: 911

Keep responses supportive, informative, and under 200 words."""
    
    async def chat(self, message: str, user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Process chat message"""
        
        logger.info("Processing chat message", message_length=len(message))
        
        # Check for crisis indicators
        message_lower = message.lower()
        crisis_detected = any(keyword in message_lower for keyword in self.crisis_keywords)
        
        if crisis_detected:
            return {
                'response': self._get_crisis_response(),
                'crisis_detected': True,
                'disclaimer': "This is not a substitute for emergency services."
            }
        
        # Generate response using AI
        try:
            response = await self._generate_response(message, user_context)
            return {
                'response': response,
                'crisis_detected': False,
                'disclaimer': "This assistant provides supportive information only and is not a substitute for professional medical advice."
            }
        except Exception as e:
            logger.error("Chat generation failed", error=str(e))
            return {
                'response': self._get_fallback_response(message),
                'crisis_detected': False,
                'disclaimer': "This assistant provides supportive information only."
            }
    
    async def _generate_response(self, message: str, context: Optional[Dict]) -> str:
        """Generate response using AI APIs"""
        
        # Build context-aware prompt
        context_info = ""
        if context and context.get('recent_analysis'):
            level = context['recent_analysis'].get('depression_level', 'unknown')
            context_info = f"\nUser's recent analysis shows {level} depression level. "
        
        full_prompt = f"{self.system_prompt}\n{context_info}\nUser: {message}\nAssistant:"
        
        # Try Gemini first
        if self.gemini_model:
            try:
                response = self.gemini_model.generate_content(full_prompt)
                return response.text.strip()
            except Exception as e:
                logger.warning("Gemini API failed", error=str(e))
        
        # Try Cohere
        if self.cohere_client:
            try:
                response = self.cohere_client.generate(
                    model='command-light',
                    prompt=full_prompt,
                    max_tokens=200,
                    temperature=0.7
                )
                return response.generations[0].text.strip()
            except Exception as e:
                logger.warning("Cohere API failed", error=str(e))
        
        return self._get_fallback_response(message)
    
    def _get_crisis_response(self) -> str:
        """Crisis response with immediate resources"""
        return """I'm very concerned about what you've shared. Please reach out for immediate support:

🚨 National Suicide Prevention Lifeline: 988
💬 Crisis Text Line: Text HOME to 741741
🚑 Emergency Services: 911

You are not alone, and help is available. Please contact one of these resources right now."""
    
    def _get_fallback_response(self, message: str) -> str:
        """Rule-based fallback responses"""
        
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['anxious', 'anxiety', 'worried']):
            return """It sounds like you're experiencing anxiety. Here are some techniques that can help:

• Deep breathing: Try the 4-7-8 technique (inhale 4, hold 7, exhale 8)
• Grounding: Name 5 things you see, 4 you hear, 3 you feel, 2 you smell, 1 you taste
• Progressive muscle relaxation

If anxiety persists, please consider speaking with a mental health professional."""

        elif any(word in message_lower for word in ['sad', 'depressed', 'down']):
            return """I hear that you're going through a difficult time. Some strategies that might help:

• Connect with others: Reach out to friends, family, or support groups
• Gentle movement: Even a short walk can help
• Maintain routine: Regular sleep and meals are important
• Practice self-compassion

If these feelings persist for more than two weeks, please consider professional support."""

        else:
            return """Thank you for sharing. I'm here to provide support and information about mental wellness. 

I can help you understand coping strategies or discuss your feelings. What specific area would you like to explore?

Remember, I'm not a replacement for professional mental health care."""