"""
Advanced fusion engine with attention weighting and Bayesian fusion
"""
import numpy as np
from typing import Dict, Any, Optional, List
import structlog
from scipy.special import softmax

logger = structlog.get_logger(__name__)

class AdvancedFusionEngine:
    """Advanced fusion engine with attention weighting and Bayesian methods"""
    
    def __init__(self):
        # Learned attention weights (would be trained in practice)
        self.attention_weights = {
            'eeg_emotion': 0.7,
            'text_emotion': 0.3,
            'eeg_anxiety': 0.8,
            'text_anxiety': 0.2
        }
        
        # Bayesian priors (population statistics)
        self.priors = {
            'emotion': {
                'happy': 0.25,
                'sad': 0.15,
                'neutral': 0.35,
                'stressed': 0.20,
                'relaxed': 0.05
            },
            'anxiety': {
                'low': 0.60,
                'moderate': 0.30,
                'high': 0.10
            },
            'depression': {
                'not_depressed': 0.70,
                'moderate': 0.25,
                'severe': 0.05
            }
        }
        
        # Risk level mapping
        self.risk_levels = ['stable', 'mild', 'moderate', 'high']
        
        # Safety rules (highest priority)
        self.safety_rules = {
            'crisis_detected': 'high',
            'severe_depression_text': 'high',
            'high_anxiety_both': 'moderate'
        }
    
    def fuse_predictions(
        self,
        eeg_results: Optional[Dict[str, Any]] = None,
        text_results: Optional[Dict[str, Any]] = None,
        user_calibration: Optional[Dict[str, float]] = None,
        fusion_method: str = 'attention'
    ) -> Dict[str, Any]:
        """
        Advanced fusion with multiple methods
        
        Args:
            eeg_results: Output from EEG model
            text_results: Output from text classifier
            user_calibration: Per-user weight adjustments
            fusion_method: 'attention', 'bayesian', or 'ensemble'
            
        Returns:
            Fused prediction with risk level and explanations
        """
        
        logger.info("Starting advanced prediction fusion", 
                   has_eeg=bool(eeg_results),
                   has_text=bool(text_results),
                   method=fusion_method)
        
        try:
            # Apply safety rules first
            safety_override = self._apply_safety_rules(eeg_results, text_results)
            if safety_override:
                return safety_override
            
            # Choose fusion method
            if fusion_method == 'attention':
                fusion_results = self._attention_fusion(eeg_results, text_results, user_calibration)
            elif fusion_method == 'bayesian':
                fusion_results = self._bayesian_fusion(eeg_results, text_results)
            else:
                fusion_results = self._ensemble_fusion(eeg_results, text_results)
            
            # Determine overall risk level
            risk_assessment = self._assess_risk_level_advanced(fusion_results, text_results)
            
            # Generate explanation with SHAP-like importance
            explanation = self._generate_explanation_with_importance(
                eeg_results, text_results, fusion_results, risk_assessment
            )
            
            return {
                'risk_level': risk_assessment['level'],
                'confidence': risk_assessment['confidence'],
                'emotion_fusion': fusion_results['emotion'],
                'anxiety_fusion': fusion_results['anxiety'],
                'explanation': explanation,
                'feature_importance': fusion_results.get('importance', {}),
                'fusion_method': fusion_method,
                'safety_flags': text_results.get('safety_flags', {}) if text_results else {},
                'recommendations_priority': self._get_recommendation_priority(risk_assessment['level'])
            }
            
        except Exception as e:
            logger.error("Advanced fusion failed", error=str(e))
            raise ValueError(f"Advanced prediction fusion failed: {str(e)}")
    
    def _attention_fusion(
        self, 
        eeg_results: Optional[Dict], 
        text_results: Optional[Dict],
        user_calibration: Optional[Dict[str, float]]
    ) -> Dict[str, Any]:
        """Attention-weighted fusion"""
        
        # Get attention weights
        weights = self._get_attention_weights(eeg_results, text_results, user_calibration)
        
        # Fuse emotion predictions
        emotion_fusion = self._fuse_with_attention(
            eeg_results.get('emotion') if eeg_results else None,
            self._text_to_emotion(text_results) if text_results else None,
            weights['emotion']
        )
        
        # Fuse anxiety predictions
        anxiety_fusion = self._fuse_with_attention(
            eeg_results.get('anxiety') if eeg_results else None,
            self._text_to_anxiety(text_results) if text_results else None,
            weights['anxiety']
        )
        
        return {
            'emotion': emotion_fusion,
            'anxiety': anxiety_fusion,
            'importance': weights
        }
    
    def _bayesian_fusion(
        self, 
        eeg_results: Optional[Dict], 
        text_results: Optional[Dict]
    ) -> Dict[str, Any]:
        """Bayesian fusion with priors"""
        
        # Emotion fusion
        emotion_posterior = self._bayesian_update(
            eeg_results.get('emotion') if eeg_results else None,
            self._text_to_emotion(text_results) if text_results else None,
            self.priors['emotion']
        )
        
        # Anxiety fusion
        anxiety_posterior = self._bayesian_update(
            eeg_results.get('anxiety') if eeg_results else None,
            self._text_to_anxiety(text_results) if text_results else None,
            self.priors['anxiety']
        )
        
        return {
            'emotion': emotion_posterior,
            'anxiety': anxiety_posterior,
            'importance': {'method': 'bayesian', 'priors_used': True}
        }
    
    def _ensemble_fusion(
        self, 
        eeg_results: Optional[Dict], 
        text_results: Optional[Dict]
    ) -> Dict[str, Any]:
        """Ensemble fusion combining multiple methods"""
        
        # Get results from both methods
        attention_results = self._attention_fusion(eeg_results, text_results, None)
        bayesian_results = self._bayesian_fusion(eeg_results, text_results)
        
        # Ensemble the results
        emotion_ensemble = self._ensemble_predictions(
            attention_results['emotion'],
            bayesian_results['emotion']
        )
        
        anxiety_ensemble = self._ensemble_predictions(
            attention_results['anxiety'],
            bayesian_results['anxiety']
        )
        
        return {
            'emotion': emotion_ensemble,
            'anxiety': anxiety_ensemble,
            'importance': {'method': 'ensemble', 'components': ['attention', 'bayesian']}
        }
    
    def _get_attention_weights(
        self, 
        eeg_results: Optional[Dict], 
        text_results: Optional[Dict],
        user_calibration: Optional[Dict[str, float]]
    ) -> Dict[str, Dict[str, float]]:
        """Calculate dynamic attention weights"""
        
        base_weights = {
            'emotion': {'eeg': 0.7, 'text': 0.3},
            'anxiety': {'eeg': 0.8, 'text': 0.2}
        }
        
        # Adjust based on confidence
        if eeg_results and text_results:
            eeg_emotion_conf = eeg_results.get('emotion', {}).get('confidence', 0.5)
            text_emotion_conf = text_results.get('sentiment', {}).get('score', 0.5)
            
            # Higher confidence gets more weight
            total_conf = eeg_emotion_conf + text_emotion_conf
            if total_conf > 0:
                base_weights['emotion']['eeg'] = eeg_emotion_conf / total_conf
                base_weights['emotion']['text'] = text_emotion_conf / total_conf
        
        # Apply user calibration
        if user_calibration:
            for modality in base_weights:
                for source in base_weights[modality]:
                    key = f"{source}_{modality}_weight"
                    if key in user_calibration:
                        base_weights[modality][source] = user_calibration[key]
        
        return base_weights
    
    def _fuse_with_attention(
        self, 
        eeg_pred: Optional[Dict], 
        text_pred: Optional[Dict],
        weights: Dict[str, float]
    ) -> Dict[str, Any]:
        """Fuse predictions using attention weights"""
        
        if eeg_pred and text_pred:
            # Weighted average of probabilities
            eeg_probs = np.array(list(eeg_pred.get('probabilities', {}).values()))
            text_probs = np.array(list(text_pred.get('probabilities', {}).values()))
            
            fused_probs = weights['eeg'] * eeg_probs + weights['text'] * text_probs
            
            # Get class names (assuming same order)
            classes = list(eeg_pred.get('probabilities', {}).keys())
            
            # Find best class
            best_idx = np.argmax(fused_probs)
            best_class = classes[best_idx]
            confidence = float(fused_probs[best_idx])
            
            return {
                'label': best_class,
                'confidence': confidence,
                'probabilities': {cls: float(prob) for cls, prob in zip(classes, fused_probs)},
                'agreement': eeg_pred.get('label') == text_pred.get('label'),
                'weights_used': weights
            }
        
        elif eeg_pred:
            return eeg_pred
        elif text_pred:
            return text_pred
        else:
            return {'label': 'neutral', 'confidence': 0.3}
    
    def _bayesian_update(
        self, 
        eeg_pred: Optional[Dict], 
        text_pred: Optional[Dict],
        prior: Dict[str, float]
    ) -> Dict[str, Any]:
        """Bayesian update with priors"""
        
        # Start with prior
        posterior = np.array(list(prior.values()))
        classes = list(prior.keys())
        
        # Update with EEG likelihood
        if eeg_pred:
            eeg_probs = np.array([eeg_pred.get('probabilities', {}).get(cls, 1/len(classes)) 
                                 for cls in classes])
            posterior *= eeg_probs
        
        # Update with text likelihood
        if text_pred:
            text_probs = np.array([text_pred.get('probabilities', {}).get(cls, 1/len(classes)) 
                                  for cls in classes])
            posterior *= text_probs
        
        # Normalize
        posterior = posterior / np.sum(posterior)
        
        # Find best class
        best_idx = np.argmax(posterior)
        best_class = classes[best_idx]
        confidence = float(posterior[best_idx])
        
        return {
            'label': best_class,
            'confidence': confidence,
            'probabilities': {cls: float(prob) for cls, prob in zip(classes, posterior)},
            'method': 'bayesian'
        }
    
    def _ensemble_predictions(self, pred1: Dict, pred2: Dict) -> Dict[str, Any]:
        """Ensemble two predictions"""
        
        if not pred1 or not pred2:
            return pred1 or pred2 or {'label': 'neutral', 'confidence': 0.3}
        
        # Average probabilities
        classes = list(pred1.get('probabilities', {}).keys())
        probs1 = np.array(list(pred1.get('probabilities', {}).values()))
        probs2 = np.array(list(pred2.get('probabilities', {}).values()))
        
        ensemble_probs = (probs1 + probs2) / 2
        
        best_idx = np.argmax(ensemble_probs)
        best_class = classes[best_idx]
        confidence = float(ensemble_probs[best_idx])
        
        return {
            'label': best_class,
            'confidence': confidence,
            'probabilities': {cls: float(prob) for cls, prob in zip(classes, ensemble_probs)},
            'method': 'ensemble'
        }
    
    def _text_to_emotion(self, text_results: Optional[Dict]) -> Optional[Dict]:
        """Convert text sentiment to emotion format"""
        if not text_results:
            return None
        
        sentiment = text_results.get('sentiment', {})
        sentiment_label = sentiment.get('label', 'neutral')
        
        # Map sentiment to emotion
        emotion_mapping = {
            'positive': 'happy',
            'negative': 'sad',
            'neutral': 'neutral'
        }
        
        emotion_label = emotion_mapping.get(sentiment_label, 'neutral')
        
        return {
            'label': emotion_label,
            'confidence': sentiment.get('score', 0.5),
            'probabilities': {
                'happy': 0.8 if emotion_label == 'happy' else 0.1,
                'sad': 0.8 if emotion_label == 'sad' else 0.1,
                'neutral': 0.8 if emotion_label == 'neutral' else 0.1,
                'stressed': 0.1,
                'relaxed': 0.1
            }
        }
    
    def _text_to_anxiety(self, text_results: Optional[Dict]) -> Optional[Dict]:
        """Convert text anxiety keywords to anxiety format"""
        if not text_results:
            return None
        
        anxiety_keywords = text_results.get('anxiety_keywords', {})
        level = anxiety_keywords.get('level', 'low')
        
        return {
            'label': level,
            'confidence': 0.7,
            'probabilities': {
                'low': 0.8 if level == 'low' else 0.1,
                'moderate': 0.8 if level == 'moderate' else 0.1,
                'high': 0.8 if level == 'high' else 0.1
            }
        }
    
    def _apply_safety_rules(
        self, 
        eeg_results: Optional[Dict], 
        text_results: Optional[Dict]
    ) -> Optional[Dict[str, Any]]:
        """Apply safety-first rules that override fusion"""
        
        # Crisis detection from text
        if text_results and text_results.get('safety_flags', {}).get('has_crisis_indicators'):
            logger.warning("Crisis indicators detected - applying safety override")
            return {
                'risk_level': 'high',
                'confidence': 0.95,
                'safety_override': True,
                'explanation': [
                    "Crisis indicators detected in text input",
                    "Immediate professional help recommended",
                    "Safety is the top priority"
                ],
                'emergency_resources': True
            }
        
        # Severe depression from text
        if (text_results and 
            text_results.get('depression', {}).get('label') == 'severe' and
            text_results.get('depression', {}).get('confidence', 0) > 0.7):
            
            logger.warning("Severe depression detected - applying safety override")
            return {
                'risk_level': 'high',
                'confidence': 0.9,
                'safety_override': True,
                'explanation': [
                    "Severe depression indicators in text analysis",
                    "Professional evaluation recommended within 24-48 hours",
                    "This assessment is for guidance only, not diagnosis"
                ]
            }
        
        return None
    
    def _assess_risk_level_advanced(
        self, 
        fusion_results: Dict, 
        text_results: Optional[Dict]
    ) -> Dict[str, Any]:
        """Advanced risk assessment with multiple factors"""
        
        risk_factors = []
        
        # Emotion risk
        emotion = fusion_results.get('emotion', {})
        if emotion.get('label') in ['sad', 'stressed']:
            risk_factors.append(2 if emotion.get('confidence', 0) > 0.7 else 1)
        
        # Anxiety risk
        anxiety = fusion_results.get('anxiety', {})
        anxiety_levels = {'low': 0, 'moderate': 1, 'high': 2}
        risk_factors.append(anxiety_levels.get(anxiety.get('label', 'low'), 0))
        
        # Depression risk from text
        if text_results:
            depression = text_results.get('depression', {})
            depression_levels = {'not_depressed': 0, 'moderate': 1, 'severe': 2}
            risk_factors.append(depression_levels.get(depression.get('label', 'not_depressed'), 0))
        
        # Calculate weighted risk score
        weights = [0.3, 0.4, 0.3]  # emotion, anxiety, depression
        risk_score = sum(w * r for w, r in zip(weights, risk_factors)) / sum(weights)
        
        # Map to risk levels
        if risk_score >= 1.5:
            level = 'high'
            confidence = 0.85
        elif risk_score >= 1.0:
            level = 'moderate'
            confidence = 0.75
        elif risk_score >= 0.5:
            level = 'mild'
            confidence = 0.65
        else:
            level = 'stable'
            confidence = 0.7
        
        return {
            'level': level,
            'confidence': confidence,
            'risk_score': risk_score,
            'risk_factors': risk_factors
        }
    
    def _generate_explanation_with_importance(
        self,
        eeg_results: Optional[Dict],
        text_results: Optional[Dict],
        fusion_results: Dict,
        risk_assessment: Dict
    ) -> List[str]:
        """Generate explanations with feature importance"""
        
        explanations = []
        
        # Feature importance explanation
        importance = fusion_results.get('importance', {})
        if 'eeg' in importance and 'text' in importance:
            eeg_weight = importance.get('eeg', 0.5)
            text_weight = importance.get('text', 0.5)
            
            if eeg_weight > text_weight:
                explanations.append(
                    f"EEG patterns were weighted more heavily ({eeg_weight:.1%}) in this analysis"
                )
            else:
                explanations.append(
                    f"Text analysis was weighted more heavily ({text_weight:.1%}) in this analysis"
                )
        
        # Specific findings
        emotion = fusion_results.get('emotion', {})
        anxiety = fusion_results.get('anxiety', {})
        
        if emotion.get('label'):
            explanations.append(
                f"Combined analysis indicates {emotion.get('label')} emotional state "
                f"with {emotion.get('confidence', 0)*100:.0f}% confidence"
            )
        
        if anxiety.get('label'):
            explanations.append(
                f"Anxiety level assessed as {anxiety.get('label')} "
                f"with {anxiety.get('confidence', 0)*100:.0f}% confidence"
            )
        
        # Risk explanation
        risk_level = risk_assessment['level']
        risk_score = risk_assessment.get('risk_score', 0)
        
        explanations.append(
            f"Overall risk assessment: {risk_level} (score: {risk_score:.2f}/2.0)"
        )
        
        # Method explanation
        method = fusion_results.get('importance', {}).get('method', 'attention')
        explanations.append(f"Analysis used {method} fusion method for optimal accuracy")
        
        return explanations
    
    def _get_recommendation_priority(self, risk_level: str) -> str:
        """Map risk level to recommendation priority"""
        priority_map = {
            'stable': 'maintenance',
            'mild': 'prevention',
            'moderate': 'intervention',
            'high': 'crisis'
        }
        return priority_map.get(risk_level, 'prevention')