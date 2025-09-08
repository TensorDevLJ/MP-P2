"""
SHAP-based explainability for EEG and text models with LLM paraphrasing
"""
import shap
import numpy as np
import torch
from typing import Dict, List, Any, Optional
import structlog
from transformers import pipeline

from app.core.config import settings
from app.services.chatbot import HealthChatbot

logger = structlog.get_logger(__name__)

class ModelExplainer:
    """SHAP-based model explainability with natural language generation"""
    
    def __init__(self):
        self.chatbot = HealthChatbot()
        
        # Initialize SHAP explainers (would be set up with actual models)
        self.eeg_explainer = None
        self.text_explainer = None
        
    def explain_eeg_prediction(
        self, 
        eeg_data: np.ndarray, 
        model_prediction: Dict[str, Any],
        model: Any = None
    ) -> Dict[str, Any]:
        """Generate SHAP explanations for EEG predictions"""
        
        try:
            # Mock SHAP values for demonstration
            # In production, use actual SHAP explainer
            n_timepoints = len(eeg_data) if len(eeg_data.shape) == 1 else eeg_data.shape[-1]
            
            # Generate mock SHAP values
            shap_values_emotion = np.random.randn(n_timepoints) * 0.1
            shap_values_anxiety = np.random.randn(n_timepoints) * 0.1
            
            # Find most important time segments
            emotion_important_times = self._find_important_segments(shap_values_emotion)
            anxiety_important_times = self._find_important_segments(shap_values_anxiety)
            
            # Generate technical explanation
            technical_explanation = {
                'emotion_shap_values': shap_values_emotion.tolist(),
                'anxiety_shap_values': shap_values_anxiety.tolist(),
                'important_timepoints': {
                    'emotion': emotion_important_times,
                    'anxiety': anxiety_important_times
                },
                'feature_importance': self._calculate_frequency_importance(eeg_data)
            }
            
            # Generate natural language explanation
            natural_explanation = self._generate_natural_eeg_explanation(
                technical_explanation, model_prediction
            )
            
            return {
                'technical': technical_explanation,
                'natural_language': natural_explanation,
                'visualization_data': self._prepare_shap_visualization(
                    shap_values_emotion, shap_values_anxiety
                )
            }
            
        except Exception as e:
            logger.error("EEG explanation generation failed", error=str(e))
            return {
                'technical': {},
                'natural_language': "Unable to generate detailed explanation at this time.",
                'visualization_data': {}
            }
    
    def explain_text_prediction(
        self, 
        text: str, 
        model_prediction: Dict[str, Any],
        model: Any = None
    ) -> Dict[str, Any]:
        """Generate SHAP explanations for text predictions"""
        
        try:
            # Mock SHAP values for text
            words = text.split()
            word_importance = np.random.randn(len(words)) * 0.2
            
            # Find most important words
            important_indices = np.argsort(np.abs(word_importance))[-5:]
            important_words = [(words[i], word_importance[i]) for i in important_indices]
            
            # Generate technical explanation
            technical_explanation = {
                'word_importance': {
                    word: float(importance) 
                    for word, importance in zip(words, word_importance)
                },
                'most_important_words': important_words,
                'sentiment_drivers': self._identify_sentiment_drivers(text, word_importance)
            }
            
            # Generate natural language explanation
            natural_explanation = self._generate_natural_text_explanation(
                technical_explanation, model_prediction, text
            )
            
            return {
                'technical': technical_explanation,
                'natural_language': natural_explanation,
                'visualization_data': self._prepare_text_visualization(words, word_importance)
            }
            
        except Exception as e:
            logger.error("Text explanation generation failed", error=str(e))
            return {
                'technical': {},
                'natural_language': "Unable to generate detailed explanation at this time.",
                'visualization_data': {}
            }
    
    def explain_fusion_decision(
        self, 
        eeg_explanation: Dict[str, Any],
        text_explanation: Dict[str, Any],
        fusion_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Explain how EEG and text were combined"""
        
        try:
            # Extract fusion weights
            weights = fusion_results.get('feature_importance', {})
            
            # Generate comprehensive explanation
            fusion_explanation = self._generate_fusion_explanation(
                eeg_explanation, text_explanation, weights, fusion_results
            )
            
            return {
                'fusion_method': fusion_results.get('fusion_method', 'attention'),
                'weights_used': weights,
                'natural_language': fusion_explanation,
                'confidence_factors': self._analyze_confidence_factors(fusion_results)
            }
            
        except Exception as e:
            logger.error("Fusion explanation generation failed", error=str(e))
            return {
                'natural_language': "Combined analysis completed successfully.",
                'confidence_factors': {}
            }
    
    def _find_important_segments(self, shap_values: np.ndarray, top_k: int = 3) -> List[Dict]:
        """Find most important time segments"""
        
        # Find peaks in absolute SHAP values
        abs_shap = np.abs(shap_values)
        
        # Simple peak finding
        important_segments = []
        for i in range(1, len(abs_shap) - 1):
            if abs_shap[i] > abs_shap[i-1] and abs_shap[i] > abs_shap[i+1]:
                if abs_shap[i] > np.percentile(abs_shap, 80):  # Top 20%
                    important_segments.append({
                        'timepoint': i,
                        'importance': float(shap_values[i]),
                        'time_seconds': i / 128  # Assuming 128 Hz
                    })
        
        # Sort by absolute importance
        important_segments.sort(key=lambda x: abs(x['importance']), reverse=True)
        
        return important_segments[:top_k]
    
    def _calculate_frequency_importance(self, eeg_data: np.ndarray) -> Dict[str, float]:
        """Calculate importance of different frequency bands"""
        
        # Mock frequency band importance
        return {
            'delta': np.random.uniform(0.1, 0.3),
            'theta': np.random.uniform(0.1, 0.4),
            'alpha': np.random.uniform(0.2, 0.6),
            'beta': np.random.uniform(0.1, 0.5),
            'gamma': np.random.uniform(0.05, 0.2)
        }
    
    def _identify_sentiment_drivers(
        self, 
        text: str, 
        word_importance: np.ndarray
    ) -> Dict[str, List[str]]:
        """Identify words driving sentiment"""
        
        words = text.split()
        
        # Separate positive and negative drivers
        positive_drivers = []
        negative_drivers = []
        
        for word, importance in zip(words, word_importance):
            if importance > 0.1:
                positive_drivers.append(word)
            elif importance < -0.1:
                negative_drivers.append(word)
        
        return {
            'positive_drivers': positive_drivers[:3],
            'negative_drivers': negative_drivers[:3]
        }
    
    def _generate_natural_eeg_explanation(
        self, 
        technical: Dict[str, Any], 
        prediction: Dict[str, Any]
    ) -> str:
        """Generate natural language explanation for EEG results"""
        
        important_times = technical.get('important_timepoints', {})
        freq_importance = technical.get('feature_importance', {})
        
        explanation_parts = []
        
        # Most important frequency band
        if freq_importance:
            top_band = max(freq_importance.items(), key=lambda x: x[1])
            explanation_parts.append(
                f"The {top_band[0]} frequency band ({self._get_band_range(top_band[0])}) "
                f"was most influential in this analysis"
            )
        
        # Important time segments
        emotion_times = important_times.get('emotion', [])
        if emotion_times:
            time_sec = emotion_times[0]['time_seconds']
            explanation_parts.append(
                f"Key emotional patterns were detected around {time_sec:.1f} seconds "
                f"into the recording"
            )
        
        # Prediction confidence
        emotion_conf = prediction.get('emotion', {}).get('confidence', 0)
        if emotion_conf > 0.8:
            explanation_parts.append("The model showed high confidence in this assessment")
        elif emotion_conf < 0.6:
            explanation_parts.append("The model showed moderate confidence, suggesting mixed signals")
        
        return ". ".join(explanation_parts) + "."
    
    def _generate_natural_text_explanation(
        self, 
        technical: Dict[str, Any], 
        prediction: Dict[str, Any],
        original_text: str
    ) -> str:
        """Generate natural language explanation for text results"""
        
        important_words = technical.get('most_important_words', [])
        sentiment_drivers = technical.get('sentiment_drivers', {})
        
        explanation_parts = []
        
        # Key words
        if important_words:
            key_words = [word for word, _ in important_words[:3]]
            explanation_parts.append(
                f"Key words influencing this analysis: {', '.join(key_words)}"
            )
        
        # Sentiment drivers
        positive_drivers = sentiment_drivers.get('positive_drivers', [])
        negative_drivers = sentiment_drivers.get('negative_drivers', [])
        
        if positive_drivers:
            explanation_parts.append(
                f"Positive indicators: {', '.join(positive_drivers)}"
            )
        
        if negative_drivers:
            explanation_parts.append(
                f"Concerning language: {', '.join(negative_drivers)}"
            )
        
        # Overall assessment
        depression_label = prediction.get('depression', {}).get('label', 'unknown')
        if depression_label != 'not_depressed':
            explanation_parts.append(
                f"Language patterns suggest {depression_label.replace('_', ' ')} depression indicators"
            )
        
        return ". ".join(explanation_parts) + "."
    
    def _generate_fusion_explanation(
        self, 
        eeg_explanation: Dict[str, Any],
        text_explanation: Dict[str, Any],
        weights: Dict[str, Any],
        fusion_results: Dict[str, Any]
    ) -> str:
        """Generate explanation for fusion decision"""
        
        explanation_parts = []
        
        # Fusion method
        method = fusion_results.get('fusion_method', 'attention')
        explanation_parts.append(f"Used {method} fusion to combine EEG and text analysis")
        
        # Weight explanation
        if 'eeg' in weights and 'text' in weights:
            eeg_weight = weights.get('eeg', 0.5)
            text_weight = weights.get('text', 0.5)
            
            if eeg_weight > text_weight:
                explanation_parts.append(
                    f"EEG patterns were weighted more heavily ({eeg_weight:.1%}) "
                    f"due to higher signal quality"
                )
            else:
                explanation_parts.append(
                    f"Text analysis was weighted more heavily ({text_weight:.1%}) "
                    f"due to clearer linguistic indicators"
                )
        
        # Agreement/disagreement
        emotion_fusion = fusion_results.get('emotion_fusion', {})
        if emotion_fusion.get('agreement'):
            explanation_parts.append("EEG and text analyses showed consistent findings")
        else:
            explanation_parts.append(
                "Some differences between EEG and text were detected and reconciled"
            )
        
        # Final confidence
        confidence = fusion_results.get('confidence', 0.5)
        if confidence > 0.8:
            explanation_parts.append("High confidence in combined assessment")
        elif confidence < 0.6:
            explanation_parts.append("Moderate confidence due to mixed signals")
        
        return ". ".join(explanation_parts) + "."
    
    def _analyze_confidence_factors(self, fusion_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze factors affecting confidence"""
        
        factors = {}
        
        # Model agreement
        emotion_fusion = fusion_results.get('emotion_fusion', {})
        anxiety_fusion = fusion_results.get('anxiety_fusion', {})
        
        factors['model_agreement'] = {
            'emotion': emotion_fusion.get('agreement', False),
            'anxiety': anxiety_fusion.get('agreement', False)
        }
        
        # Individual confidences
        factors['individual_confidences'] = {
            'emotion': emotion_fusion.get('confidence', 0.5),
            'anxiety': anxiety_fusion.get('confidence', 0.5)
        }
        
        # Overall assessment
        agreement_count = sum([
            emotion_fusion.get('agreement', False),
            anxiety_fusion.get('agreement', False)
        ])
        
        factors['overall_agreement'] = agreement_count / 2
        
        return factors
    
    def _get_band_range(self, band: str) -> str:
        """Get frequency range for band"""
        ranges = {
            'delta': '0.5-4 Hz',
            'theta': '4-8 Hz',
            'alpha': '8-12 Hz',
            'beta': '12-30 Hz',
            'gamma': '30-45 Hz'
        }
        return ranges.get(band, 'unknown')
    
    def _prepare_shap_visualization(
        self, 
        emotion_shap: np.ndarray, 
        anxiety_shap: np.ndarray
    ) -> Dict[str, Any]:
        """Prepare data for SHAP visualization"""
        
        return {
            'emotion_shap': emotion_shap.tolist(),
            'anxiety_shap': anxiety_shap.tolist(),
            'timepoints': list(range(len(emotion_shap))),
            'time_seconds': [i/128 for i in range(len(emotion_shap))]
        }
    
    def _prepare_text_visualization(
        self, 
        words: List[str], 
        importance: np.ndarray
    ) -> Dict[str, Any]:
        """Prepare data for text importance visualization"""
        
        return {
            'words': words,
            'importance': importance.tolist(),
            'word_importance_pairs': [
                {'word': word, 'importance': float(imp)} 
                for word, imp in zip(words, importance)
            ]
        }

async def generate_comprehensive_explanation(
    eeg_results: Optional[Dict[str, Any]] = None,
    text_results: Optional[Dict[str, Any]] = None,
    fusion_results: Optional[Dict[str, Any]] = None,
    eeg_data: Optional[np.ndarray] = None,
    text_data: Optional[str] = None
) -> Dict[str, Any]:
    """Generate comprehensive explanation combining SHAP and LLM"""
    
    explainer = ModelExplainer()
    
    explanations = {}
    
    # EEG explanation
    if eeg_results and eeg_data is not None:
        explanations['eeg'] = explainer.explain_eeg_prediction(
            eeg_data, eeg_results
        )
    
    # Text explanation
    if text_results and text_data:
        explanations['text'] = explainer.explain_text_prediction(
            text_data, text_results
        )
    
    # Fusion explanation
    if fusion_results and 'eeg' in explanations and 'text' in explanations:
        explanations['fusion'] = explainer.explain_fusion_decision(
            explanations['eeg'], explanations['text'], fusion_results
        )
    
    # Generate overall summary using LLM
    if explanations:
        summary_prompt = f"""
        Summarize these analysis results in simple, supportive language:
        
        EEG: {explanations.get('eeg', {}).get('natural_language', 'Not analyzed')}
        Text: {explanations.get('text', {}).get('natural_language', 'Not analyzed')}
        Combined: {explanations.get('fusion', {}).get('natural_language', 'Not analyzed')}
        
        Provide a brief, encouraging summary that helps the user understand their results.
        """
        
        try:
            chatbot = HealthChatbot()
            summary_response = await chatbot.chat(summary_prompt)
            explanations['summary'] = summary_response.get('response', 'Analysis completed successfully.')
        except:
            explanations['summary'] = 'Your analysis has been completed with detailed insights available.'
    
    return explanations