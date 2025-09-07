"""
Text analysis tests
"""
import pytest
from app.services.ml.text_classifier import TextClassifier

@pytest.fixture
def text_classifier():
    """Initialize text classifier for testing"""
    return TextClassifier()

def test_text_preprocessing():
    """Test text preprocessing"""
    classifier = TextClassifier()
    
    # Test basic cleaning
    dirty_text = "Check out this link: http://example.com @user   Extra   spaces!!!"
    clean_text = classifier._preprocess_text(dirty_text)
    
    assert "http://" not in clean_text
    assert "@user" not in clean_text
    assert "extra spaces" in clean_text  # Normalized whitespace

def test_safety_check():
    """Test crisis keyword detection"""
    classifier = TextClassifier()
    
    # Safe text
    safe_text = "feeling a bit down today but managing okay"
    safety_result = classifier._check_safety(safe_text)
    assert not safety_result['has_crisis_indicators']
    assert safety_result['risk_level'] == 'low'
    
    # Crisis text
    crisis_text = "i want to hurt myself and end it all"
    crisis_result = classifier._check_safety(crisis_text)
    assert crisis_result['has_crisis_indicators']
    assert crisis_result['risk_level'] == 'high'
    assert len(crisis_result['crisis_keywords_found']) > 0

def test_depression_analysis():
    """Test depression severity analysis"""
    classifier = TextClassifier()
    
    test_cases = [
        {
            "text": "feeling happy and excited about life, everything is going great",
            "expected": "not_depressed"
        },
        {
            "text": "been feeling sad and low lately, not much motivation for anything",
            "expected": "moderate"  
        },
        {
            "text": "life feels completely hopeless and pointless, nothing matters anymore",
            "expected": "severe"
        }
    ]
    
    for case in test_cases:
        result = classifier._analyze_depression(case["text"])
        
        assert result['label'] == case['expected']
        assert 'probabilities' in result
        assert 'confidence' in result
        assert 0 <= result['confidence'] <= 1

def test_anxiety_keyword_analysis():
    """Test anxiety level detection from keywords"""
    classifier = TextClassifier()
    
    # High anxiety text
    high_anxiety_text = "feeling panic and terror, everything is overwhelming and catastrophic"
    result = classifier._analyze_anxiety_keywords(high_anxiety_text)
    assert result['level'] == 'high'
    assert result['scores']['high'] > 0
    
    # Low anxiety text  
    low_anxiety_text = "feeling calm and peaceful today, very relaxed and stable"
    result = classifier._analyze_anxiety_keywords(low_anxiety_text)
    assert result['level'] == 'low'
    assert result['scores']['low'] > 0

def test_complete_text_analysis():
    """Test complete text analysis pipeline"""
    classifier = TextClassifier()
    
    sample_text = """
    I've been struggling lately with sleep issues and feeling quite overwhelmed 
    with work stress. Not enjoying things I used to love and feeling tired all the time.
    Sometimes I worry that things won't get better.
    """
    
    result = classifier.analyze_text(sample_text)
    
    # Verify response structure
    assert 'depression' in result
    assert 'anxiety_keywords' in result  
    assert 'sentiment' in result
    assert 'safety_flags' in result
    assert 'text_stats' in result
    
    # Verify data types
    assert isinstance(result['depression']['probabilities'], dict)
    assert isinstance(result['safety_flags']['has_crisis_indicators'], bool)
    assert isinstance(result['text_stats']['word_count'], int)
    
    # Should detect some depression/anxiety indicators
    assert result['depression']['label'] != 'not_depressed'
    assert result['anxiety_keywords']['level'] != 'low'

if __name__ == "__main__":
    pytest.main([__file__])