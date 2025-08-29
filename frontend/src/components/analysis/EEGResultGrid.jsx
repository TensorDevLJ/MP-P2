import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Download, Maximize2, RefreshCw, Share2, AlertTriangle } from 'lucide-react';
import StateCard from '../dashboard/StateCard';
import BandChart from './BandChart';
import PSDChart from './PSDChart';
import SpectrogramView from './SpectrogramView';
import ExplanationPanel from './ExplanationPanel';

const EEGResultGrid = ({ 
  sessionData,
  onSaveSession,
  onScheduleFollowup,
  onShare,
  onReanalyze 
}) => {
  const [selectedEpoch, setSelectedEpoch] = useState('aggregated');
  const [selectedTimeWindow, setSelectedTimeWindow] = useState(null);
  const [expandedChart, setExpandedChart] = useState(null);

  if (!sessionData) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-8 border border-gray-200 text-center">
        <p className="text-gray-500">No analysis results available</p>
      </div>
    );
  }

  const {
    fusion,
    emotion,
    anxiety,
    depression_text,
    charts,
    explain,
    recommendations,
    bands_timeseries,
    times,
    psd,
    spectrogram_image_base64,
    natural_explanation,
    safety_alerts,
  } = sessionData;

  const handleTimeWindowSelect = (window) => {
    setSelectedTimeWindow(window);
  };

  const handleExportReport = () => {
    console.log('Exporting comprehensive report...');
    // Would generate PDF with all charts and explanations
  };

  const handleFullScreenChart = (chartType) => {
    setExpandedChart(expandedChart === chartType ? null : chartType);
  };

  return (
    <div className="space-y-6">
      {/* Header Controls */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="bg-white rounded-xl shadow-lg p-4 border border-gray-200"
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <h2 className="text-xl font-bold text-gray-900">Analysis Results</h2>
            <span className="bg-success-100 text-success-700 px-3 py-1 rounded-full text-sm font-medium">
              Analysis Complete
            </span>
          </div>
          
          <div className="flex items-center space-x-3">
            {onReanalyze && (
              <button
                onClick={onReanalyze}
                className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg font-medium hover:bg-gray-200 transition-colors flex items-center space-x-2"
              >
                <RefreshCw className="h-4 w-4" />
                <span>Reanalyze</span>
              </button>
            )}
            
            <button
              onClick={handleExportReport}
              className="bg-primary-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-primary-700 transition-colors flex items-center space-x-2"
            >
              <Download className="h-4 w-4" />
              <span>Export Report</span>
            </button>
          </div>
        </div>
      </motion.div>

      {/* Top Section: State Card + Quick Stats */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
          >
            <StateCard
              state={fusion?.risk?.toUpperCase() || 'STABLE'}
              confidence={fusion?.confidence || 0}
              lastUpdated={sessionData.completed_at || new Date()}
              emotions={{
                primary: emotion?.label || 'neutral',
                secondary: anxiety ? `${anxiety.label} anxiety` : null
              }}
              textSentiment={depression_text?.label}
              recommendations={recommendations}
              onSaveSession={onSaveSession}
              onScheduleFollowup={onScheduleFollowup}
              onShare={onShare}
            />
          </motion.div>
        </div>
        
        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Analysis Breakdown</h3>
          <div className="space-y-4">
            {emotion && (
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-700">Primary Emotion</span>
                  <span className="text-sm text-gray-900 font-semibold capitalize">
                    {emotion.label}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-primary-600 h-2 rounded-full transition-all duration-1000"
                    style={{ width: `${Math.max(...Object.values(emotion.probs)) * 100}%` }}
                  />
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  Confidence: {Math.round(Math.max(...Object.values(emotion.probs)) * 100)}%
                </div>
              </div>
            )}

            {anxiety && (
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-700">Anxiety Level</span>
                  <span className="text-sm text-gray-900 font-semibold capitalize">
                    {anxiety.label}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-warning-500 h-2 rounded-full transition-all duration-1000"
                    style={{ width: `${anxiety.score * 100}%` }}
                  />
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  Score: {Math.round(anxiety.score * 100)}/100
                </div>
              </div>
            )}

            {depression_text && (
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-700">Depression Indicators</span>
                  <span className="text-sm text-gray-900 font-semibold capitalize">
                    {depression_text.label}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-error-500 h-2 rounded-full transition-all duration-1000"
                    style={{ width: `${Math.max(...Object.values(depression_text.probs)) * 100}%` }}
                  />
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  Based on text analysis
                </div>
              </div>
            )}

            {fusion && (
              <div className="pt-4 border-t border-gray-200">
                <div className="text-center">
                  <div className="text-lg font-bold text-gray-900">Overall Assessment</div>
                  <div className={`text-xl font-bold capitalize ${
                    fusion.risk === 'stable' ? 'text-success-600' :
                    fusion.risk === 'mild' ? 'text-warning-600' : 'text-error-600'
                  }`}>
                    {fusion.risk} Risk
                  </div>
                  <div className="text-sm text-gray-500">
                    {Math.round(fusion.confidence * 100)}% confidence
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        {bands_timeseries && times && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className={expandedChart === 'bands' ? 'xl:col-span-2' : ''}
          >
            <div className="relative">
              <button
                onClick={() => handleFullScreenChart('bands')}
                className="absolute top-4 right-4 z-10 p-2 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow"
                title="Toggle full screen"
              >
                <Maximize2 className="h-4 w-4 text-gray-600" />
              </button>
              
              <BandChart
                bandsTimeSeries={bands_timeseries}
                times={times}
                title="EEG Frequency Bands Over Time"
                selectedTimeWindow={selectedTimeWindow}
              />
            </div>
          </motion.div>
        )}

        {psd && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className={expandedChart === 'psd' ? 'xl:col-span-2' : ''}
          >
            <div className="relative">
              <button
                onClick={() => handleFullScreenChart('psd')}
                className="absolute top-4 right-4 z-10 p-2 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow"
                title="Toggle full screen"
              >
                <Maximize2 className="h-4 w-4 text-gray-600" />
              </button>
              
              <PSDChart
                psdData={psd}
                selectedEpoch={selectedEpoch}
                onEpochChange={setSelectedEpoch}
                title="Power Spectral Density Analysis"
              />
            </div>
          </motion.div>
        )}

        {spectrogram_image_base64 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="xl:col-span-2"
          >
            <div className="relative">
              <button
                onClick={() => handleFullScreenChart('spectrogram')}
                className="absolute top-4 right-4 z-10 p-2 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow"
                title="Toggle full screen"
              >
                <Maximize2 className="h-4 w-4 text-gray-600" />
              </button>
              
              <SpectrogramView
                spectrogramImage={spectrogram_image_base64}
                timeRange={sessionData.time_range || { start: 0, end: 60000 }}
                frequencyRange={{ min: 0, max: 50 }}
                onTimeWindowSelect={handleTimeWindowSelect}
                title="EEG Time-Frequency Spectrogram"
              />
            </div>
          </motion.div>
        )}
      </div>

      {/* Explanations Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.5 }}
      >
        <ExplanationPanel
          explanations={explain}
          sessionState={fusion}
          naturalLanguageExplanation={natural_explanation}
          safetyAlerts={safety_alerts || []}
          recommendations={recommendations}
          emotions={emotion}
          anxiety={anxiety}
          depression={depression_text}
        />
      </motion.div>
    </div>
  );
};

export default EEGResultGrid;