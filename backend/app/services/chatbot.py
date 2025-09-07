"""
LLM-powered health chatbot with safety guardrails
"""
import openai
from typing import Dict, List, Any, Optional
import structlog
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory

from app.core.config import settings

logger = structlog.get_logger(__name__)

class HealthChatbot:
    """AI-powered health chatbot with safety guardrails"""
    
    def __init__(self):
        self.openai_client = None
        if settings.OPENAI_API_KEY:
            self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Safety keywords that trigger refusal
        self.unsafe_topics = [
            'diagnosis', 'prescribe', 'medication dosage', 'stop medication',
            'medical advice', 'replace doctor', 'cure', 'treat'
        ]
        
        # Crisis keywords that trigger emergency resources
        self.crisis_keywords = [
            'suicide', 'kill myself', 'end my life', 'not worth living',
            'self harm', 'hurt myself', 'overdose'
        ]
        
        # System prompt for health assistant
        self.system_prompt = """You are a supportive mental health companion assistant. Your role is to:

1. Provide emotional support and evidence-based coping strategies
2. Help users understand their EEG analysis results in simple terms
3. Suggest self-care activities and mental wellness practices
4. Guide users to appropriate professional help when needed

CRITICAL SAFETY RULES:
- Never provide medical diagnosis or replace professional care
- Never recommend specific medications or dosages
- Never tell users to stop prescribed treatments
- Always encourage professional help for serious concerns
- If crisis language is detected, immediately provide emergency resources

You can discuss:
- Coping strategies (breathing, mindfulness, exercise)
- Sleep hygiene and stress management
- General wellness practices
- Explaining EEG results in simple terms
- When to seek professional help

Always end responses with appropriate disclaimers about not replacing professional care."""

        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=5  # Remember last 5 exchanges
        )
    
    async def chat(
        self,
        message: str,
        user_context: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process chat message with safety checks"""
        
        logger.info("Processing chat message", 
                   message_length=len(message),
                   session_id=session_id)
        
        try:
            # Safety checks
            safety_check = self._check_message_safety(message)
            if safety_check['action'] == 'block':
                return safety_check
            elif safety_check['action'] == 'crisis':
                return self._handle_crisis_response(message, safety_check)
            
            # Generate response
            if self.openai_client:
                response = await self._generate_llm_response(message, user_context)
            else:
                response = self._generate_fallback_response(message)
            
            # Post-process for additional safety
            final_response = self._post_process_response(response, safety_check)
            
            return {
                'response': final_response,
                'safety_checked': True,
                'crisis_detected': safety_check['action'] == 'crisis',
                'disclaimer': self._get_disclaimer()
            }
            
        except Exception as e:
            logger.error("Chat processing failed", error=str(e))
            return {
                'response': "I'm having technical difficulties right now. Please try again or contact support if issues persist.",
                'error': True,
                'disclaimer': self._get_disclaimer()
            }
    
    def _check_message_safety(self, message: str) -> Dict[str, Any]:
        """Check message for safety concerns"""
        message_lower = message.lower()
        
        # Crisis detection
        for keyword in self.crisis_keywords:
            if keyword in message_lower:
                return {
                    'action': 'crisis',
                    'detected_keywords': [keyword],
                    'severity': 'high'
                }
        
        # Unsafe topic detection
        detected_unsafe = []
        for topic in self.unsafe_topics:
            if topic in message_lower:
                detected_unsafe.append(topic)
        
        if detected_unsafe:
            return {
                'action': 'block',
                'detected_topics': detected_unsafe,
                'severity': 'medium'
            }
        
        return {'action': 'proceed', 'severity': 'low'}
    
    def _handle_crisis_response(self, message: str, safety_check: Dict) -> Dict[str, Any]:
        """Handle crisis situations with immediate resources"""
        
        crisis_response = """I'm very concerned about what you've shared. Your safety is the most important thing right now.

Please reach out for immediate support:

🚨 **Emergency Services**: 911 (US) or your local emergency number
📞 **National Suicide Prevention Lifeline**: 988 (US) or 1-800-273-8255
💬 **Crisis Text Line**: Text HOME to 741741
🌐 **International**: befrienders.org for worldwide support

You are not alone, and help is available. Professional counselors are trained to help with exactly what you're experiencing.

Would you like me to help you find mental health professionals in your area?"""

        return {
            'response': crisis_response,
            'crisis_detected': True,
            'emergency_resources': True,
            'action_required': 'immediate_support',
            'disclaimer': "This is not a substitute for emergency services or professional crisis intervention."
        }
    
    async def _generate_llm_response(
        self, 
        message: str, 
        user_context: Optional[Dict[str, Any]]
    ) -> str:
        """Generate response using LLM"""
        
        # Build context-aware prompt
        context_info = ""
        if user_context:
            recent_analysis = user_context.get('recent_analysis')
            if recent_analysis:
                risk_level = recent_analysis.get('risk_level', 'unknown')
                context_info = f"\nUser's recent analysis shows {risk_level} risk level. "
        
        full_prompt = f"{self.system_prompt}\n{context_info}\nUser: {message}\nAssistant:"
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt + context_info},
                    {"role": "user", "content": message}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error("LLM generation failed", error=str(e))
            return self._generate_fallback_response(message)
    
    def _generate_fallback_response(self, message: str) -> str:
        """Generate rule-based response when LLM unavailable"""
        
        message_lower = message.lower()
        
        # Common response patterns
        if any(word in message_lower for word in ['anxious', 'anxiety', 'worried']):
            return """It sounds like you're experiencing anxiety. Here are some techniques that many people find helpful:

• **Deep breathing**: Try the 4-7-8 technique - inhale for 4, hold for 7, exhale for 8
• **Grounding**: Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste
• **Progressive muscle relaxation**: Tense and release muscle groups starting from your toes

If anxiety persists or interferes with daily life, consider speaking with a mental health professional."""

        elif any(word in message_lower for word in ['sad', 'depressed', 'down', 'low']):
            return """I hear that you're going through a difficult time. It's important to acknowledge these feelings. Some strategies that might help:

• **Connect with others**: Reach out to friends, family, or support groups
• **Gentle movement**: Even a short walk can help improve mood
• **Routine**: Maintain basic self-care like regular sleep and meals
• **Mindfulness**: Practice being present without judgment

If these feelings persist for more than two weeks or impact your daily functioning, please consider reaching out to a mental health professional."""

        elif any(word in message_lower for word in ['stress', 'overwhelmed', 'pressure']):
            return """Feeling stressed or overwhelmed is very common. Here are some immediate strategies:

• **Prioritize tasks**: Focus on what's most important today
• **Take breaks**: Even 5-10 minutes can help reset your mind
• **Breathing exercises**: Deep, slow breaths activate your relaxation response
• **Set boundaries**: It's okay to say no to additional commitments

Remember, it's important to address chronic stress with professional support if needed."""

        else:
            return """Thank you for sharing. I'm here to provide support and information about mental wellness. 

I can help you understand coping strategies, discuss your analysis results, or guide you toward appropriate resources. What specific area would you like to explore?

Remember, while I can offer support and information, I'm not a replacement for professional mental health care."""
    
    def _post_process_response(self, response: str, safety_check: Dict) -> str:
        """Post-process response for additional safety"""
        
        # Add disclaimers for medical topics
        medical_terms = ['treatment', 'therapy', 'medication', 'diagnosis']
        if any(term in response.lower() for term in medical_terms):
            response += "\n\n*Please consult with a qualified healthcare provider for medical advice.*"
        
        return response
    
    def _get_disclaimer(self) -> str:
        """Standard disclaimer for all responses"""
        return ("This assistant provides supportive information only and is not a substitute "
                "for professional medical advice, diagnosis, or treatment.")

    def get_explanation_for_results(self, analysis_results: Dict[str, Any]) -> str:
        """Generate user-friendly explanation of analysis results"""
        
        risk_level = analysis_results.get('risk_level', 'unknown')
        emotion = analysis_results.get('emotion_fusion', {}).get('label', 'neutral')
        anxiety = analysis_results.get('anxiety_fusion', {}).get('label', 'low')
        
        explanation = f"""Based on your analysis, here's what the results suggest:

**Overall Assessment**: {risk_level.title()} risk level detected

**Emotional State**: The analysis indicates a {emotion} emotional pattern. """

        if emotion == 'stressed':
            explanation += "This suggests you might be experiencing stress, which is very common and manageable with the right strategies."
        elif emotion == 'sad':
            explanation += "This pattern is often associated with low mood, which can be temporary and responsive to self-care."
        
        explanation += f"""

**Anxiety Level**: {anxiety.title()} anxiety indicators were found. """
        
        if anxiety == 'high':
            explanation += "Consider practicing relaxation techniques and monitoring these feelings."
        elif anxiety == 'moderate':
            explanation += "This is manageable with stress-reduction practices."
        
        explanation += f"""

**Next Steps**: Based on the {risk_level} risk level:"""
        
        if risk_level == 'high':
            explanation += "\n• Consider speaking with a mental health professional soon\n• Use immediate coping strategies\n• Ensure you have support nearby"
        elif risk_level == 'moderate':
            explanation += "\n• Practice regular self-care\n• Monitor your symptoms\n• Consider professional support if symptoms persist"
        else:
            explanation += "\n• Continue with healthy habits\n• Practice preventive self-care\n• Stay connected with support systems"
        
        return explanation