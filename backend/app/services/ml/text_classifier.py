import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from transformers import pipeline
import numpy as np
from typing import Dict, List
import re
import logging

class TextDepressionClassifier:
    def __init__(self, model_name: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # For demo, using sentiment analysis as proxy for depression
        # In production, use a properly trained depression classifier
        self.sentiment_classifier = pipeline(
            "sentiment-analysis",
            model=model_name,
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Crisis keywords for safety
        self.crisis_keywords = [
            'suicide', 'kill myself', 'end it all', 'worthless', 
            'hopeless', 'can\'t go on', 'want to die'
        ]
        
        self.depression_indicators = [
            'depressed', 'sad', 'empty', 'hopeless', 'worthless',
            'tired', 'exhausted', 'can\'t sleep', 'no energy',
            'anxious', 'worried', 'stressed', 'overwhelmed'
        ]
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text"""
        # Basic cleaning
        text = re.sub(r'http\S+', '', text)  # Remove URLs
        text = re.sub(r'@\w+', '', text)     # Remove mentions
        text = re.sub(r'#\w+', '', text)     # Remove hashtags
        text = re.sub(r'\s+', ' ', text)     # Normalize whitespace
        
        return text.strip()
    
    def detect_crisis(self, text: str) -> Dict:
        """Detect crisis indicators in text"""
        text_lower = text.lower()
        crisis_detected = False
        matched_keywords = []
        
        for keyword in self.crisis_keywords:
            if keyword in text_lower:
                crisis_detected = True
                matched_keywords.append(keyword)
        
        return {
            'crisis_detected': crisis_detected,
            'matched_keywords': matched_keywords,
            'confidence': 0.9 if crisis_detected else 0.1
        }
    
    def classify_depression(self, text: str) -> Dict:
        """Classify depression severity from text"""
        try:
            preprocessed_text = self.preprocess_text(text)
            
            # Check for crisis first
            crisis_result = self.detect_crisis(preprocessed_text)
            
            # Get sentiment analysis
            sentiment_result = self.sentiment_classifier(preprocessed_text)[0]
            
            # Convert sentiment to depression classification
            # This is a simplified approach - in production use trained models
            sentiment_label = sentiment_result['label'].upper()
            sentiment_score = sentiment_result['score']
            
            # Count depression indicators
            depression_count = sum(1 for indicator in self.depression_indicators 
                                 if indicator in preprocessed_text.lower())
            
            # Determine depression severity
            if crisis_result['crisis_detected']:
                depression_level = 'severe'
                confidence = 0.9
            elif sentiment_label == 'NEGATIVE' and sentiment_score > 0.8:
                if depression_count >= 3:
                    depression_level = 'severe'
                    confidence = 0.8
                elif depression_count >= 1:
                    depression_level = 'moderate'
                    confidence = 0.7
                else:
                    depression_level = 'mild'
                    confidence = 0.6
            elif sentiment_label == 'NEGATIVE':
                depression_level = 'mild'
                confidence = 0.6
            else:
                depression_level = 'minimal'
                confidence = 0.7
            
            return {
                'label': depression_level,
                'confidence': confidence,
                'probabilities': self._generate_probabilities(depression_level, confidence),
                'crisis_detected': crisis_result['crisis_detected'],
                'indicators_found': depression_count,
                'sentiment': {
                    'label': sentiment_label,
                    'score': sentiment_score
                }
            }
            
        except Exception as e:
            logging.error(f"Error in depression classification: {str(e)}")
            return {
                'label': 'unknown',
                'confidence': 0.0,
                'probabilities': {
                    'minimal': 0.25,
                    'mild': 0.25,
                    'moderate': 0.25,
                    'severe': 0.25
                },
                'crisis_detected': False,
                'error': str(e)
            }
    
    def _generate_probabilities(self, predicted_label: str, confidence: float) -> Dict:
        """Generate probability distribution for depression levels"""
        labels = ['minimal', 'mild', 'moderate', 'severe']
        probs = {label: 0.1 for label in labels}  # Base probability
        
        # Assign higher probability to predicted class
        probs[predicted_label] = confidence
        
        # Redistribute remaining probability
        remaining = 1.0 - confidence
        other_labels = [l for l in labels if l != predicted_label]
        prob_per_other = remaining / len(other_labels)
        
        for label in other_labels:
            probs[label] = prob_per_other
            
        return probs

class TextAnalyzer:
    def __init__(self):
        self.depression_classifier = TextDepressionClassifier()
        
        # Additional analyzers
        self.anxiety_keywords = [
            'anxious', 'worried', 'panic', 'nervous', 'stressed',
            'overwhelmed', 'restless', 'tense', 'fearful'
        ]
    
    def analyze_text(self, text: str) -> Dict:
        """Comprehensive text analysis"""
        if not text or len(text.strip()) < 5:
            return {
                'depression': {'label': 'insufficient_data', 'confidence': 0.0},
                'anxiety': {'label': 'insufficient_data', 'confidence': 0.0},
                'crisis': {'detected': False}
            }
        
        # Depression analysis
        depression_result = self.depression_classifier.classify_depression(text)
        
        # Anxiety analysis (simple keyword-based)
        anxiety_result = self._analyze_anxiety(text)
        
        return {
            'depression': depression_result,
            'anxiety': anxiety_result,
            'crisis': {
                'detected': depression_result.get('crisis_detected', False),
                'keywords': depression_result.get('matched_keywords', [])
            },
            'text_length': len(text),
            'word_count': len(text.split())
        }
    
    def _analyze_anxiety(self, text: str) -> Dict:
        """Simple anxiety level assessment"""
        text_lower = text.lower()
        anxiety_count = sum(1 for keyword in self.anxiety_keywords 
                          if keyword in text_lower)
        
        if anxiety_count >= 3:
            level = 'high'
            confidence = 0.8
        elif anxiety_count >= 1:
            level = 'moderate'
            confidence = 0.6
        else:
            level = 'low'
            confidence = 0.5
        
        return {
            'label': level,
            'confidence': confidence,
            'indicators_found': anxiety_count,
            'keywords_detected': [kw for kw in self.anxiety_keywords if kw in text_lower]
        }