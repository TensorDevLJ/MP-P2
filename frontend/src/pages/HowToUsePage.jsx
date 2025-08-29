// frontend/src/pages/HowToUsePage.jsx
import React from 'react';
import { 
  Brain, 
  Upload, 
  MessageSquare, 
  TrendingUp, 
  Users,
  Shield,
  BookOpen,
  CheckCircle,
  AlertTriangle,
  Heart,
  Zap,
  Target
} from 'lucide-react';

const HowToUsePage = () => {
  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl p-8">
        <div className="flex items-center space-x-4 mb-4">
          <Brain className="w-12 h-12" />
          <div>
            <h1 className="text-4xl font-bold mb-2">How to Use EEG Mental Health Assistant</h1>
            <p className="text-xl text-blue-100">
              Your comprehensive guide to AI-powered mental wellness insights
            </p>
          </div>
        </div>
      </div>

      {/* Quick Start */}
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
          <Zap className="w-6 h-6 mr-3 text-yellow-500" />
          Quick Start Guide
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[
            {
              icon: Upload,
              title: "1. Upload EEG Data",
              description: "Upload your CSV file with EEG brainwave data",
              color: "blue"
            },
            {
              icon: MessageSquare,
              title: "2. Add Context",
              description: "Optionally describe your current mood and feelings",
              color: "green"
            },
            {
              icon: Brain,
              title: "3. Get Insights",
              description: "Receive AI-powered analysis and personalized recommendations",
              color: "purple"
            }
          ].map((step, index) => (
            <div key={index} className={`bg-${step.color}-50 p-6 rounded-lg border border-${step.color}-200`}>
              <step.icon className={`w-12 h-12 text-${step.color}-500 mb-4`} />
              <h3 className={`text-lg font-semibold text-${step.color}-900 mb-2`}>{step.title}</h3>
              <p className={`text-${step.color}-700`}>{step.description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Detailed Features */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* EEG Analysis */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex items-center mb-4">
            <Brain className="w-8 h-8 text-blue-500 mr-3" />
            <h3 className="text-xl font-semibold">EEG Brainwave Analysis</h3>
          </div>
          
          <div className="space-y-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <h4 className="font-semibold text-blue-900 mb-2">What We Analyze</h4>
              <ul className="text-blue-800 text-sm space-y-1">
                <li>• <strong>Delta waves (0.5-4 Hz):</strong> Deep sleep, unconscious processes</li>
                <li>• <strong>Theta waves (4-8 Hz):</strong> Creativity, meditation, memory</li>
                <li>• <strong>Alpha waves (8-13 Hz):</strong> Relaxation, calm alertness</li>
                <li>• <strong>Beta waves (13-30 Hz):</strong> Active thinking, concentration</li>
                <li>• <strong>Gamma waves (30-45 Hz):</strong> Higher cognitive functions</li>
              </ul>
            </div>

            <div className="bg-green-50 p-4 rounded-lg">
              <h4 className="font-semibold text-green-900 mb-2">CSV Format Requirements</h4>
              <ul className="text-green-800 text-sm space-y-1">
                <li>• Include sampling rate in header (e.g., "EEG_128Hz")</li>
                <li>• Minimum recording duration: 2 seconds</li>
                <li>• Common channel names: EEG, AF3, AF4, F3, F4</li>
                <li>• Data values in microvolts (µV)</li>
                <li>• Maximum file size: 50MB</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Text Analysis */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex items-center mb-4">
            <MessageSquare className="w-8 h-8 text-green-500 mr-3" />
            <h3 className="text-xl font-semibold">Text & Mood Analysis</h3>
          </div>
          
          <div className="space-y-4">
            <div className="bg-green-50 p-4 rounded-lg">
              <h4 className="font-semibold text-green-900 mb-2">What to Include</h4>
              <ul className="text-green-800 text-sm space-y-1">
                <li>• Current emotional state</li>
                <li>• Sleep quality and patterns</li>
                <li>• Stress levels and sources</li>
                <li>• Energy and motivation levels</li>
                <li>• Any concerns or worries</li>
              </ul>
            </div>

            <div className="bg-yellow-50 p-4 rounded-lg">
              <h4 className="font-semibold text-yellow-900 mb-2">AI Detection Capabilities</h4>
              <ul className="text-yellow-800 text-sm space-y-1">
                <li>• Depression severity assessment</li>
                <li>• Anxiety level indicators</li>
                <li>• Crisis situation detection</li>
                <li>• Mood pattern analysis</li>
                <li>• Sentiment and emotional tone</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Understanding Results */}
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
          <TrendingUp className="w-6 h-6 mr-3 text-indigo-500" />
          Understanding Your Results
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[
            {
              title: "Stable",
              color: "green",
              description: "Low risk indicators, generally positive mental state",
              recommendations: "Continue wellness practices, maintain routine"
            },
            {
              title: "Mild Concern",
              color: "yellow", 
              description: "Some stress or mood indicators present",
              recommendations: "Practice self-care, consider relaxation techniques"
            },
            {
              title: "Moderate Risk",
              color: "orange",
              description: "Multiple risk factors detected",
              recommendations: "Consider professional consultation, increased monitoring"
            },
            {
              title: "High Risk",
              color: "red",
              description: "Significant mental health concerns identified",
              recommendations: "Seek professional help immediately, safety planning"
            }
          ].map((level, index) => (
            <div key={index} className={`bg-${level.color}-50 p-4 rounded-lg border border-${level.color}-200`}>
              <div className={`w-4 h-4 bg-${level.color}-500 rounded-full mb-3`}></div>
              <h3 className={`font-semibold text-${level.color}-900 mb-2`}>{level.title}</h3>
              <p className={`text-${level.color}-800 text-sm mb-3`}>{level.description}</p>
              <div className={`text-xs text-${level.color}-700 bg-${level.color}-100 p-2 rounded`}>
                <strong>Action:</strong> {level.recommendations}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* AI Assistant */}
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
          <Heart className="w-6 h-6 mr-3 text-pink-500" />
          AI Mental Health Assistant
        </h2>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-4">What Your Assistant Can Help With</h3>
            <div className="space-y-3">
              {[
                "Explain your EEG analysis results in simple terms",
                "Provide evidence-based coping strategies",
                "Answer questions about mental health",
                "Offer personalized wellness recommendations",
                "Help you track mood patterns over time",
                "Guide you to appropriate professional resources"
              ].map((item, index) => (
                <div key={index} className="flex items-center space-x-3">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  <span className="text-gray-700">{item}</span>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">Example Questions to Ask</h3>
            <div className="space-y-2">
              {[
                ""What do my alpha waves indicate?"",
                ""How can I reduce my anxiety levels?"",
                ""What does a high beta power mean?"",
                ""Can you suggest some relaxation techniques?"",
                ""How should I interpret my risk level?"",
                ""What are signs I should see a therapist?""
              ].map((question, index) => (
                <div key={index} className="bg-blue-50 p-3 rounded-lg text-blue-800 text-sm">
                  {question}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Safety & Privacy */}
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
          <Shield className="w-6 h-6 mr-3 text-green-500" />
          Safety & Privacy
        </h2>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-4 flex items-center">
              <AlertTriangle className="w-5 h-5 mr-2 text-red-500" />
              Important Safety Information
            </h3>
            <div className="bg-red-50 p-4 rounded-lg border border-red-200">
              <ul className="text-red-800 text-sm space-y-2">
                <li>• This tool provides <strong>supportive insights only</strong></li>
                <li>• <strong>Not a substitute</strong> for professional medical diagnosis</li>
                <li>• <strong>Crisis detection</strong> automatically provides emergency resources</li>
                <li>• Always consult healthcare providers for serious concerns</li>
                <li>• If you're in crisis, contact emergency services immediately</li>
              </ul>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4 flex items-center">
              <Shield className="w-5 h-5 mr-2 text-green-500" />
              Data Privacy & Security
            </h3>
            <div className="bg-green-50 p-4 rounded-lg border border-green-200">
              <ul className="text-green-800 text-sm space-y-2">
                <li>• <strong>Encrypted storage</strong> for all EEG and text data</li>
                <li>• <strong>No data sharing</strong> without explicit consent</li>
                <li>• <strong>Right to deletion</strong> - remove your data anytime</li>
                <li>• <strong>Anonymized analytics</strong> for research only</li>
                <li>• <strong>GDPR compliant</strong> data handling practices</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Tips for Best Results */}
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
          <Target className="w-6 h-6 mr-3 text-purple-500" />
          Tips for Best Results
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[
            {
              title: "Quality EEG Data",
              tips: [
                "Use clean, artifact-free recordings",
                "Ensure good electrode contact",
                "Record in quiet environment",
                "Include at least 2 minutes of data"
              ]
            },
            {
              title: "Detailed Text Input",
              tips: [
                "Be honest about your feelings",
                "Include specific examples",
                "Mention sleep and energy levels",
                "Note any recent stressors"
              ]
            },
            {
              title: "Regular Monitoring",
              tips: [
                "Track changes over time",
                "Use consistently for trends",
                "Note external factors",
                "Follow up on recommendations"
              ]
            }
          ].map((section, index) => (
            <div key={index} className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="font-semibold text-purple-900 mb-4">{section.title}</h3>
              <ul className="text-purple-800 text-sm space-y-2">
                {section.tips.map((tip, tipIndex) => (
                  <li key={tipIndex} className="flex items-start space-x-2">
                    <CheckCircle className="w-4 h-4 text-purple-500 mt-0.5" />
                    <span>{tip}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>

      {/* Contact & Support */}
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
          <Users className="w-6 h-6 mr-3 text-indigo-500" />
          Support & Feedback
        </h2>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-4">Need Help?</h3>
            <p className="text-gray-600 mb-4">
              Our support team is here to help you make the most of your mental health journey.
            </p>
            <div className="space-y-3">
              <div className="flex items-center space-x-3">
                <MessageSquare className="w-5 h-5 text-blue-500" />
                <span>Use the in-app chat assistant for immediate help</span>
              </div>
              <div className="flex items-center space-x-3">
                <BookOpen className="w-5 h-5 text-green-500" />
                <span>Check our knowledge base and FAQ</span>
              </div>
              <div className="flex items-center space-x-3">
                <Users className="w-5 h-5 text-purple-500" />
                <span>Contact support: support@eeghealth.ai</span>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">Share Your Experience</h3>
            <p className="text-gray-600 mb-4">
              Your feedback helps us improve our AI models and user experience.
            </p>
            <div className="bg-indigo-50 p-4 rounded-lg border border-indigo-200">
              <h4 className="font-semibold text-indigo-900 mb-2">Rate Your Experience</h4>
              <p className="text-indigo-800 text-sm mb-3">
                How helpful was your analysis? Your rating helps improve our AI accuracy.
              </p>
              <button className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors">
                Provide Feedback
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Emergency Resources */}
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <div className="flex items-center mb-4">
          <AlertTriangle className="w-8 h-8 text-red-500 mr-3" />
          <h2 className="text-xl font-bold text-red-900">Crisis Resources</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div className="bg-white p-4 rounded-lg">
            <h3 className="font-semibold text-red-900 mb-2">United States</h3>
            <p className="text-red-800">National Suicide Prevention Lifeline: 988</p>
            <p className="text-red-800">Crisis Text Line: Text HOME to 741741</p>
          </div>
          <div className="bg-white p-4 rounded-lg">
            <h3 className="font-semibold text-red-900 mb-2">International</h3>
            <p className="text-red-800">International Association for Suicide Prevention</p>
            <p className="text-red-800">befrienders.org</p>
          </div>
          <div className="bg-white p-4 rounded-lg">
            <h3 className="font-semibold text-red-900 mb-2">Emergency</h3>
            <p className="text-red-800">If in immediate danger: 911 (US)</p>
            <p className="text-red-800">Go to nearest emergency room</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HowToUsePage;