"""
RoBERTa-based text analysis for depression severity assessment
"""
from typing import Dict, List, Any, Optional
import re
import structlog
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

logger = structlog.get_logger(__name__)

class TextClassifier:
    """Text analysis for mental health assessment"""
    
    def __init__(self, model_path: str = "roberta-base"):
        self.model_path = model_path
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Depression severity classes
        self.depression_classes = ['not_depressed', 'moderate', 'severe']
        
        # Anxiety keywords for supplementary analysis
        self.anxiety_keywords = {
            'high': ['panic', 'terror', 'overwhelming', 'catastrophic', 'unbearable'],
            'moderate': ['anxious', 'worried', 'nervous', 'stressed', 'tense', 'uneasy'],
            'low': ['calm', 'relaxed', 'peaceful', 'content', 'stable']
        }
        
        # Crisis keywords for safety
        self.crisis_keywords = [
            'suicide', 'kill myself', 'end it all', 'not worth living',
            'self harm', 'hurt myself', 'cutting', 'overdose'
        ]
        
        self._load_models()
    
    def _load_models(self):
        """Load text classification models"""
        try:
            # For development, use a general sentiment model
            # In production, load fine-tuned depression classifier
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                device=0 if self.device == "cuda" else -1
            )
            
            logger.info("Loaded text classification models")
            
        except Exception as e:
            logger.error("Failed to load text models", error=str(e))
            # Fallback to rule-based analysis
            self.sentiment_pipeline = None
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Comprehensive text analysis for mental health indicators"""
        
        logger.info("Starting text analysis", text_length=len(text))
        
        try:
            # Preprocess text
            cleaned_text = self._preprocess_text(text)
            
            # Safety check for crisis keywords
            safety_flags = self._check_safety(cleaned_text)
            
            # Depression severity analysis
            depression_results = self._analyze_depression(cleaned_text)
            
            # Anxiety keyword analysis
            anxiety_results = self._analyze_anxiety_keywords(cleaned_text)
            
            # General sentiment
            sentiment_results = self._analyze_sentiment(cleaned_text)
            
            return {
                'depression': depression_results,
                'anxiety_keywords': anxiety_results,
                'sentiment': sentiment_results,
                'safety_flags': safety_flags,
                'text_stats': {
                    'word_count': len(cleaned_text.split()),
                    'char_count': len(cleaned_text),
                    'sentence_count': len(re.split(r'[.!?]+', cleaned_text))
                }
            }
            
        except Exception as e:
            logger.error("Text analysis failed", error=str(e))
            raise ValueError(f"Text analysis failed: {str(e)}")
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and preprocess text"""
        # Basic cleaning
        text = re.sub(r'http\S+', '', text)  # Remove URLs
        text = re.sub(r'@\w+', '', text)     # Remove mentions
        text = re.sub(r'\s+', ' ', text)     # Normalize whitespace
        text = text.strip().lower()
        
        return text
    
    def _check_safety(self, text: str) -> Dict[str, Any]:
        """Check for crisis indicators"""
        flags = []
        
        for keyword in self.crisis_keywords:
            if keyword in text:
                flags.append(keyword)
        
        return {
            'has_crisis_indicators': len(flags) > 0,
            'crisis_keywords_found': flags,
            'risk_level': 'high' if len(flags) > 0 else 'low'
        }
    
    def _analyze_depression(self, text: str) -> Dict[str, Any]:
        """Analyze text for depression severity indicators"""
        
        # Depression indicator keywords
        depression_indicators = {
            'severe': ['hopeless', 'worthless', 'empty', 'numb', 'pointless', 'trapped'],
            'moderate': ['sad', 'down', 'depressed', 'low', 'blue', 'unhappy', 'tired'],
            'positive': ['happy', 'good', 'better', 'improving', 'hopeful', 'optimistic']
        }
        
        scores = {'severe': 0, 'moderate': 0, 'positive': 0}
        
        for severity, keywords in depression_indicators.items():
            for keyword in keywords:
                scores[severity] += text.count(keyword)
        
        # Simple scoring logic
        total_negative = scores['severe'] + scores['moderate']
        
        if scores['severe'] > 2 or (scores['severe'] > 0 and scores['positive'] == 0):
            predicted_class = 'severe'
            confidence = min(0.9, 0.6 + scores['severe'] * 0.1)
        elif scores['moderate'] > scores['positive']:
            predicted_class = 'moderate'
            confidence = min(0.8, 0.5 + scores['moderate'] * 0.05)
        else:
            predicted_class = 'not_depressed'
            confidence = min(0.8, 0.5 + scores['positive'] * 0.05)
        
        probabilities = {
            'not_depressed': 0.8 if predicted_class == 'not_depressed' else 0.1,
            'moderate': 0.8 if predicted_class == 'moderate' else 0.1,
            'severe': 0.8 if predicted_class == 'severe' else 0.1
        }
        
        # Normalize probabilities
        total = sum(probabilities.values())
        probabilities = {k: v/total for k, v in probabilities.items()}
        
        return {
            'label': predicted_class,
            'probabilities': probabilities,
            'confidence': confidence,
            'keyword_scores': scores
        }
    
    def _analyze_anxiety_keywords(self, text: str) -> Dict[str, Any]:
        """Analyze anxiety level based on keywords"""
        
        scores = {'high': 0, 'moderate': 0, 'low': 0}
        
        for level, keywords in self.anxiety_keywords.items():
            for keyword in keywords:
                scores[level] += text.count(keyword)
        
        # Determine level
        if scores['high'] > 0:
            level = 'high'
        elif scores['moderate'] > scores['low']:
            level = 'moderate'
        else:
            level = 'low'
        
        return {
            'level': level,
            'scores': scores,
            'total_anxiety_words': sum(scores.values())
        }
    
    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """General sentiment analysis"""
        
        if self.sentiment_pipeline is None:
            # Fallback rule-based sentiment
            positive_words = ['good', 'great', 'happy', 'amazing', 'wonderful', 'excellent']
            negative_words = ['bad', 'terrible', 'awful', 'horrible', 'sad', 'angry']
            
            pos_count = sum(text.count(word) for word in positive_words)
            neg_count = sum(text.count(word) for word in negative_words)
            
            if pos_count > neg_count:
                return {'label': 'positive', 'score': 0.7}
            elif neg_count > pos_count:
                return {'label': 'negative', 'score': 0.7}
            else:
                return {'label': 'neutral', 'score': 0.6}
        
        try:
            result = self.sentiment_pipeline(text)
            return {
                'label': result[0]['label'].lower(),
                'score': result[0]['score']
            }
        except Exception as e:
            logger.error("Sentiment analysis failed", error=str(e))
            return {'label': 'neutral', 'score': 0.5}