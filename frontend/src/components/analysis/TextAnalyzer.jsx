import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FileText, Brain, AlertTriangle, CheckCircle, MessageCircle } from 'lucide-react';
import { analysisAPI } from '../../services/api';
import LoadingSpinner from '../common/LoadingSpinner';

const TextAnalyzer = () => {
  const [text, setText] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (text.trim().length < 10) {
      setError('Please provide at least 10 characters for meaningful analysis');
      return;
    }

    setAnalyzing(true);
    setError('');

    try {
      const response = await analysisAPI.analyzeText(text);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed');
    } finally {
      setAnalyzing(false);
    }
  };

  const getResultColor = (level) => {
    switch (level) {
      case 'not_depressed': return 'success';
      case 'mild': return 'warning';
      case 'moderate': return 'error';
      case 'severe': return 'error';
      default: return 'gray';
    }
  };

  const getResultIcon = (level) => {
    switch (level) {
      case 'not_depressed': return CheckCircle;
      case 'mild': return AlertTriangle;
      case 'moderate': return AlertTriangle;
      case 'severe': return AlertTriangle;
      default: return Brain;
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-xl shadow-lg p-6 border border-gray-200"
      >
        <div className="flex items-center space-x-4">
          <div className="p-3 bg-primary-100 rounded-xl">
            <FileText className="h-8 w-8 text-primary-600" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Mental Health Text Analysis</h1>
            <p className="text-gray-600">AI-powered depression screening from your text</p>
          </div>
        </div>
      </motion.div>

      {/* Text Input */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-white rounded-xl shadow-lg p-6 border border-gray-200"
      >
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            How are you feeling? Share your thoughts...
          </label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 resize-none"
            rows="6"
            placeholder="Share your thoughts, feelings, or any symptoms you've been experiencing. This helps our AI provide better mental health insights..."
            maxLength="2000"
          />
          <div className="flex justify-between mt-2 text-xs text-gray-500">
            <span>Minimum 10 characters for analysis</span>
            <span className={text.length > 1800 ? 'text-error-600' : ''}>
              {text.length}/2000
            </span>
          </div>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-error-50 border border-error-200 rounded-lg">
            <p className="text-sm text-error-700">{error}</p>
          </div>
        )}

        <button
          onClick={handleAnalyze}
          disabled={analyzing || text.trim().length < 10}
          className="w-full bg-primary-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center space-x-2"
        >
          {analyzing ? (
            <LoadingSpinner size="small" message="" />
          ) : (
            <>
              <Brain className="h-5 w-5" />
              <span>Analyze Mental Health</span>
            </>
          )}
        </button>
      </motion.div>

      {/* Results */}
      {result && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-xl shadow-lg p-6 border border-gray-200"
        >
          <div className="flex items-center space-x-3 mb-6">
            <div className="p-2 bg-success-100 rounded-lg">
              <Brain className="h-5 w-5 text-success-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Analysis Results</h3>
              <p className="text-sm text-gray-500">AI-powered mental health assessment</p>
            </div>
          </div>

          {/* Main Result */}
          <div className={`p-6 rounded-lg border-2 mb-6 bg-${getResultColor(result.depression_level)}-50 border-${getResultColor(result.depression_level)}-200`}>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                {React.createElement(getResultIcon(result.depression_level), {
                  className: `h-8 w-8 text-${getResultColor(result.depression_level)}-600`
                })}
                <div>
                  <h4 className="text-xl font-bold text-gray-900">{result.stage}</h4>
                  <p className="text-sm text-gray-600">Depression Level: {result.depression_level.replace('_', ' ')}</p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-sm text-gray-500">Confidence</p>
                <p className="text-2xl font-bold text-gray-900">{Math.round(result.confidence * 100)}%</p>
              </div>
            </div>
            
            <p className="text-gray-700">{result.explanation}</p>
          </div>

          {/* Recommendations */}
          {result.recommendations && result.recommendations.length > 0 && (
            <div className="mb-6">
              <h4 className="text-lg font-semibold text-gray-900 mb-4">Recommendations</h4>
              <div className="space-y-3">
                {result.recommendations.map((rec, index) => (
                  <div key={index} className="p-4 bg-gray-50 rounded-lg border-l-4 border-primary-500">
                    <p className="text-gray-700">{rec}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Crisis Resources for Severe Cases */}
          {result.depression_level === 'severe' && (
            <div className="bg-error-50 border-2 border-error-200 rounded-lg p-6">
              <div className="flex items-center space-x-3 mb-4">
                <AlertTriangle className="h-6 w-6 text-error-600" />
                <h4 className="text-lg font-semibold text-error-900">Immediate Support Available</h4>
              </div>
              
              <p className="text-error-800 mb-4">
                Based on your responses, we recommend reaching out for professional support immediately.
              </p>
              
              <div className="space-y-2">
                <div className="flex items-center space-x-2">
                  <span className="font-medium text-error-900">Crisis Hotline:</span>
                  <a href="tel:988" className="text-error-600 hover:text-error-800 font-medium">988</a>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="font-medium text-error-900">Crisis Text:</span>
                  <span className="text-error-600">Text HOME to 741741</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="font-medium text-error-900">Emergency:</span>
                  <a href="tel:911" className="text-error-600 hover:text-error-800 font-medium">911</a>
                </div>
              </div>
            </div>
          )}
        </motion.div>
      )}

      {/* Medical Disclaimer */}
      <div className="bg-warning-50 border border-warning-200 rounded-lg p-4">
        <div className="flex items-start space-x-2">
          <AlertTriangle className="h-4 w-4 text-warning-600 flex-shrink-0 mt-0.5" />
          <div className="text-sm text-warning-700">
            <p className="font-medium mb-1">Medical Disclaimer</p>
            <p>
              This analysis provides supportive insights based on AI and should not replace professional medical advice. 
              Always consult qualified healthcare providers for medical concerns.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TextAnalyzer;