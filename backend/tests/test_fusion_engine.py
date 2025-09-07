"""
Fusion engine tests
"""
import pytest
from app.services.ml.fusion_engine import FusionEngine

@pytest.fixture
def fusion_engine():
    """Initialize fusion engine"""
    return FusionEngine()

def test_safety_rules_override():
    """Test that safety rules override fusion logic"""
    engine = FusionEngine()
    
    # Mock text results with crisis indicators
    text_results = {
        'safety_flags': {
            'has_crisis_indicators': True,
            'risk_level': 'high'
        },
        'depression': {
            'label': 'severe',
            'confidence': 0.9
        }
    }
    
    # Mock EEG results showing stable state
    eeg_results = {
        'emotion': {'label': 'relaxed', 'confidence': 0.8},
        'anxiety': {'label': 'low', 'confidence': 0.8}
    }
    
    # Fusion should prioritize safety
    result = engine.fuse_predictions(eeg_results, text_results)
    
    assert result['risk_level'] == 'high'
    assert result.get('safety_override') is True
    assert 'Crisis indicators detected' in str(result.get('explanation', []))

def test_normal_fusion():
    """Test normal fusion without safety overrides"""
    engine = FusionEngine()
    
    # Mock agreeing results
    eeg_results = {
        'emotion': {'label': 'stressed', 'confidence': 0.7},
        'anxiety': {'label': 'moderate', 'confidence': 0.8}
    }
    
    text_results = {
        'sentiment': {'label': 'negative', 'score': 0.7},
        'depression': {'label': 'moderate', 'confidence': 0.6},
        'anxiety_keywords': {'level': 'moderate'},
        'safety_flags': {'has_crisis_indicators': False}
    }
    
    result = engine.fuse_predictions(eeg_results, text_results)
    
    assert result['risk_level'] in ['stable', 'mild', 'moderate', 'high']
    assert 'confidence' in result
    assert 'emotion_fusion' in result
    assert 'anxiety_fusion' in result
    assert isinstance(result.get('explanation'), list)

def test_eeg_only_analysis():
    """Test fusion with only EEG data"""
    engine = FusionEngine()
    
    eeg_results = {
        'emotion': {'label': 'happy', 'confidence': 0.85},
        'anxiety': {'label': 'low', 'confidence': 0.9}
    }
    
    result = engine.fuse_predictions(eeg_results=eeg_results)
    
    assert result['emotion_fusion']['label'] == 'happy'
    assert result['anxiety_fusion']['label'] == 'low'
    assert result['risk_level'] == 'stable'

def test_text_only_analysis():
    """Test fusion with only text data"""
    engine = FusionEngine()
    
    text_results = {
        'sentiment': {'label': 'positive', 'score': 0.8},
        'depression': {'label': 'not_depressed', 'confidence': 0.9},
        'anxiety_keywords': {'level': 'low'},
        'safety_flags': {'has_crisis_indicators': False}
    }
    
    result = engine.fuse_predictions(text_results=text_results)
    
    assert result['emotion_fusion']['label'] == 'happy'
    assert result['anxiety_fusion']['label'] == 'low'
    assert result['risk_level'] == 'stable'

def test_disagreement_handling():
    """Test fusion when EEG and text disagree"""
    engine = FusionEngine()
    
    # EEG shows relaxed, text shows stressed
    eeg_results = {
        'emotion': {'label': 'relaxed', 'confidence': 0.8},
        'anxiety': {'label': 'low', 'confidence': 0.8}
    }
    
    text_results = {
        'sentiment': {'label': 'negative', 'score': 0.9},
        'depression': {'label': 'moderate', 'confidence': 0.8},
        'anxiety_keywords': {'level': 'high'},
        'safety_flags': {'has_crisis_indicators': False}
    }
    
    result = engine.fuse_predictions(eeg_results, text_results)
    
    # Should detect disagreement
    emotion_fusion = result.get('emotion_fusion', {})
    anxiety_fusion = result.get('anxiety_fusion', {})
    
    assert emotion_fusion.get('agreement') is False or anxiety_fusion.get('agreement') is False
    assert result['risk_level'] != 'stable'  # Disagreement should increase caution

def test_risk_assessment_logic():
    """Test risk level determination logic"""
    engine = FusionEngine()
    
    # Test high risk scenario
    high_risk_emotion = {'label': 'sad', 'confidence': 0.8, 'agreement': True}
    high_risk_anxiety = {'label': 'high', 'confidence': 0.9, 'agreement': True}
    
    text_results = {
        'depression': {'label': 'severe', 'confidence': 0.8}
    }
    
    risk_assessment = engine._assess_risk_level(high_risk_emotion, high_risk_anxiety, text_results)
    
    assert risk_assessment['level'] in ['moderate', 'high']
    assert 0 <= risk_assessment['confidence'] <= 1

if __name__ == "__main__":
    pytest.main([__file__])