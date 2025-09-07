"""
Natural language explanation generation for EEG results
"""
from typing import Dict, List, Any, Optional
import structlog

logger = structlog.get_logger(__name__)

class ExplanationGenerator:
    """Generate user-friendly explanations for EEG and text analysis results"""
    
    def __init__(self):
        self.band_interpretations = {
            'delta': {
                'high': "Delta waves are elevated, which can indicate deep relaxation or fatigue",
                'normal': "Delta wave activity is within normal range",
                'low': "Delta waves are reduced, suggesting alert wakefulness"
            },
            'theta': {
                'high': "Theta waves are prominent, often associated with creativity and deep meditation",
                'normal': "Theta wave activity is balanced",
                'low': "Theta waves are minimal, indicating focused attention"
            },
            'alpha': {
                'high': "Alpha waves are strong, suggesting a relaxed and calm mental state",
                'normal': "Alpha wave activity is balanced",
                'low': "Alpha waves are reduced, which may indicate stress or active concentration"
            },
            'beta': {
                'high': "Beta waves are elevated, indicating active thinking but possibly stress or anxiety",
                'normal': "Beta wave activity shows normal cognitive engagement",
                'low': "Beta waves are low, suggesting a very relaxed state"
            },
            'gamma': {
                'high': "Gamma waves are increased, associated with high-level cognitive processing",
                'normal': "Gamma wave activity is within expected range",
                'low': "Gamma waves are minimal"
            }
        }
        
        self.emotion_descriptions = {
            'happy': "patterns associated with positive emotional state",
            'sad': "patterns that may indicate low mood or sadness",
            'neutral': "balanced emotional patterns",
            'stressed': "patterns suggesting stress or tension",
            'relaxed': "patterns indicating relaxation and calm"
        }
        
        self.anxiety_descriptions = {
            'low': "minimal anxiety indicators",
            'moderate': "some signs of anxiety or worry", 
            'high': "significant anxiety patterns detected"
        }
        
        self.depression_descriptions = {
            'not_depressed': "no significant depression indicators",
            'moderate': "some depression indicators present",
            'severe': "concerning depression indicators detected"
        }
    
    def generate_eeg_explanation(
        self, 
        eeg_features: Dict[str, Any], 
        predictions: Dict[str, Any]
    ) -> List[str]:
        """Generate explanation for EEG analysis results"""
        
        explanations = []
        
        try:
            # Band power explanations
            band_powers = eeg_features.get('features', {}).get('band_powers', {}).get('mean', {})
            
            if band_powers:
                # Determine which bands are elevated/reduced
                band_levels = self._categorize_band_levels(band_powers)
                
                for band, level in band_levels.items():
                    if level != 'normal':
                        explanation = self.band_interpretations[band][level]
                        explanations.append(explanation)
            
            # Alpha/beta ratio interpretation
            spectral_features = eeg_features.get('features', {}).get('spectral_features', {}).get('mean', {})
            if 'alpha_beta_ratio' in spectral_features:
                ratio = spectral_features['alpha_beta_ratio']
                if ratio > 1.2:
                    explanations.append("High alpha-to-beta ratio suggests good relaxation capacity")
                elif ratio < 0.8:
                    explanations.append("Low alpha-to-beta ratio may indicate mental tension or alertness")
            
            # Emotion prediction explanation
            if 'emotion' in predictions:
                emotion = predictions['emotion']
                emotion_desc = self.emotion_descriptions.get(emotion['label'], 'unknown patterns')
                confidence = emotion['confidence'] * 100
                
                explanations.append(
                    f"EEG signals show {emotion_desc} with {confidence:.0f}% confidence"
                )
            
            # Anxiety prediction explanation
            if 'anxiety' in predictions:
                anxiety = predictions['anxiety']
                anxiety_desc = self.anxiety_descriptions.get(anxiety['label'], 'unknown level')
                confidence = anxiety['confidence'] * 100
                
                explanations.append(
                    f"Analysis indicates {anxiety_desc} ({confidence:.0f}% confidence)"
                )
            
            # Technical quality notes
            metadata = eeg_features.get('metadata', {})
            n_epochs = metadata.get('n_epochs', 0)
            if n_epochs < 10:
                explanations.append(
                    f"Note: Analysis based on {n_epochs} epochs - longer recordings may provide more reliable results"
                )
            
        except Exception as e:
            logger.error("EEG explanation generation failed", error=str(e))
            explanations.append("EEG analysis completed - detailed interpretation unavailable")
        
        return explanations
    
    def generate_text_explanation(self, text_results: Dict[str, Any]) -> List[str]:
        """Generate explanation for text analysis results"""
        
        explanations = []
        
        try:
            # Safety flags
            safety_flags = text_results.get('safety_flags', {})
            if safety_flags.get('has_crisis_indicators'):
                explanations.append(
                    "Crisis language detected - please reach out for immediate professional support"
                )
                return explanations  # Don't add other explanations for crisis cases
            
            # Depression analysis
            depression = text_results.get('depression', {})
            if depression:
                label = depression['label']
                confidence = depression['confidence'] * 100
                desc = self.depression_descriptions.get(label, 'unclear patterns')
                
                explanations.append(
                    f"Text analysis shows {desc} ({confidence:.0f}% confidence)"
                )
                
                # Add context based on keyword scores
                keyword_scores = depression.get('keyword_scores', {})
                if keyword_scores.get('severe', 0) > 0:
                    explanations.append(
                        "Language patterns suggest significant emotional distress"
                    )
                elif keyword_scores.get('positive', 0) > keyword_scores.get('moderate', 0):
                    explanations.append(
                        "Positive language indicators suggest resilience and coping"
                    )
            
            # Sentiment analysis
            sentiment = text_results.get('sentiment', {})
            if sentiment:
                sentiment_label = sentiment['label']
                score = sentiment['score'] * 100
                
                if sentiment_label == 'negative' and score > 70:
                    explanations.append(f"Overall sentiment is negative ({score:.0f}% confidence)")
                elif sentiment_label == 'positive' and score > 70:
                    explanations.append(f"Overall sentiment is positive ({score:.0f}% confidence)")
            
            # Anxiety keywords
            anxiety_keywords = text_results.get('anxiety_keywords', {})
            if anxiety_keywords:
                level = anxiety_keywords['level']
                total_words = anxiety_keywords['scores'].get('moderate', 0) + anxiety_keywords['scores'].get('high', 0)
                
                if level == 'high' and total_words > 2:
                    explanations.append("Multiple anxiety-related terms suggest heightened worry or stress")
                elif level == 'low' and anxiety_keywords['scores'].get('low', 0) > 0:
                    explanations.append("Language suggests calm and stable emotional state")
            
        except Exception as e:
            logger.error("Text explanation generation failed", error=str(e))
            explanations.append("Text analysis completed - detailed interpretation unavailable")
        
        return explanations
    
    def generate_fusion_explanation(
        self, 
        fusion_results: Dict[str, Any],
        eeg_explanations: List[str],
        text_explanations: List[str]
    ) -> List[str]:
        """Generate explanation for fused results"""
        
        explanations = []
        
        try:
            # Safety override explanation
            if fusion_results.get('safety_override'):
                return fusion_results.get('explanation', ['Safety protocols activated'])
            
            # Overall risk assessment
            risk_level = fusion_results.get('risk_level', 'stable')
            confidence = fusion_results.get('confidence', 0.5) * 100
            
            risk_descriptions = {
                'stable': 'stable mental state with no immediate concerns',
                'mild': 'mild concerns that may benefit from self-care attention',
                'moderate': 'moderate risk requiring active coping strategies and monitoring',
                'high': 'elevated risk requiring professional evaluation and support'
            }
            
            desc = risk_descriptions.get(risk_level, 'unclear risk level')
            explanations.append(f"Combined analysis suggests {desc} ({confidence:.0f}% confidence)")
            
            # Agreement between modalities
            emotion_fusion = fusion_results.get('emotion_fusion', {})
            anxiety_fusion = fusion_results.get('anxiety_fusion', {})
            
            agreement_count = 0
            if emotion_fusion.get('agreement'):
                agreement_count += 1
            if anxiety_fusion.get('agreement'):
                agreement_count += 1
            
            if agreement_count == 2:
                explanations.append("EEG signals and text analysis show consistent findings, increasing confidence")
            elif agreement_count == 1:
                explanations.append("Partial agreement between EEG and text analyses")
            else:
                explanations.append("Some differences between EEG and text analyses - this is normal and both perspectives are valuable")
            
            # Specific fusion insights
            if emotion_fusion.get('label'):
                emotion_confidence = emotion_fusion.get('confidence', 0.5) * 100
                explanations.append(
                    f"Emotional state assessment: {emotion_fusion['label']} ({emotion_confidence:.0f}% confidence)"
                )
            
            if anxiety_fusion.get('label'):
                anxiety_confidence = anxiety_fusion.get('confidence', 0.5) * 100
                explanations.append(
                    f"Anxiety level assessment: {anxiety_fusion['label']} ({anxiety_confidence:.0f}% confidence)"
                )
            
            # Recommendations priority
            rec_priority = fusion_results.get('recommendations_priority', 'prevention')
            if rec_priority == 'crisis':
                explanations.append("Immediate action recommended - please prioritize safety and professional support")
            elif rec_priority == 'intervention':
                explanations.append("Active intervention strategies recommended to address current concerns")
            elif rec_priority == 'prevention':
                explanations.append("Preventive care and routine wellness practices recommended")
            
        except Exception as e:
            logger.error("Fusion explanation generation failed", error=str(e))
            explanations.append("Combined analysis completed - detailed interpretation unavailable")
        
        return explanations
    
    def _categorize_band_levels(self, band_powers: Dict[str, float]) -> Dict[str, str]:
        """Categorize band power levels as high/normal/low"""
        
        # These thresholds would be calibrated from population data
        # For demonstration, using relative comparisons
        
        levels = {}
        total_power = sum(band_powers.values())
        
        if total_power == 0:
            return {band: 'normal' for band in band_powers.keys()}
        
        # Calculate relative powers
        relative_powers = {band: power / total_power for band, power in band_powers.items()}
        
        # Expected relative distributions (approximate)
        expected = {
            'delta': 0.15,
            'theta': 0.20, 
            'alpha': 0.35,
            'beta': 0.25,
            'gamma': 0.05
        }
        
        for band, rel_power in relative_powers.items():
            expected_power = expected.get(band, 0.2)
            
            if rel_power > expected_power * 1.3:
                levels[band] = 'high'
            elif rel_power < expected_power * 0.7:
                levels[band] = 'low'
            else:
                levels[band] = 'normal'
        
        return levels