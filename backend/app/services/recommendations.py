"""
Personalized recommendation engine for mental health interventions
"""
from typing import Dict, List, Any, Optional
import structlog
import random

logger = structlog.get_logger(__name__)

class RecommendationEngine:
    """Generates personalized mental health recommendations"""
    
    def __init__(self):
        self.intervention_library = self._build_intervention_library()
        self.cultural_adaptations = self._build_cultural_library()
    
    def generate_recommendations(
        self,
        emotion_results: Optional[Dict[str, Any]] = None,
        anxiety_results: Optional[Dict[str, Any]] = None,
        depression_results: Optional[Dict[str, Any]] = None,
        fusion_results: Optional[Dict[str, Any]] = None,
        user_preferences: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Generate personalized recommendations based on analysis results"""
        
        risk_level = 'stable'
        if fusion_results:
            risk_level = fusion_results.get('risk_level', 'stable')
        
        logger.info("Generating recommendations", risk_level=risk_level)
        
        # Get base recommendations for risk level
        base_recommendations = self.intervention_library.get(risk_level, [])
        
        # Filter by anxiety level if available
        anxiety_level = 'low'
        if anxiety_results:
            anxiety_level = anxiety_results.get('label', 'low')
        
        # Filter by emotional state if available
        emotion_state = 'neutral'
        if emotion_results:
            emotion_state = emotion_results.get('label', 'neutral')
        
        # Apply filters and personalization
        filtered_recommendations = self._filter_recommendations(
            base_recommendations,
            anxiety_level=anxiety_level,
            emotion_state=emotion_state,
            user_preferences=user_preferences
        )
        
        # Limit to 3-5 recommendations
        selected_recommendations = self._select_top_recommendations(
            filtered_recommendations, 
            max_count=4
        )
        
        return selected_recommendations
    
    def _build_intervention_library(self) -> Dict[str, List[Dict[str, Any]]]:
        """Build library of evidence-based interventions"""
        
        return {
            'stable': [
                {
                    'id': 'maintenance_mindfulness',
                    'title': '5-Minute Morning Mindfulness',
                    'description': 'Start your day with focused breathing and intention setting',
                    'duration_minutes': 5,
                    'type': 'mindfulness',
                    'evidence_level': 'high',
                    'instructions': [
                        'Find a comfortable seated position',
                        'Focus on your breath for 3 minutes',
                        'Set a positive intention for the day',
                        'Notice how you feel before and after'
                    ],
                    'tags': ['morning', 'prevention', 'routine']
                },
                {
                    'id': 'gratitude_practice',
                    'title': 'Three Good Things',
                    'description': 'Write down three positive things from your day',
                    'duration_minutes': 3,
                    'type': 'journaling',
                    'evidence_level': 'high',
                    'instructions': [
                        'At the end of each day, write down three things that went well',
                        'Include why you think each good thing happened',
                        'Reflect on your role in making them happen'
                    ],
                    'tags': ['evening', 'gratitude', 'positive psychology']
                }
            ],
            
            'mild': [
                {
                    'id': 'box_breathing',
                    'title': 'Box Breathing for Calm',
                    'description': '4-4-4-4 breathing pattern to reduce stress',
                    'duration_minutes': 5,
                    'type': 'breathing',
                    'evidence_level': 'high',
                    'instructions': [
                        'Inhale for 4 counts',
                        'Hold for 4 counts', 
                        'Exhale for 4 counts',
                        'Hold empty for 4 counts',
                        'Repeat for 5 minutes'
                    ],
                    'tags': ['stress relief', 'immediate', 'anxiety']
                },
                {
                    'id': 'gentle_movement',
                    'title': '10-Minute Gentle Movement',
                    'description': 'Light stretching or walking to boost mood',
                    'duration_minutes': 10,
                    'type': 'movement',
                    'evidence_level': 'high',
                    'instructions': [
                        'Step outside or find a quiet space',
                        'Walk slowly or do gentle stretches',
                        'Focus on how your body feels',
                        'Notice any changes in your mood'
                    ],
                    'tags': ['exercise', 'mood', 'outdoor']
                }
            ],
            
            'moderate': [
                {
                    'id': 'cbt_reframing',
                    'title': 'Thought Reframing Exercise',
                    'description': 'Challenge negative thought patterns using CBT techniques',
                    'duration_minutes': 15,
                    'type': 'cognitive',
                    'evidence_level': 'high',
                    'instructions': [
                        'Identify the negative thought bothering you',
                        'Ask: "Is this thought realistic? What evidence supports it?"',
                        'Consider alternative, more balanced perspectives',
                        'Write down the reframed thought',
                        'Notice how the reframe affects your emotions'
                    ],
                    'tags': ['cbt', 'thoughts', 'reframing']
                },
                {
                    'id': 'progressive_relaxation',
                    'title': 'Progressive Muscle Relaxation',
                    'description': 'Systematic tension and release to reduce physical stress',
                    'duration_minutes': 20,
                    'type': 'relaxation',
                    'evidence_level': 'high',
                    'instructions': [
                        'Lie down or sit comfortably',
                        'Tense your toes for 5 seconds, then release',
                        'Move up through each muscle group',
                        'End with your face and scalp muscles',
                        'Rest for 5 minutes afterward'
                    ],
                    'tags': ['relaxation', 'body awareness', 'stress']
                }
            ],
            
            'high': [
                {
                    'id': 'grounding_54321',
                    'title': 'Immediate Grounding Exercise',
                    'description': '5-4-3-2-1 sensory grounding for acute distress',
                    'duration_minutes': 5,
                    'type': 'grounding',
                    'evidence_level': 'high',
                    'instructions': [
                        'Name 5 things you can see',
                        'Name 4 things you can touch',
                        'Name 3 things you can hear',
                        'Name 2 things you can smell',
                        'Name 1 thing you can taste'
                    ],
                    'tags': ['crisis', 'immediate', 'grounding'],
                    'priority': 'urgent'
                },
                {
                    'id': 'safety_planning',
                    'title': 'Create a Safety Plan',
                    'description': 'Develop a plan for managing crisis moments',
                    'duration_minutes': 30,
                    'type': 'safety',
                    'evidence_level': 'high',
                    'instructions': [
                        'List your personal warning signs',
                        'Identify helpful coping strategies',
                        'List people you can contact for support',
                        'Write down professional contacts',
                        'Make your environment safer if needed'
                    ],
                    'tags': ['safety', 'planning', 'crisis'],
                    'priority': 'urgent',
                    'requires_support': True
                }
            ]
        }
    
    def _build_cultural_library(self) -> Dict[str, Dict[str, Any]]:
        """Build culturally adapted interventions"""
        
        return {
            'indian': {
                'meditation_adaptations': {
                    'pranayama': 'Traditional breathing practices from yoga',
                    'mantra': 'Use of Om or personal mantras for focus'
                },
                'movement': {
                    'yoga_asanas': 'Gentle yoga poses for stress relief',
                    'walking_meditation': 'Mindful walking in nature'
                }
            },
            'western': {
                'cbt_focus': 'Emphasis on cognitive behavioral techniques',
                'mindfulness_secular': 'Non-religious mindfulness practices'
            }
        }
    
    def _filter_recommendations(
        self,
        recommendations: List[Dict[str, Any]],
        anxiety_level: str,
        emotion_state: str,
        user_preferences: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Filter recommendations based on user state and preferences"""
        
        filtered = []
        
        for rec in recommendations:
            # Check if recommendation fits anxiety level
            if anxiety_level == 'high' and rec['type'] not in ['breathing', 'grounding']:
                continue
            
            # Check emotion state compatibility
            if emotion_state == 'stressed' and rec['type'] == 'movement' and rec.get('intensity') == 'high':
                continue
            
            # Apply user preferences
            if user_preferences:
                preferred_types = user_preferences.get('preferred_intervention_types', [])
                if preferred_types and rec['type'] not in preferred_types:
                    continue
                
                max_duration = user_preferences.get('max_duration_minutes', 60)
                if rec['duration_minutes'] > max_duration:
                    continue
            
            filtered.append(rec)
        
        return filtered
    
    def _select_top_recommendations(
        self, 
        recommendations: List[Dict[str, Any]], 
        max_count: int = 4
    ) -> List[Dict[str, Any]]:
        """Select top recommendations with diversity"""
        
        if len(recommendations) <= max_count:
            return recommendations
        
        # Ensure type diversity
        selected = []
        types_used = set()
        
        # First pass: select different types
        for rec in recommendations:
            if rec['type'] not in types_used and len(selected) < max_count:
                selected.append(rec)
                types_used.add(rec['type'])
        
        # Fill remaining slots by evidence level
        remaining = [r for r in recommendations if r not in selected]
        remaining.sort(key=lambda x: x.get('evidence_level') == 'high', reverse=True)
        
        while len(selected) < max_count and remaining:
            selected.append(remaining.pop(0))
        
        return selected

    def get_intervention_by_id(self, intervention_id: str) -> Optional[Dict[str, Any]]:
        """Get specific intervention by ID"""
        
        for risk_level, interventions in self.intervention_library.items():
            for intervention in interventions:
                if intervention['id'] == intervention_id:
                    return intervention
        
        return None