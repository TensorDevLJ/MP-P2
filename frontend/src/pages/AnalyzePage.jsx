// frontend/src/pages/AnalyzePage.jsx
import React, { useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { toast } from 'react-hot-toast';

import EEGUploader from '../components/analysis/EEGUploader';
import EEGResultGrid from '../components/analysis/EEGResultGrid';
import TextAnalysisPanel from '../components/analysis/TextAnalysisPanel';
import { api } from '../services/api';

const AnalyzePage = () => {
  const [activeTab, setActiveTab] = useState('eeg');
  const [currentSessionId, setCurrentSessionId] = useState(null);
  const [analysisResults, setAnalysisResults] = useState(null);

  // EEG Upload Mutation
  const uploadEEGMutation = useMutation({
    mutationFn: (file) => {
      const formData = new FormData();
      formData.append('file', file);
      return api.post('/analysis/eeg/upload', formData);
    },
    onSuccess: (data) => {
      setCurrentSessionId(data.session_id);
      toast.success('EEG file uploaded successfully!');
      
      // Start polling for results
      pollForResults(data.session_id);
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Upload failed');
    }
  });

  // Text Analysis Mutation
  const textAnalysisMutation = useMutation({
    mutationFn: (text) => api.post('/analysis/text/analyze', { text }),
    onSuccess: (data) => {
      setAnalysisResults(data.results);
      toast.success('Text analysis completed!');
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Analysis failed');
    }
  });

  // Combined Analysis Mutation
  const combinedAnalysisMutation = useMutation({
    mutationFn: (data) => api.post('/analysis/combined', data),
    onSuccess: (data) => {
      setAnalysisResults(data);
      toast.success('Combined analysis completed!');
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Combined analysis failed');
    }
  });

  // Poll for EEG results
  const pollForResults = async (sessionId) => {
    let attempts = 0;
    const maxAttempts = 60; // 2 minutes with 2-second intervals
    
    const poll = async () => {
      try {
        const response = await api.get(`/analysis/eeg/result/${sessionId}`);
        
        if (response.status === 'completed') {
          setAnalysisResults(response.results);
          toast.success('EEG analysis completed!');
          return;
        }
        
        if (attempts < maxAttempts) {
          attempts++;
          setTimeout(poll, 2000);
        } else {
          toast.error('Analysis timeout. Please try again.');
        }
      } catch (error) {
        toast.error('Failed to get results');
      }
    };
    
    poll();
  };

  const handleEEGUpload = (file) => {
    uploadEEGMutation.mutate(file);
  };

  const handleTextSubmit = (text) => {
    if (text.trim().length < 10) {
      toast.error('Please provide more detailed text for analysis');
      return;
    }
    textAnalysisMutation.mutate(text);
  };

  const handleCombinedAnalysis = (eegSessionId, text) => {
    combinedAnalysisMutation.mutate({
      eeg_session_id: eegSessionId,
      text: text
    });
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Mental Health Analysis</h1>
        <p className="text-gray-600">
          Upload your EEG data and optionally provide text input for comprehensive mental health insights.
        </p>
      </div>

      {/* Analysis Tabs */}
      <div className="bg-white rounded-lg shadow-md">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6" aria-label="Tabs">
            {[
              { key: 'eeg', label: 'EEG Analysis', desc: 'Brainwave signal analysis' },
              { key: 'text', label: 'Text Analysis', desc: 'Mood from written input' },
              { key: 'combined', label: 'Combined Analysis', desc: 'EEG + Text fusion' }
            ].map((tab) => (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key)}
                className={`${
                  activeTab === tab.key
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors`}
              >
                <div>
                  <div>{tab.label}</div>
                  <div className="text-xs text-gray-400">{tab.desc}</div>
                </div>
              </button>
            ))}
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'eeg' && (
            <div className="space-y-6">
              <EEGUploader
                onUpload={handleEEGUpload}
                isUploading={uploadEEGMutation.isPending}
              />
              
              {analysisResults && (
                <EEGResultGrid
                  results={analysisResults}
                  sessionId={currentSessionId}
                />
              )}
            </div>
          )}

          {activeTab === 'text' && (
            <TextAnalysisPanel
              onSubmit={handleTextSubmit}
              isAnalyzing={textAnalysisMutation.isPending}
              results={analysisResults}
            />
          )}

          {activeTab === 'combined' && (
            <div className="space-y-6">
              <div className="bg-blue-50 p-4 rounded-lg">
                <h3 className="font-medium text-blue-900 mb-2">Combined Analysis</h3>
                <p className="text-blue-700 text-sm">
                  For the most accurate results, upload EEG data and provide text input about your current mood and feelings.
                </p>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-medium text-gray-900 mb-3">1. Upload EEG Data</h4>
                  <EEGUploader
                    onUpload={handleEEGUpload}
                    isUploading={uploadEEGMutation.isPending}
                    compact={true}
                  />
                </div>

                <div>
                  <h4 className="font-medium text-gray-900 mb-3">2. Describe Your Current State</h4>
                  <TextAnalysisPanel
                    onSubmit={(text) => handleCombinedAnalysis(currentSessionId, text)}
                    isAnalyzing={combinedAnalysisMutation.isPending}
                    compact={true}
                    placeholder="How are you feeling today? Describe your mood, energy level, any concerns..."
                  />
                </div>
              </div>

              {analysisResults && (
                <div className="mt-6">
                  <EEGResultGrid
                    results={analysisResults}
                    sessionId={currentSessionId}
                    isCombined={true}
                  />
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Information Panel */}
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-3">About Our Analysis</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div>
            <h3 className="font-medium text-purple-900 mb-2">EEG Analysis</h3>
            <p className="text-purple-700">
              Analyzes brainwave patterns to detect emotional states, anxiety levels, and cognitive load using advanced CNN-LSTM models.
            </p>
          </div>
          <div>
            <h3 className="font-medium text-blue-900 mb-2">Text Analysis</h3>
            <p className="text-blue-700">
              Uses natural language processing to identify depression indicators, mood patterns, and crisis signals from your written input.
            </p>
          </div>
          <div>
            <h3 className="font-medium text-indigo-900 mb-2">Combined Insights</h3>
            <p className="text-indigo-700">
              Fuses objective EEG data with subjective text input for comprehensive mental health assessment and personalized recommendations.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyzePage;