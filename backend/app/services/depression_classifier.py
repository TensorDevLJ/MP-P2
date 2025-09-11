"""
Transformer-based depression classification using free APIs
"""
import google.generativeai as genai
import cohere
from typing import Dict, Any, Optional
import structlog
import re

from app.core.config import settings

logger = structlog.get_logger(__name__)

class DepressionClassifier:
    """Depression classification using transformer models and free APIs"""
    
    def __init__(self):
        # Initialize free API clients
        self.gemini_model = None
        self.cohere_client = None
        
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel('gemini-pro')
        
        if settings.COHERE_API_KEY:
            self.cohere_client = cohere.Client(settings.COHERE_API_KEY)
        
        # Depression indicators for rule-based fallback
        self.depression_keywords = {
            'severe': [
                'hopeless', 'worthless', 'suicidal', 'kill myself', 'end it all',
                'pointless', 'empty', 'numb', 'trapped', 'burden'
            ],
            'moderate': [
                'depressed', 'sad', 'down', 'low', 'blue', 'unhappy',
                'tired', 'exhausted', 'unmotivated', 'lonely', 'isolated'
            ],
            'mild': [
                'stressed', 'worried', 'anxious', 'overwhelmed', 'frustrated',
                'disappointed', 'discouraged', 'upset'
            ]
        }
        
        self.positive_indicators = [
            'happy', 'good', 'great', 'excellent', 'wonderful', 'amazing',
            'positive', 'optimistic', 'hopeful', 'grateful', 'blessed'
        ]
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze text for depression indicators"""
        
        logger.info("Analyzing text for depression", text_length=len(text))
        
        try:
            # Try AI-powered analysis first
            ai_result = self._analyze_with_ai(text)
            if ai_result:
                return ai_result
            
            # Fallback to rule-based analysis
            return self._analyze_with_rules(text)
            
        except Exception as e:
            logger.error("Text analysis failed", error=str(e))
            return self._analyze_with_rules(text)
    
    def _analyze_with_ai(self, text: str) -> Optional[Dict[str, Any]]:
        """Use AI APIs for analysis"""
        
        prompt = f"""
        Analyze the following text for depression indicators. Classify the depression level as:
        - "not_depressed": No significant depression indicators
        - "mild": Mild stress or temporary low mood
        - "moderate": Clear depression symptoms affecting daily life
        - "severe": Severe depression with significant impairment or crisis indicators
        
        Text to analyze: "{text}"
        
        Respond with only the classification level and a confidence score (0-1).
        Format: LEVEL|CONFIDENCE
        Example: moderate|0.75
        """
        
        try:
            # Try Gemini first
            if self.gemini_model:
                response = self.gemini_model.generate_content(prompt)
                result = self._parse_ai_response(response.text, text)
                if result:
                    return result
        except Exception as e:
            logger.warning("Gemini API failed", error=str(e))
        
        try:
            # Try Cohere
            if self.cohere_client:
                response = self.cohere_client.generate(
                    model='command-light',
                    prompt=prompt,
                    max_tokens=50,
                    temperature=0.3
                )
                result = self._parse_ai_response(response.generations[0].text, text)
                if result:
                    return result
        except Exception as e:
            logger.warning("Cohere API failed", error=str(e))
        
        return None
    
    def _parse_ai_response(self, response: str, original_text: str) -> Optional[Dict[str, Any]]:
        """Parse AI response into structured format"""
        
        try:
            # Look for pattern: level|confidence
            match = re.search(r'(not_depressed|mild|moderate|severe)\|([0-9.]+)', response.lower())
            
            if match:
                level = match.group(1)
                confidence = float(match.group(2))
                
                return {
                    'depression_level': level,
                    'confidence': confidence,
                    'analysis_method': 'ai',
                    'explanation': self._generate_explanation(level, confidence, original_text)
                }
        except Exception as e:
            logger.error("Failed to parse AI response", error=str(e))
        
        return None
    
    def _analyze_with_rules(self, text: str) -> Dict[str, Any]:
        """Rule-based depression analysis as fallback"""
        
        text_lower = text.lower()
        
        # Count indicators by severity
        scores = {'severe': 0, 'moderate': 0, 'mild': 0, 'positive': 0}
        
        for level, keywords in self.depression_keywords.items():
            for keyword in keywords:
                scores[level] += text_lower.count(keyword)
        
        for keyword in self.positive_indicators:
            scores['positive'] += text_lower.count(keyword)
        
        # Determine classification
        if scores['severe'] > 0:
            level = 'severe'
            confidence = min(0.9, 0.6 + scores['severe'] * 0.1)
        elif scores['moderate'] > scores['positive']:
            level = 'moderate'
            confidence = min(0.8, 0.5 + scores['moderate'] * 0.05)
        elif scores['mild'] > scores['positive']:
            level = 'mild'
            confidence = min(0.7, 0.4 + scores['mild'] * 0.05)
        else:
            level = 'not_depressed'
            confidence = min(0.8, 0.5 + scores['positive'] * 0.05)
        
        return {
            'depression_level': level,
            'confidence': confidence,
            'analysis_method': 'rule_based',
            'keyword_scores': scores,
            'explanation': self._generate_explanation(level, confidence, text)
        }
    
    def _generate_explanation(self, level: str, confidence: float, text: str) -> str:
        """Generate human-readable explanation"""
        
        explanations = {
            'not_depressed': "The text shows positive language patterns with no significant depression indicators.",
            'mild': "Some stress or temporary low mood indicators detected. This is common and often manageable with self-care.",
            'moderate': "Clear depression symptoms are present that may be affecting daily functioning. Consider professional support.",
            'severe': "Significant depression indicators detected. Please reach out to a mental health professional immediately."
        }
        
        base_explanation = explanations.get(level, "Analysis completed.")
        confidence_text = f" (Confidence: {confidence:.0%})"
        
        return base_explanation + confidence_text