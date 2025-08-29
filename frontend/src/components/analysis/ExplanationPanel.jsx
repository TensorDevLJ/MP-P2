import React from 'react';
import { 
  Brain, 
  AlertTriangle, 
  CheckCircle, 
  Info, 
  Phone,
  ExternalLink,
  Lightbulb
} from 'lucide-react';
import { CRISIS_RESOURCES } from '../../utils/constants';

const ExplanationPanel = ({ 
  explanations = [],
  sessionState,
  naturalLanguageExplanation = '',
  safetyAlerts = [],
  recommendations = []
}) => {
  const getAlertIcon = (type) => {
    switch (type) {
      case 'crisis': return AlertTriangle;
      case 'info': return Info;
      case 'success': return CheckCircle;
      default: return Brain;
    }
  };

  const getAlertColor = (type) => {
    switch (type) {
      case 'crisis': return 'error';
      case 'info': return 'primary';
      case 'success': return 'success';
      default: return 'gray';
    }
  };

  return (
    <div className="space-y-6">
      {/* Natural Language Summary */}
      {naturalLanguageExplanation && (
        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-primary-100 rounded-lg">
              <Brain className="h-5 w-5 text-primary-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">AI Analysis Summary</h3>
              <p className="text-sm text-gray-500">Combined EEG and text insights</p>
            </div>
          </div>
          
          <div className="prose prose-sm max-w-none text-gray-700">
            <p>{naturalLanguageExplanation}</p>
          </div>
        </div>
      )}

      {/* Technical Explanations */}
      {explanations.length > 0 && (
        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-gray-100 rounded-lg">
              <Lightbulb className="h-5 w-5 text-gray-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Technical Insights</h3>
              <p className="text-sm text-gray-500">Detailed analysis breakdown</p>
            </div>
          </div>
          
          <div className="space-y-3">
            {explanations.map((explanation, index) => (
              <div key={index} className="p-4 bg-gray-50 rounded-lg border-l-4 border-primary-500">
                <p className="text-sm text-gray-700">{explanation}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Personalized Recommendations */}
      {recommendations.length > 0 && (
        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-success-100 rounded-lg">
              <CheckCircle className="h-5 w-5 text-success-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Personalized Recommendations</h3>
              <p className="text-sm text-gray-500">Evidence-based suggestions for you</p>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {recommendations.map((rec, index) => (
              <div key={index} className="p-4 border border-gray-200 rounded-lg hover:shadow-sm transition-shadow">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="text-sm font-semibold text-gray-900">{rec.title}</h4>
                  <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                    {rec.duration}min
                  </span>
                </div>
                <p className="text-sm text-gray-600 mb-3">{rec.description}</p>
                <button className="text-xs text-primary-600 hover:text-primary-700 font-medium">
                  Start Activity →
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Safety Alerts */}
      {safetyAlerts.length > 0 && (
        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
          {safetyAlerts.map((alert, index) => {
            const Icon = getAlertIcon(alert.type);
            const colorClass = getAlertColor(alert.type);
            
            return (
              <div key={index} className={`p-4 bg-${colorClass}-50 border border-${colorClass}-200 rounded-lg mb-4 last:mb-0`}>
                <div className="flex items-start space-x-3">
                  <Icon className={`h-5 w-5 text-${colorClass}-600 flex-shrink-0 mt-0.5`} />
                  <div className="flex-1">
                    <h4 className={`text-sm font-semibold text-${colorClass}-800 mb-1`}>
                      {alert.title}
                    </h4>
                    <p className={`text-sm text-${colorClass}-700`}>{alert.message}</p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Crisis Resources (shown for high-risk states) */}
      {(sessionState?.risk === 'high' || safetyAlerts.some(a => a.type === 'crisis')) && (
        <div className="bg-white rounded-xl shadow-lg p-6 border border-error-200 border-2">
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-error-100 rounded-lg">
              <Phone className="h-5 w-5 text-error-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-error-900">Crisis Support Resources</h3>
              <p className="text-sm text-error-700">Immediate help is available 24/7</p>
            </div>
          </div>
          
          <div className="space-y-3">
            {CRISIS_RESOURCES.map((resource, index) => (
              <div key={index} className="p-4 bg-error-50 rounded-lg border border-error-200">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="text-sm font-semibold text-error-900">{resource.name}</h4>
                    <p className="text-sm text-error-700">{resource.description}</p>
                  </div>
                  <a
                    href={`tel:${resource.phone.replace(/[^0-9]/g, '')}`}
                    className="bg-error-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-error-700 transition-colors flex items-center space-x-2"
                  >
                    <Phone className="h-4 w-4" />
                    <span>{resource.phone}</span>
                  </a>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-4 p-3 bg-error-100 rounded-lg">
            <p className="text-sm text-error-800 font-medium">
              If you're experiencing thoughts of self-harm or suicide, please call emergency services (911) or go to your nearest emergency room immediately.
            </p>
          </div>
        </div>
      )}

      {/* Medical Disclaimer */}
      <div className="bg-warning-50 border border-warning-200 rounded-lg p-4">
        <div className="flex items-start space-x-2">
          <AlertTriangle className="h-4 w-4 text-warning-600 flex-shrink-0 mt-0.5" />
          <div className="text-sm text-warning-700">
            <p className="font-medium mb-1">Important Medical Disclaimer</p>
            <p>
              This analysis provides supportive insights based on EEG patterns and should not be used as a substitute for professional medical diagnosis or treatment. 
              Always consult with qualified healthcare providers for medical advice.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExplanationPanel;