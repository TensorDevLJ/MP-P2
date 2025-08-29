import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  HelpCircle, 
  Upload, 
  Brain, 
  MessageCircle, 
  TrendingUp,
  Play,
  CheckCircle,
  ArrowRight,
  FileText,
  Zap,
  Shield,
  Clock,
  AlertTriangle
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { ROUTES } from '../utils/constants';

const HowToUsePage = () => {
  const [activeSection, setActiveSection] = useState('getting-started');
  const [expandedFaq, setExpandedFaq] = useState(null);

  const sections = [
    { id: 'getting-started', title: 'Getting Started', icon: Play },
    { id: 'eeg-analysis', title: 'EEG Analysis', icon: Brain },
    { id: 'ai-assistant', title: 'AI Assistant', icon: MessageCircle },
    { id: 'tracking', title: 'Progress Tracking', icon: TrendingUp },
    { id: 'safety', title: 'Safety & Privacy', icon: Shield },
  ];

  const steps = [
    {
      number: 1,
      title: 'Create Your Account',
      description: 'Sign up with your email and complete the consent process',
      icon: FileText,
      details: [
        'Provide a valid email address and secure password',
        'Review and accept our privacy policy and terms of service',
        'Complete the medical disclaimer acknowledgment',
        'Set your timezone for accurate scheduling',
      ],
    },
    {
      number: 2,
      title: 'Upload EEG Data',
      description: 'Upload your brainwave recordings for analysis',
      icon: Upload,
      details: [
        'Supported formats: CSV with EEG channel columns',
        'Minimum recording length: 30 seconds',
        'Maximum file size: 50MB per upload',
        'Auto-detection of sampling rate from filename or headers',
      ],
    },
    {
      number: 3,
      title: 'Get AI Insights',
      description: 'Receive comprehensive mental health analysis',
      icon: Brain,
      details: [
        'Emotion classification (happy, sad, neutral, stressed, relaxed)',
        'Anxiety level assessment (low, moderate, high)',
        'Depression indicators from text analysis (optional)',
        'Confidence scores and natural language explanations',
      ],
    },
    {
      number: 4,
      title: 'Follow Recommendations',
      description: 'Implement personalized wellness strategies',
      icon: Zap,
      details: [
        'Evidence-based breathing exercises and meditation',
        'Cognitive behavioral therapy (CBT) prompts',
        'Sleep hygiene and lifestyle recommendations',
        'Crisis resources if high-risk patterns detected',
      ],
    },
  ];

  const faqs = [
    {
      question: 'What type of EEG data can I upload?',
      answer: 'We accept CSV files containing EEG channel data. The most common formats include recordings from devices like OpenBCI, MUSE, or clinical EEG systems. Your file should have timestamps and at least one EEG channel (like AF3, AF4, etc.). We automatically detect sampling rates from 128Hz to 1000Hz.',
    },
    {
      question: 'How accurate is the AI analysis?',
      answer: 'Our AI models achieve 80-85% accuracy on standardized datasets. However, accuracy can vary based on data quality, recording conditions, and individual differences. We always provide confidence scores with results and recommend using insights as supportive information, not medical diagnosis.',
    },
    {
      question: 'Is my brain data secure and private?',
      answer: 'Yes. All data is encrypted in transit (TLS) and at rest (AES-256). Raw EEG files are deleted within 24 hours after processing. We only store extracted features and analysis results. You can export or delete your data anytime. We never share personal data with third parties.',
    },
    {
      question: 'What should I do if I get concerning results?',
      answer: 'If the system indicates high-risk patterns or you\'re experiencing mental health concerns, please reach out to a qualified mental health professional immediately. We provide crisis resources and nearby provider finder to help you get appropriate care quickly.',
    },
    {
      question: 'Can I use this instead of seeing a therapist?',
      answer: 'No. This platform provides supportive insights and wellness tools but cannot replace professional mental health care. It\'s designed to complement, not substitute, clinical treatment. Always consult licensed healthcare providers for diagnosis and treatment.',
    },
    {
      question: 'How often should I do EEG analysis?',
      answer: 'For general wellness tracking, 2-3 sessions per week can provide good insights into patterns. Daily analysis isn\'t necessary unless recommended by your healthcare provider. Focus on consistency rather than frequency for meaningful trend detection.',
    },
  ];

  const renderGettingStarted = () => (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
        <h2 className="text-xl font-bold text-gray-900 mb-6">Quick Start Guide</h2>
        
        <div className="space-y-6">
          {steps.map((step) => {
            const Icon = step.icon;
            return (
              <div key={step.number} className="flex space-x-4">
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                    <span className="text-sm font-bold text-primary-600">{step.number}</span>
                  </div>
                </div>
                
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <Icon className="h-5 w-5 text-gray-600" />
                    <h3 className="text-lg font-semibold text-gray-900">{step.title}</h3>
                  </div>
                  <p className="text-gray-600 mb-3">{step.description}</p>
                  
                  <ul className="space-y-1">
                    {step.details.map((detail, index) => (
                      <li key={index} className="flex items-start space-x-2 text-sm text-gray-700">
                        <CheckCircle className="h-4 w-4 text-success-600 flex-shrink-0 mt-0.5" />
                        <span>{detail}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            );
          })}
        </div>

        <div className="mt-8 p-4 bg-primary-50 border border-primary-200 rounded-lg">
          <div className="flex items-center space-x-3">
            <Play className="h-5 w-5 text-primary-600" />
            <div>
              <h4 className="font-semibold text-primary-900">Ready to start?</h4>
              <p className="text-sm text-primary-700">Begin your mental health journey with your first analysis</p>
            </div>
            <Link
              to={ROUTES.ANALYZE}
              className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors flex items-center space-x-2"
            >
              <span>Start Analysis</span>
              <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </div>
      </div>
    </div>
  );

  const renderEEGAnalysis = () => (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
        <h2 className="text-xl font-bold text-gray-900 mb-6">Understanding EEG Analysis</h2>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Frequency Bands</h3>
            <div className="space-y-3">
              {Object.entries({
                'Delta (0.5-4 Hz)': 'Deep sleep and unconscious processes',
                'Theta (4-8 Hz)': 'Creativity, intuition, and deep meditation',
                'Alpha (8-13 Hz)': 'Relaxed awareness and calm focus',
                'Beta (13-30 Hz)': 'Active thinking and problem solving',
                'Gamma (30-50 Hz)': 'High-level cognitive processing',
              }).map(([band, description]) => (
                <div key={band} className="p-3 bg-gray-50 rounded-lg">
                  <h4 className="font-medium text-gray-900">{band}</h4>
                  <p className="text-sm text-gray-600">{description}</p>
                </div>
              ))}
            </div>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">What We Analyze</h3>
            <div className="space-y-3">
              <div className="flex items-start space-x-3">
                <Brain className="h-5 w-5 text-primary-600 flex-shrink-0 mt-1" />
                <div>
                  <h4 className="font-medium text-gray-900">Emotional States</h4>
                  <p className="text-sm text-gray-600">Recognition of basic emotions from brainwave patterns</p>
                </div>
              </div>
              
              <div className="flex items-start space-x-3">
                <Zap className="h-5 w-5 text-warning-600 flex-shrink-0 mt-1" />
                <div>
                  <h4 className="font-medium text-gray-900">Stress Levels</h4>
                  <p className="text-sm text-gray-600">Detection of stress and anxiety indicators in neural activity</p>
                </div>
              </div>
              
              <div className="flex items-start space-x-3">
                <TrendingUp className="h-5 w-5 text-success-600 flex-shrink-0 mt-1" />
                <div>
                  <h4 className="font-medium text-gray-900">Mental Balance</h4>
                  <p className="text-sm text-gray-600">Overall cognitive and emotional equilibrium assessment</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-warning-50 border border-warning-200 rounded-lg p-6">
        <div className="flex items-start space-x-3">
          <AlertTriangle className="h-5 w-5 text-warning-600 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-semibold text-warning-900 mb-2">Important Limitations</h3>
            <ul className="space-y-1 text-sm text-warning-800">
              <li>• EEG analysis provides insights, not medical diagnosis</li>
              <li>• Results are influenced by recording quality and external factors</li>
              <li>• Individual brain patterns vary significantly between people</li>
              <li>• Always consult healthcare professionals for medical concerns</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Page Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="bg-white rounded-xl shadow-lg p-6 border border-gray-200"
      >
        <div className="flex items-center space-x-4">
          <div className="p-3 bg-primary-100 rounded-xl">
            <HelpCircle className="h-8 w-8 text-primary-600" />
          </div>
          <div>
            <h1 className="text-2xl lg:text-3xl font-bold text-gray-900">How to Use</h1>
            <p className="text-gray-600">
              Learn how to get the most from your EEG Health Assistant
            </p>
          </div>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Sidebar Navigation */}
        <div className="lg:col-span-1">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden sticky top-4"
          >
            <nav className="space-y-1 p-2">
              {sections.map((section) => {
                const Icon = section.icon;
                return (
                  <button
                    key={section.id}
                    onClick={() => setActiveSection(section.id)}
                    className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-left font-medium transition-colors ${
                      activeSection === section.id
                        ? 'bg-primary-100 text-primary-700'
                        : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                    }`}
                  >
                    <Icon className="h-5 w-5" />
                    <span>{section.title}</span>
                  </button>
                );
              })}
            </nav>
          </motion.div>
        </div>

        {/* Content Area */}
        <div className="lg:col-span-3">
          <motion.div
            key={activeSection}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
          >
            {activeSection === 'getting-started' && renderGettingStarted()}
            {activeSection === 'eeg-analysis' && renderEEGAnalysis()}
            {activeSection === 'ai-assistant' && renderAIAssistant()}
            {activeSection === 'tracking' && renderTracking()}
            {activeSection === 'safety' && renderSafety()}
          </motion.div>
        </div>
      </div>

      {/* FAQ Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.4 }}
        className="bg-white rounded-xl shadow-lg p-6 border border-gray-200"
      >
        <h2 className="text-xl font-bold text-gray-900 mb-6">Frequently Asked Questions</h2>
        
        <div className="space-y-3">
          {faqs.map((faq, index) => (
            <div key={index} className="border border-gray-200 rounded-lg">
              <button
                onClick={() => setExpandedFaq(expandedFaq === index ? null : index)}
                className="w-full px-4 py-4 text-left font-medium text-gray-900 hover:bg-gray-50 transition-colors flex items-center justify-between"
              >
                <span>{faq.question}</span>
                <ArrowRight className={`h-4 w-4 text-gray-600 transition-transform ${
                  expandedFaq === index ? 'rotate-90' : ''
                }`} />
              </button>
              
              {expandedFaq === index && (
                <motion.div
                  initial={{ height: 0 }}
                  animate={{ height: 'auto' }}
                  exit={{ height: 0 }}
                  className="overflow-hidden"
                >
                  <div className="px-4 pb-4 text-sm text-gray-700 leading-relaxed border-t border-gray-200 pt-4">
                    {faq.answer}
                  </div>
                </motion.div>
              )}
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );

  function renderAIAssistant() {
    return (
      <div className="space-y-6">
        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
          <h2 className="text-xl font-bold text-gray-900 mb-6">AI Health Assistant</h2>
          
          <div className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">What the Assistant Can Help With</h3>
                <ul className="space-y-2">
                  {[
                    'Explain your EEG analysis results',
                    'Provide evidence-based wellness strategies',
                    'Answer questions about mental health',
                    'Guide you to appropriate resources',
                    'Help interpret mood patterns',
                  ].map((item, index) => (
                    <li key={index} className="flex items-start space-x-2">
                      <CheckCircle className="h-4 w-4 text-success-600 flex-shrink-0 mt-0.5" />
                      <span className="text-gray-700 text-sm">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
              
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Safety Features</h3>
                <ul className="space-y-2">
                  {[
                    'Crisis detection and immediate resource provision',
                    'Refusal to provide medical diagnosis',
                    'Mandatory medical disclaimers',
                    'Escalation prompts for serious concerns',
                    'Evidence-based information only',
                  ].map((item, index) => (
                    <li key={index} className="flex items-start space-x-2">
                      <Shield className="h-4 w-4 text-primary-600 flex-shrink-0 mt-0.5" />
                      <span className="text-gray-700 text-sm">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="bg-warning-50 border border-warning-200 rounded-lg p-4">
              <div className="flex items-start space-x-3">
                <AlertTriangle className="h-5 w-5 text-warning-600 flex-shrink-0 mt-0.5" />
                <div className="text-sm text-warning-700">
                  <p className="font-medium mb-1">Remember</p>
                  <p>The AI assistant provides supportive information based on current research but cannot diagnose conditions or replace professional medical advice.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  function renderTracking() {
    return (
      <div className="space-y-6">
        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
          <h2 className="text-xl font-bold text-gray-900 mb-6">Progress Tracking</h2>
          
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Features Available</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 bg-primary-50 border border-primary-200 rounded-lg">
                  <TrendingUp className="h-6 w-6 text-primary-600 mb-2" />
                  <h4 className="font-semibold text-gray-900 mb-2">Trend Analysis</h4>
                  <p className="text-sm text-gray-700">
                    Visualize changes in your mental state metrics over time with interactive charts.
                  </p>
                </div>
                
                <div className="p-4 bg-success-50 border border-success-200 rounded-lg">
                  <Calendar className="h-6 w-6 text-success-600 mb-2" />
                  <h4 className="font-semibold text-gray-900 mb-2">Mood Calendar</h4>
                  <p className="text-sm text-gray-700">
                    Track daily moods and identify patterns in your mental health journey.
                  </p>
                </div>
                
                <div className="p-4 bg-warning-50 border border-warning-200 rounded-lg">
                  <CheckCircle className="h-6 w-6 text-warning-600 mb-2" />
                  <h4 className="font-semibold text-gray-900 mb-2">Goal Setting</h4>
                  <p className="text-sm text-gray-700">
                    Set and track wellness goals like meditation streaks and analysis frequency.
                  </p>
                </div>
                
                <div className="p-4 bg-error-50 border border-error-200 rounded-lg">
                  <Clock className="h-6 w-6 text-error-600 mb-2" />
                  <h4 className="font-semibold text-gray-900 mb-2">Habit Tracking</h4>
                  <p className="text-sm text-gray-700">
                    Monitor daily wellness activities and build sustainable healthy routines.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  function renderSafety() {
    return (
      <div className="space-y-6">
        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
          <h2 className="text-xl font-bold text-gray-900 mb-6">Safety & Privacy</h2>
          
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Data Security</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-medium text-gray-900 mb-3">Encryption</h4>
                  <ul className="space-y-1 text-sm text-gray-700">
                    <li>• TLS 1.3 for data in transit</li>
                    <li>• AES-256 encryption at rest</li>
                    <li>• End-to-end encrypted file uploads</li>
                    <li>• Secure token-based authentication</li>
                  </ul>
                </div>
                
                <div>
                  <h4 className="font-medium text-gray-900 mb-3">Data Handling</h4>
                  <ul className="space-y-1 text-sm text-gray-700">
                    <li>• Raw EEG files deleted within 24 hours</li>
                    <li>• Only processed features stored</li>
                    <li>• No third-party data sharing</li>
                    <li>• User-controlled data retention</li>
                  </ul>
                </div>
              </div>
            </div>

            <div className="bg-error-50 border border-error-200 rounded-lg p-4">
              <h3 className="font-semibold text-error-900 mb-3">Crisis Support</h3>
              <p className="text-sm text-error-800 mb-3">
                If you're experiencing thoughts of self-harm or suicide, please reach out immediately:
              </p>
              <ul className="space-y-2 text-sm text-error-800">
                <li>• National Suicide Prevention Lifeline: 988</li>
                <li>• Crisis Text Line: Text HOME to 741741</li>
                <li>• Emergency Services: 911</li>
                <li>• Or go to your nearest emergency room</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    );
  }
};

export default HowToUsePage;