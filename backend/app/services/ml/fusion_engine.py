"""
Fusion engine for combining EEG and text predictions with safety rules
"""
import numpy as np
from typing import Dict, Any, Optional, List
import structlog

logger = structlog.get_logger(__name__)

class FusionEngine:
    """Combines EEG and text predictions with safety-first rules"""
    
    def __init__(self):
        # Default fusion weights (can be calibrated per user)
        self.default_weights = {
            'eeg_weight': 0.6,
            'text_weight': 0.4
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
        user_calibration: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Combine EEG and text predictions with safety rules
        
        Args:
            eeg_results: Output from EEG model
            text_results: Output from text classifier
            user_calibration: Per-user weight adjustments
            
        Returns:
            Fused prediction with risk level and explanations
        """
        
        logger.info("Starting prediction fusion", 
                   has_eeg=bool(eeg_results),
                   has_text=bool(text_results))
        
        try:
            # Apply safety rules first
            safety_override = self._apply_safety_rules(eeg_results, text_results)
            if safety_override:
                return safety_override
            
            # Get fusion weights (use calibration if available)
            weights = self._get_fusion_weights(user_calibration)
            
            # Fuse individual predictions
            emotion_fusion = self._fuse_emotion(eeg_results, text_results, weights)
            anxiety_fusion = self._fuse_anxiety(eeg_results, text_results, weights)
            
            # Determine overall risk level
            risk_assessment = self._assess_risk_level(emotion_fusion, anxiety_fusion, text_results)
            
            # Generate explanation
            explanation = self._generate_explanation(
                eeg_results, text_results, emotion_fusion, anxiety_fusion, risk_assessment
            )
            
            return {
                'risk_level': risk_assessment['level'],
                'confidence': risk_assessment['confidence'],
                'emotion_fusion': emotion_fusion,
                'anxiety_fusion': anxiety_fusion,
                'explanation': explanation,
                'weights_used': weights,
                'safety_flags': text_results.get('safety_flags', {}) if text_results else {},
                'recommendations_priority': self._get_recommendation_priority(risk_assessment['level'])
            }
            
        except Exception as e:
            logger.error("Fusion failed", error=str(e))
            raise ValueError(f"Prediction fusion failed: {str(e)}")
    
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
    
    def _get_fusion_weights(self, user_calibration: Optional[Dict[str, float]]) -> Dict[str, float]:
        """Get fusion weights with optional user calibration"""
        if user_calibration:
            return {
                'eeg_weight': user_calibration.get('eeg_weight', self.default_weights['eeg_weight']),
                'text_weight': user_calibration.get('text_weight', self.default_weights['text_weight'])
            }
        return self.default_weights.copy()
    
    def _fuse_emotion(
        self, 
        eeg_results: Optional[Dict], 
        text_results: Optional[Dict], 
        weights: Dict[str, float]
    ) -> Dict[str, Any]:
        """Fuse emotion predictions"""
        
        if eeg_results and text_results:
            # Late fusion of probabilities
            eeg_emotion = eeg_results.get('emotion', {})
            text_sentiment = text_results.get('sentiment', {})
            
            # Map sentiment to emotion (simplified)
            emotion_mapping = {
                'positive': 'happy',
                'negative': 'sad',
                'neutral': 'neutral'
            }
            
            text_emotion_label = emotion_mapping.get(text_sentiment.get('label'), 'neutral')
            
            # Simple fusion (in production, use learned weights)
            if eeg_emotion.get('label') == text_emotion_label:
                confidence = min(0.95, 
                    weights['eeg_weight'] * eeg_emotion.get('confidence', 0.5) + 
                    weights['text_weight'] * text_sentiment.get('score', 0.5)
                )
                return {
                    'label': eeg_emotion.get('label'),
                    'confidence': confidence,
                    'agreement': True
                }
            else:
                # Disagreement - favor higher confidence
                if eeg_emotion.get('confidence', 0) > text_sentiment.get('score', 0):
                    return {
                        'label': eeg_emotion.get('label'),
                        'confidence': eeg_emotion.get('confidence', 0.5) * weights['eeg_weight'],
                        'agreement': False
                    }
                else:
                    return {
                        'label': text_emotion_label,
                        'confidence': text_sentiment.get('score', 0.5) * weights['text_weight'],
                        'agreement': False
                    }
        
        elif eeg_results:
            return eeg_results.get('emotion', {})
        elif text_results:
            sentiment = text_results.get('sentiment', {})
            emotion_mapping = {'positive': 'happy', 'negative': 'sad', 'neutral': 'neutral'}
            return {
                'label': emotion_mapping.get(sentiment.get('label'), 'neutral'),
                'confidence': sentiment.get('score', 0.5)
            }
        
        return {'label': 'neutral', 'confidence': 0.3}
    
    def _fuse_anxiety(
        self, 
        eeg_results: Optional[Dict], 
        text_results: Optional[Dict], 
        weights: Dict[str, float]
    ) -> Dict[str, Any]:
        """Fuse anxiety predictions"""
        
        if eeg_results and text_results:
            eeg_anxiety = eeg_results.get('anxiety', {})
            text_anxiety = text_results.get('anxiety_keywords', {})
            
            # Convert text anxiety to same scale
            text_level = text_anxiety.get('level', 'low')
            
            if eeg_anxiety.get('label') == text_level:
                confidence = min(0.9,
                    weights['eeg_weight'] * eeg_anxiety.get('confidence', 0.5) + 
                    weights['text_weight'] * 0.7
                )
                return {
                    'label': eeg_anxiety.get('label'),
                    'confidence': confidence,
                    'agreement': True
                }
            else:
                # Take higher severity
                eeg_severity = ['low', 'moderate', 'high'].index(eeg_anxiety.get('label', 'low'))
                text_severity = ['low', 'moderate', 'high'].index(text_level)
                
                if eeg_severity >= text_severity:
                    return {
                        'label': eeg_anxiety.get('label'),
                        'confidence': eeg_anxiety.get('confidence', 0.5) * weights['eeg_weight'],
                        'agreement': False
                    }
                else:
                    return {
                        'label': text_level,
                        'confidence': 0.7 * weights['text_weight'],
                        'agreement': False
                    }
        
        elif eeg_results:
            return eeg_results.get('anxiety', {})
        elif text_results:
            text_anxiety = text_results.get('anxiety_keywords', {})
            return {
                'label': text_anxiety.get('level', 'low'),
                'confidence': 0.6
            }
        
        return {'label': 'low', 'confidence': 0.3}
    
    def _assess_risk_level(
        self, 
        emotion_fusion: Dict, 
        anxiety_fusion: Dict, 
        text_results: Optional[Dict]
    ) -> Dict[str, Any]:
        """Assess overall mental health risk level"""
        
        risk_scores = []
        
        # Emotion contribution
        emotion_label = emotion_fusion.get('label', 'neutral')
        if emotion_label in ['sad', 'stressed']:
            risk_scores.append(2)
        elif emotion_label == 'neutral':
            risk_scores.append(1)
        else:
            risk_scores.append(0)
        
        # Anxiety contribution
        anxiety_label = anxiety_fusion.get('label', 'low')
        anxiety_score = ['low', 'moderate', 'high'].index(anxiety_label)
        risk_scores.append(anxiety_score)
        
        # Depression contribution from text
        if text_results:
            depression = text_results.get('depression', {})
            depression_label = depression.get('label', 'not_depressed')
            if depression_label == 'severe':
                risk_scores.append(3)
            elif depression_label == 'moderate':
                risk_scores.append(2)
            else:
                risk_scores.append(0)
        
        # Calculate overall risk
        avg_risk = np.mean(risk_scores)
        max_risk = max(risk_scores)
        
        # Risk level determination
        if max_risk >= 3 or avg_risk >= 2.5:
            level = 'high'
            confidence = 0.85
        elif max_risk >= 2 or avg_risk >= 1.5:
            level = 'moderate'
            confidence = 0.75
        elif avg_risk >= 0.5:
            level = 'mild'
            confidence = 0.65
        else:
            level = 'stable'
            confidence = 0.7
        
        return {
            'level': level,
            'confidence': confidence,
            'risk_scores': risk_scores,
            'avg_risk': avg_risk
        }
    
    def _generate_explanation(
        self,
        eeg_results: Optional[Dict],
        text_results: Optional[Dict],
        emotion_fusion: Dict,
        anxiety_fusion: Dict,
        risk_assessment: Dict
    ) -> List[str]:
        """Generate natural language explanations"""
        
        explanations = []
        
        # EEG findings
        if eeg_results:
            emotion = eeg_results.get('emotion', {})
            anxiety = eeg_results.get('anxiety', {})
            
            explanations.append(
                f"EEG patterns suggest {emotion.get('label', 'neutral')} emotional state "
                f"with {anxiety.get('label', 'low')} anxiety level"
            )
        
        # Text findings
        if text_results:
            depression = text_results.get('depression', {})
            sentiment = text_results.get('sentiment', {})
            
            explanations.append(
                f"Text analysis indicates {depression.get('label', 'not_depressed').replace('_', ' ')} "
                f"depression indicators with {sentiment.get('label', 'neutral')} sentiment"
            )
        
        # Agreement/disagreement
        if eeg_results and text_results:
            if emotion_fusion.get('agreement') and anxiety_fusion.get('agreement'):
                explanations.append("EEG and text analyses show consistent findings")
            else:
                explanations.append("Some differences between EEG and text analyses detected")
        
        # Risk level explanation
        risk_level = risk_assessment['level']
        if risk_level == 'high':
            explanations.append(
                "Risk assessment indicates need for professional evaluation and support"
            )
        elif risk_level == 'moderate':
            explanations.append(
                "Moderate risk detected - consider coping strategies and monitoring"
            )
        elif risk_level == 'mild':
            explanations.append(
                "Mild concerns detected - self-care and routine monitoring recommended"
            )
        else:
            explanations.append("Analysis suggests stable mental state")
        
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