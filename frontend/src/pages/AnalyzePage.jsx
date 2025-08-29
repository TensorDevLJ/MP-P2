import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Brain, FileText, Zap, AlertTriangle } from 'lucide-react';
import EEGUploader from '../components/analysis/EEGUploader';
import EEGResultGrid from '../components/analysis/EEGResultGrid';
import LoadingSpinner from '../components/common/LoadingSpinner';
import { useAPIMutation } from '../hooks/useAPI';
import { eegAPI, analysisAPI } from '../services/api';

const AnalyzePage = () => {
  const [analysisState, setAnalysisState] = useState('idle'); // idle, analyzing, complete, error
  const [sessionData, setSessionData] = useState(null);
  const [includeTextAnalysis, setIncludeTextAnalysis] = useState(false);
  const [error, setError] = useState(null);

  // Mock analysis mutation - in real app would call actual API
  const analysisMutation = useAPIMutation(
    async (analysisData) => {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      // Mock successful response
      return {
        session_id: 'mock-session-' + Date.now(),
        fusion: { risk: 'stable', confidence: 0.87 },
        emotion: { label: 'calm', probs: { calm: 0.8, neutral: 0.15, stressed: 0.05 } },
        anxiety: { label: 'low', score: 0.23 },
        depression_text: includeTextAnalysis ? { label: 'not', probs: { not: 0.82, moderate: 0.15, severe: 0.03 } } : null,
        explain: [
          'Alpha waves show strong presence, indicating relaxed awareness',
          'Beta activity is within normal range, suggesting good cognitive function',
          'No significant asymmetry detected in frontal regions'
        ],
        recommendations: [
          { title: 'Continue meditation practice', duration: 10, description: 'Your alpha patterns suggest meditation is working well' },
          { title: 'Morning sunlight exposure', duration: 15, description: 'Help maintain healthy circadian rhythms' },
        ],
        bands_timeseries: {
          delta: Array.from({ length: 60 }, (_, i) => 0.3 + Math.sin(i * 0.1) * 0.1),
          theta: Array.from({ length: 60 }, (_, i) => 0.4 + Math.sin(i * 0.15) * 0.15),
          alpha: Array.from({ length: 60 }, (_, i) => 0.8 + Math.sin(i * 0.2) * 0.2),
          beta: Array.from({ length: 60 }, (_, i) => 0.5 + Math.sin(i * 0.25) * 0.1),
          gamma: Array.from({ length: 60 }, (_, i) => 0.2 + Math.sin(i * 0.3) * 0.05),
        },
        times: Array.from({ length: 60 }, (_, i) => new Date(Date.now() + i * 1000).toISOString()),
        psd: {
          freqs: Array.from({ length: 50 }, (_, i) => i + 0.5),
          power: Array.from({ length: 50 }, (_, i) => Math.exp(-i * 0.1) + Math.random() * 0.1),
        },
        spectrogram_image_base64: null, // Would contain actual base64 image
        natural_explanation: 'Your brain activity shows healthy patterns typical of a relaxed, focused state. Alpha waves are prominent, indicating good mental balance, while beta activity suggests appropriate cognitive engagement without excessive stress.',
        completed_at: new Date().toISOString(),
      };
    },
    {
      onSuccess: (data) => {
        setSessionData(data);
        setAnalysisState('complete');
      },
      onError: (error) => {
        setError(error.message || 'Analysis failed');
        setAnalysisState('error');
      },
    }
  );

  const handleFileUpload = (file) => {
    console.log('File uploaded:', file.name);
    setError(null);
  };

  const handleAnalysisStart = async (analysisData) => {
    setAnalysisState('analyzing');
    setError(null);
    
    try {
      await analysisMutation.mutateAsync(analysisData);
    } catch (err) {
      console.error('Analysis failed:', err);
    }
  };

  const handleSaveSession = () => {
    console.log('Saving session...');
  };

  const handleScheduleFollowup = () => {
    console.log('Scheduling follow-up...');
  };

  const handleShare = () => {
    console.log('Sharing results...');
  };

  const handleNewAnalysis = () => {
    setAnalysisState('idle');
    setSessionData(null);
    setError(null);
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Page Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="bg-white rounded-xl shadow-lg p-6 border border-gray-200"
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-primary-100 rounded-xl">
              <Brain className="h-8 w-8 text-primary-600" />
            </div>
            <div>
              <h1 className="text-2xl lg:text-3xl font-bold text-gray-900">EEG Analysis</h1>
              <p className="text-gray-600">
                Upload your brainwave data for AI-powered mental health insights
              </p>
            </div>
          </div>
          
          {analysisState === 'complete' && (
            <button
              onClick={handleNewAnalysis}
              className="bg-primary-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-primary-700 transition-colors flex items-center space-x-2"
            >
              <Zap className="h-4 w-4" />
              <span>New Analysis</span>
            </button>
          )}
        </div>
      </motion.div>

      {/* Analysis Flow */}
      {analysisState === 'idle' && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
        >
          <EEGUploader
            onFileUpload={handleFileUpload}
            onAnalysisStart={handleAnalysisStart}
            includeTextAnalysis={includeTextAnalysis}
            setIncludeTextAnalysis={setIncludeTextAnalysis}
          />
        </motion.div>
      )}

      {analysisState === 'analyzing' && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6 }}
          className="bg-white rounded-xl shadow-lg p-12 border border-gray-200 text-center"
        >
          <LoadingSpinner size="large" message="Analyzing your EEG data..." />
          
          <div className="mt-8 space-y-4">
            <div className="flex items-center justify-center space-x-2 text-sm text-gray-600">
              <FileText className="h-4 w-4" />
              <span>Processing signal data...</span>
            </div>
            
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-primary-600 h-2 rounded-full animate-pulse w-2/3"></div>
            </div>
            
            <p className="text-sm text-gray-500 max-w-md mx-auto">
              Our AI is analyzing your brainwave patterns across multiple frequency bands 
              to provide comprehensive mental health insights.
            </p>
          </div>
        </motion.div>
      )}

      {analysisState === 'error' && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="bg-white rounded-xl shadow-lg p-8 border border-error-200 text-center"
        >
          <div className="w-16 h-16 bg-error-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <AlertTriangle className="h-8 w-8 text-error-600" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Analysis Failed</h3>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={handleNewAnalysis}
            className="bg-primary-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-primary-700 transition-colors"
          >
            Try Again
          </button>
        </motion.div>
      )}

      {analysisState === 'complete' && sessionData && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <EEGResultGrid
            sessionData={sessionData}
            onSaveSession={handleSaveSession}
            onScheduleFollowup={handleScheduleFollowup}
            onShare={handleShare}
          />
        </motion.div>
      )}
    </div>
  );
};

export default AnalyzePage;