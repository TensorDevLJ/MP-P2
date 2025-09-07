# EEG Mental Health Assistant - User Guide

## What is the EEG Mental Health Assistant?

The EEG Mental Health Assistant is an AI-powered tool that analyzes brain wave patterns (EEG) and text inputs to provide insights about your mental state. It combines objective neurophysiological data with your personal thoughts and feelings to offer personalized wellness recommendations.

**Important:** This tool provides supportive insights and is NOT a medical device or diagnostic tool. It should complement, not replace, professional mental health care.

## Getting Started

### 1. Account Setup

**Registration:**
- Visit the application and click "Sign Up"
- Provide email, secure password, and display name
- Review and accept privacy policy and terms
- Choose your data sharing preferences

**Privacy Controls:**
- **Research Consent:** Allow anonymized data for research (optional)
- **Data Sharing:** Share aggregated insights with healthcare providers (optional)
- **Retention Period:** Choose how long to keep your data (1-5 years)

### 2. Understanding the Analysis

The system analyzes two types of input:

**EEG Analysis (Objective):**
- Brain wave patterns from EEG recordings
- Identifies emotional states and anxiety levels
- Requires CSV files from compatible EEG devices

**Text Analysis (Subjective):**
- Your written thoughts, feelings, or journal entries
- Assesses language patterns for depression indicators
- Provides sentiment and emotional tone analysis

**Combined Analysis:**
- Fuses both EEG and text insights
- Provides overall mental health risk assessment
- Offers personalized recommendations

## Using EEG Analysis

### Supported Devices

The system works with EEG recordings from:
- Emotiv EPOC/Insight headsets
- OpenBCI boards
- NeuroSky devices
- Research-grade EEG systems
- Any device that exports CSV format with time-series data

### File Requirements

**Format:** CSV files with columns for time and EEG channels
**Example format:**
```
Time, EEG.AF3, EEG.F7, EEG.F3, EEG.FC5
0.0, 4235.23, 4182.56, 4198.77, 4221.33
0.008, 4238.91, 4185.12, 4201.45, 4224.88
```

**Technical Specifications:**
- Sampling rate: 64-1024 Hz (128 Hz recommended)
- Duration: Minimum 30 seconds, optimal 2-5 minutes
- Channels: Single channel sufficient, multi-channel preferred
- File size: Maximum 50MB

### Recording Guidelines

**For Best Results:**
1. **Environment:** Quiet, comfortable space
2. **Position:** Seated comfortably, eyes closed or relaxed
3. **Duration:** 2-3 minutes minimum
4. **State:** Try to be natural - don't force any particular mood
5. **Electrode Quality:** Ensure good skin contact, minimal artifacts

**Recording States:**
- **Baseline:** 2 minutes relaxed with eyes closed
- **Task State:** During specific activities if analyzing task-related stress
- **Post-Activity:** After meditation, exercise, or stressful events

### Uploading and Processing

1. **Upload File:**
   - Drag and drop CSV file or click to browse
   - System automatically detects sampling rate and channels
   - Preview shows first few rows for verification

2. **Configuration:**
   - **Channel Selection:** Choose primary analysis channel (usually frontal)
   - **Epoch Length:** 2-4 seconds (default: 2 seconds)
   - **Overlap:** 50% (provides smoother analysis)

3. **Processing:**
   - Takes 30-60 seconds for typical recordings
   - Real-time progress updates
   - Background processing allows you to continue using the app

## Understanding Your Results

### Brain Wave Patterns

**Delta Waves (0.5-4 Hz):**
- High: Deep relaxation, meditation, fatigue
- Low: Alert, wakeful state
- Associated with: Deep sleep, healing, regeneration

**Theta Waves (4-8 Hz):**
- High: Creativity, deep meditation, REM sleep
- Low: Alert focus, active thinking
- Associated with: Memory formation, intuition, emotional processing

**Alpha Waves (8-12 Hz):**
- High: Relaxed awareness, calm alertness
- Low: Stress, anxiety, active concentration
- Associated with: Meditation, flow states, peaceful awareness

**Beta Waves (12-30 Hz):**
- High: Active thinking, problem-solving, anxiety
- Low: Relaxed state, less mental activity
- Associated with: Focus, analytical thinking, alertness

**Gamma Waves (30-45 Hz):**
- High: High-level cognitive processing, insight moments
- Low: Normal for most relaxed states
- Associated with: Learning, memory binding, consciousness

### Risk Level Interpretation

**Stable (Green):**
- Balanced brain patterns
- No significant concerns detected
- Continue current wellness practices

**Mild (Yellow):**
- Minor imbalances detected
- Good time for preventive self-care
- Monitor patterns over time

**Moderate (Orange):**
- Notable patterns requiring attention
- Implement active coping strategies
- Consider professional consultation if persistent

**High (Red):**
- Concerning patterns detected
- Immediate self-care and professional support recommended
- Emergency resources provided if crisis language detected

### Text Analysis Results

**Depression Assessment:**
- **Not Depressed:** Language patterns suggest stable mood
- **Moderate:** Some concerning language patterns detected
- **Severe:** Significant depression indicators present

**Sentiment Analysis:**
- Overall emotional tone of your writing
- Positive/negative/neutral classification
- Confidence score for assessment accuracy

**Safety Features:**
- Automatic detection of crisis language
- Immediate emergency resource provision
- Professional help recommendations

## Using the Chat Assistant

### What the Chatbot Can Help With:

✅ **Supported Topics:**
- Explaining your EEG analysis results
- Discussing coping strategies and self-care
- Understanding brain wave patterns
- Guidance on when to seek professional help
- General mental wellness education
- Interpreting trends in your data

❌ **What It Cannot Do:**
- Provide medical diagnosis
- Prescribe medications
- Replace professional therapy
- Handle medical emergencies (will redirect to emergency services)

### Sample Conversations:

**Understanding Results:**
> "What do my alpha waves mean?"
> "Can you explain why my anxiety level was marked as moderate?"

**Wellness Guidance:**
> "I'm feeling stressed, what breathing exercises can help?"
> "How can I improve my sleep for better mental health?"

**Crisis Support:**
> If crisis language is detected, immediate resources are provided
> Emergency hotlines and professional support options

## Tracking Your Progress

### Trends Dashboard

**Weekly View:**
- Risk level changes over time
- Brain wave pattern trends
- Mood consistency tracking

**Monthly Analysis:**
- Long-term pattern identification
- Intervention effectiveness
- Wellness goal progress

### Data Export

You can export your data for:
- Sharing with healthcare providers
- Personal record keeping
- Research participation (if consented)

**Export Options:**
- JSON format (complete data)
- CSV format (for analysis)
- PDF reports (for sharing)

## Finding Professional Help

### Nearby Providers Feature

**How It Works:**
1. Enable location services (optional)
2. System finds mental health professionals within 10km
3. Filter by specialty: psychiatrist, psychologist, therapist
4. View ratings, contact info, and hours

**Provider Information:**
- Specialty and credentials
- Patient ratings and reviews
- Contact information and website
- Distance and travel time
- Current hours and availability

**Privacy Note:**
Your location is only used for provider search and is not stored permanently.

## Privacy and Data Control

### Your Data Rights

**Access:** View all your data at any time
**Export:** Download complete data archive
**Delete:** Remove all data permanently
**Control:** Granular sharing preferences

### Data Security

**Encryption:**
- All data encrypted with military-grade AES-256
- Secure transmission using TLS 1.3
- No data stored on local devices

**Access Control:**
- Only you can access your personal data
- Healthcare providers only see what you explicitly share
- Researchers only see anonymized aggregates (if consented)

### Data Retention

**Default Policy:** 2 years
**Options:** 1 year to 5 years
**Deletion:** Automatic after retention period
**Override:** Manual deletion available anytime

## Safety and Crisis Support

### Crisis Detection

The system automatically detects concerning language patterns and immediately provides:
- Emergency hotline numbers
- Local crisis resources
- Professional support guidance
- Safety planning resources

### Emergency Resources

**United States:**
- National Suicide Prevention Lifeline: 988
- Crisis Text Line: Text HOME to 741741
- Emergency Services: 911

**International:**
- Befrienders Worldwide: befrienders.org
- International Association for Suicide Prevention: iasp.info

### When to Seek Professional Help

**Immediate Support Needed:**
- Thoughts of self-harm or suicide
- Substance abuse concerns
- Inability to function in daily life
- Persistent high-risk assessments

**Consider Professional Support:**
- Consistent moderate risk levels
- Persistent sleep or appetite changes
- Relationship or work difficulties
- Desire for additional coping strategies

## Technical Support

### Common Issues

**Upload Problems:**
- Ensure CSV format with time and EEG columns
- Check file size (must be under 50MB)
- Verify sampling rate is detected correctly

**Analysis Errors:**
- Try different channel selection
- Ensure minimum 30 seconds of data
- Check for excessive artifacts in recording

**Account Issues:**
- Password reset available on login page
- Contact support for account recovery
- Check email (including spam folder) for verification

### Getting Help

**In-App Support:**
- Chat with the AI assistant for technical questions
- Help section with common solutions
- Feedback form for reporting issues

**Contact Information:**
- Email: support@eeghealth.app
- Response time: 24-48 hours
- Emergency: Use crisis resources above

## Best Practices

### For Accurate Analysis

1. **Consistent Recording Environment**
2. **Regular Recording Schedule** 
3. **Honest Text Inputs**
4. **Follow Recommended Guidelines**
5. **Review Trends Over Time**

### For Maximum Benefit

1. **Use Consistently:** Regular analysis provides better insights
2. **Combine Methods:** Both EEG and text provide fuller picture
3. **Follow Recommendations:** Try suggested wellness activities
4. **Track Progress:** Monitor your trends over time
5. **Stay Connected:** Use nearby providers when needed

### Privacy Best Practices

1. **Review Settings:** Regularly check privacy preferences
2. **Secure Account:** Use strong password and enable 2FA
3. **Monitor Access:** Review account activity logs
4. **Control Sharing:** Only share what you're comfortable with
5. **Understand Usage:** Read privacy policy updates

## Disclaimer

This system is designed to support your mental wellness journey and provide educational information. It is not intended to diagnose, treat, cure, or prevent any medical condition. Always consult with qualified healthcare professionals for medical advice, diagnosis, or treatment.

The AI analysis provides insights based on patterns in your data but cannot account for all factors affecting mental health. Use this tool as one part of a comprehensive approach to mental wellness that includes professional care, social support, and healthy lifestyle practices.

If you are experiencing a mental health crisis, please contact emergency services or a crisis hotline immediately rather than relying solely on this application.