import numpy as np
from typing import Dict, Optional, List
import logging
from datetime import datetime

class FusionEngine:
    def __init__(self):
        self.eeg_weight = 0.6  # EEG is more objective
        self.text_weight = 0.4  # Text provides context
        
        # Risk level thresholds
        self.risk_thresholds = {
            'stable': 0.3,
            'mild': 0.5,
            'moderate': 0.7,
            'high': 0.85
        }
        
        # Safety rules (override fusion if triggered)
        self.safety_rules = {
            'crisis_override': True,
            'severe_text_threshold': 0.8,
            'high_anxiety_threshold': 0.8
        }
    
    def fuse_predictions(self, eeg_results: Dict, text_results: Optional[Dict] = None) -> Dict:
        """Fuse EEG and text predictions with safety rules"""
        
        # Initialize fusion result
        fusion_result = {
            'risk_level': 'stable',
            'confidence': 0.0,
            'components': {
                'eeg_contribution': 0.0,
                'text_contribution': 0.0
            },
            'explanation': [],
            'recommendations': [],
            'safety_triggered': False,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        try:
            # Extract EEG components
            eeg_emotion_conf = eeg_results.get('emotion', {}).get('confidence', 0.0)
            eeg_anxiety_score = eeg_results.get('anxiety', {}).get('score', 0.0)
            eeg_anxiety_level = eeg_results.get('anxiety', {}).get('label', 'low')
            
            # Calculate EEG risk score
            eeg_risk_score = self._calculate_eeg_risk(eeg_results)
            fusion_result['components']['eeg_contribution'] = eeg_risk_score
            
            # Handle text results if available
            text_risk_score = 0.0
            if text_results and text_results.get('depression'):
                text_risk_score = self._calculate_text_risk(text_results)
                fusion_result['components']['text_contribution'] = text_risk_score
                
                # Check safety rules
                safety_check = self._check_safety_rules(text_results, eeg_results)
                if safety_check['triggered']:
                    fusion_result.update(safety_check)
                    return fusion_result
            
            # Calculate weighted fusion score
            if text_results:
                final_risk_score = (
                    self.eeg_weight * eeg_risk_score + 
                    self.text_weight * text_risk_score
                )
            else:
                final_risk_score = eeg_risk_score
                fusion_result['components']['text_contribution'] = 0.0
            
            # Determine risk level
            risk_level, confidence = self._determine_risk_level(final_risk_score)
            fusion_result['risk_level'] = risk_level
            fusion_result['confidence'] = confidence
            
            # Generate explanations and recommendations
            fusion_result['explanation'] = self._generate_explanation(
                eeg_results, text_results, risk_level
            )
            fusion_result['recommendations'] = self._generate_recommendations(risk_level)
            
        except Exception as e:
            logging.error(f"Error in fusion engine: {str(e)}")
            fusion_result.update({
                'risk_level': 'unknown',
                'confidence': 0.0,
                'error': str(e)
            })
        
        return fusion_result
    
    def _calculate_eeg_risk(self, eeg_results: Dict) -> float:
        """Calculate risk score from EEG results"""
        risk_score = 0.0
        
        # Emotion contribution
        emotion = eeg_results.get('emotion', {})
        emotion_label = emotion.get('label', 'unknown')
        emotion_conf = emotion.get('confidence', 0.0)
        
        emotion_risk_map = {
            'stressed': 0.8,
            'angry': 0.7,
            'sad': 0.6,
            'neutral': 0.3,
            'happy': 0.1,
            'relaxed': 0.1
        }
        
        emotion_risk = emotion_risk_map.get(emotion_label, 0.5) * emotion_conf
        
        # Anxiety contribution
        anxiety = eeg_results.get('anxiety', {})
        anxiety_score = anxiety.get('score', 0.0)
        anxiety_level = anxiety.get('label', 'low')
        
        anxiety_risk_map = {
            'high': 0.9,
            'moderate': 0.6,
            'low': 0.2
        }
        
        anxiety_risk = anxiety_risk_map.get(anxiety_level, 0.5) * anxiety_score
        
        # Combine emotion and anxiety (weighted average)
        risk_score = 0.4 * emotion_risk + 0.6 * anxiety_risk
        
        return min(risk_score, 1.0)
    
    def _calculate_text_risk(self, text_results: Dict) -> float:
        """Calculate risk score from text analysis"""
        depression = text_results.get('depression', {})
        anxiety = text_results.get('anxiety', {})
        
        # Depression risk
        depression_label = depression.get('label', 'minimal')
        depression_conf = depression.get('confidence', 0.0)
        
        depression_risk_map = {
            'severe': 0.9,
            'moderate': 0.7,
            'mild': 0.4,
            'minimal': 0.1
        }
        
        depression_risk = depression_risk_map.get(depression_label, 0.3) * depression_conf
        
        # Anxiety risk
        anxiety_label = anxiety.get('label', 'low')
        anxiety_conf = anxiety.get('confidence', 0.0)
        
        anxiety_risk_map = {
            'high': 0.8,
            'moderate': 0.5,
            'low': 0.2
        }
        
        anxiety_risk = anxiety_risk_map.get(anxiety_label, 0.3) * anxiety_conf
        
        # Combine depression and anxiety
        risk_score = 0.7 * depression_risk + 0.3 * anxiety_risk
        
        return min(risk_score, 1.0)
    
    def _check_safety_rules(self, text_results: Dict, eeg_results: Dict) -> Dict:
        """Check safety override rules"""
        safety_result = {
            'triggered': False,
            'risk_level': 'high',
            'confidence': 0.9,
            'safety_triggered': True,
            'explanation': ['Safety protocols activated'],
            'recommendations': []
        }
        
        # Crisis detection override
        if text_results.get('crisis', {}).get('detected', False):
            safety_result['triggered'] = True
            safety_result['explanation'] = [
                'Crisis indicators detected in text input',
                'Immediate professional support recommended'
            ]
            safety_result['recommendations'] = [
                'Contact emergency services if in immediate danger',
                'Reach out to crisis helpline',
                'Consult with mental health professional immediately'
            ]
            return safety_result
        
        # Severe depression override
        depression = text_results.get('depression', {})
        if (depression.get('label') == 'severe' and 
            depression.get('confidence', 0.0) > self.safety_rules['severe_text_threshold']):
            safety_result['triggered'] = True
            safety_result['explanation'] = [
                'Severe depression indicators detected',
                'Professional evaluation strongly recommended'
            ]
            safety_result['recommendations'] = [
                'Schedule appointment with mental health professional',
                'Consider reaching out to trusted friend or family',
                'Monitor mood closely over next few days'
            ]
            return safety_result
        
        return safety_result
    
    def _determine_risk_level(self, risk_score: float) -> tuple:
        """Determine risk level from fusion score"""
        if risk_score >= self.risk_thresholds['high']:
            return 'high', min(risk_score, 0.95)
        elif risk_score >= self.risk_thresholds['moderate']:
            return 'moderate', risk_score
        elif risk_score >= self.risk_thresholds['mild']:
            return 'mild', risk_score
        else:
            return 'stable', max(risk_score, 0.5)  # Minimum confidence for stable
    
    def _generate_explanation(self, eeg_results: Dict, text_results: Optional[Dict], risk_level: str) -> List[str]:
        """Generate human-readable explanation"""
        explanations = []
        
        # EEG-based explanations
        emotion = eeg_results.get('emotion', {})
        if emotion.get('label') in ['stressed', 'angry']:
            explanations.append(f"EEG patterns indicate {emotion['label']} emotional state")
        
        anxiety = eeg_results.get('anxiety', {})
        if anxiety.get('label') == 'high':
            explanations.append("Elevated anxiety markers detected in brain activity")
        elif anxiety.get('label') == 'moderate':
            explanations.append("Moderate anxiety levels observed in EEG signals")
        
        # Text-based explanations
        if text_results:
            depression = text_results.get('depression', {})
            if depression.get('label') in ['moderate', 'severe']:
                explanations.append(f"Text analysis suggests {depression['label']} depressive symptoms")
            
            if text_results.get('anxiety', {}).get('label') == 'high':
                explanations.append("High anxiety levels expressed in written responses")
        
        # Risk level summary
        if risk_level == 'high':
            explanations.append("Combined indicators suggest elevated mental health risk")
        elif risk_level == 'moderate':
            explanations.append("Multiple factors indicate moderate concern level")
        elif risk_level == 'mild':
            explanations.append("Some indicators present but generally manageable")
        else:
            explanations.append("Current state appears stable with low risk indicators")
        
        return explanations
    
    def _generate_recommendations(self, risk_level: str) -> List[str]:
        """Generate personalized recommendations based on risk level"""
        recommendations = {
            'stable': [
                "Continue current wellness practices",
                "Regular exercise and good sleep hygiene",
                "Maintain social connections"
            ],
            'mild': [
                "Practice daily mindfulness or meditation",
                "Engage in regular physical activity",
                "Consider talking to a trusted friend or counselor"
            ],
            'moderate': [
                "Schedule consultation with mental health professional",
                "Implement stress reduction techniques",
                "Monitor symptoms closely",
                "Maintain regular sleep schedule"
            ],
            'high': [
                "Seek immediate professional mental health support",
                "Contact healthcare provider or crisis helpline",
                "Inform trusted family member or friend",
                "Avoid making major life decisions",
                "Focus on basic self-care and safety"
            ]
        }
        
        return recommendations.get(risk_level, recommendations['stable'])