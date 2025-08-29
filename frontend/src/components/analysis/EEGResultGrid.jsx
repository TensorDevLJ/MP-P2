import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Brain,
  TrendingUp,
  Download,
  Share,
  RefreshCw,
  AlertTriangle,
  CheckCircle,
  Info,
  Activity,
  Zap,
} from 'lucide-react';
import StateCard from '../dashboard/StateCard';
import BandChart from './BandChart';
import PSDChart from './PSDChart';
import SpectrogramView from './SpectrogramView';
import ExplanationPanel from './ExplanationPanel';

const EEGResultGrid = ({ results, analysisMode, onNewAnalysis }) => {
  const [selectedEpoch, setSelectedEpoch] = useState(0);
  const [activeChart, setActiveChart] = useState('bands');

  if (!results) return null;

  const getRiskColor = (risk) => {
    switch (risk?.toLowerCase()) {
      case 'stable':
      case 'low':
        return 'text-green-600 dark:text-green-400 bg-green-100 dark:bg-green-900/30';
      case 'mild':
      case 'moderate':
        return 'text-yellow-600 dark:text-yellow-400 bg-yellow-100 dark:bg-yellow-900/30';
      case 'high':
      case 'severe':
        return 'text-red-600 dark:text-red-400 bg-red-100 dark:bg-red-900/30';
      default:
        return 'text-slate-600 dark:text-slate-400 bg-slate-100 dark:bg-slate-700';
    }
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return 'text-green-600 dark:text-green-400';
    if (confidence >= 0.6) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Header with Actions */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white">
            Analysis Results
          </h1>
          <p className="text-slate-600 dark:text-slate-400">
            Session completed • {new Date().toLocaleString()}
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="flex items-center space-x-2 px-4 py-2 bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-600 transition-colors"
          >
            <Download className="w-4 h-4" />
            <span>Export</span>
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="flex items-center space-x-2 px-4 py-2 bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-600 transition-colors"
          >
            <Share className="w-4 h-4" />
            <span>Share</span>
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={onNewAnalysis}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            <span>New Analysis</span>
          </motion.button>
        </div>
      </div>

      {/* Main Results Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* State Card - Full width on mobile, spans 1 column on desktop */}
        <div className="lg:col-span-1">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-white dark:bg-slate-800 rounded-xl p-6 shadow-sm border border-slate-200 dark:border-slate-700 h-fit"
          >
            <div className="flex items-center space-x-2 mb-4">
              <Brain className="w-5 h-5 text-blue-600" />
              <h2 className="text-lg font-semibold text-slate-800 dark:text-white">
                Mental State
              </h2>
            </div>

            {/* Overall Risk Level */}
            <div className="space-y-4">
              <div>
                <p className="text-sm text-slate-600 dark:text-slate-400 mb-2">Overall Assessment</p>
                <div className={`inline-flex items-center space-x-2 px-3 py-1.5 rounded-full text-sm font-medium ${getRiskColor(results.fusion?.risk || results.overall_risk)}`}>
                  {results.fusion?.risk === 'high' || results.overall_risk === 'severe' ? (
                    <AlertTriangle className="w-4 h-4" />
                  ) : (
                    <CheckCircle className="w-4 h-4" />
                  )}
                  <span className="capitalize">
                    {results.fusion?.risk || results.overall_risk || 'Unknown'}
                  </span>
                </div>
              </div>

              <div>
                <p className="text-sm text-slate-600 dark:text-slate-400 mb-2">Confidence</p>
                <div className="flex items-center space-x-2">
                  <div className={`text-lg font-bold ${getConfidenceColor(results.fusion?.confidence || results.confidence || 0)}`}>
                    {Math.round((results.fusion?.confidence || results.confidence || 0) * 100)}%
                  </div>
                  <div className="flex-1 bg-slate-200 dark:bg-slate-700 rounded-full h-2">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${(results.fusion?.confidence || results.confidence || 0) * 100}%` }}
                      transition={{ duration: 1, delay: 0.5 }}
                      className={`h-2 rounded-full ${
                        (results.fusion?.confidence || results.confidence || 0) >= 0.8
                          ? 'bg-green-500'
                          : (results.fusion?.confidence || results.confidence || 0) >= 0.6
                          ? 'bg-yellow-500'
                          : 'bg-red-500'
                      }`}
                    />
                  </div>
                </div>
              </div>

              {/* Individual Scores */}
              {results.emotion && (
                <div>
                  <p className="text-sm text-slate-600 dark:text-slate-400 mb-2">Emotion</p>
                  <div className="text-sm">
                    <span className="font-medium text-slate-800 dark:text-white capitalize">
                      {results.emotion.label}
                    </span>
                    <span className="text-slate-500 dark:text-slate-500 ml-2">
                      ({Math.round((results.emotion.probs?.[results.emotion.label] || 0) * 100)}%)
                    </span>
                  </div>
                </div>
              )}

              {results.anxiety && (
                <div>
                  <p className="text-sm text-slate-600 dark:text-slate-400 mb-2">Anxiety Level</p>
                  <div className="text-sm">
                    <span className="font-medium text-slate-800 dark:text-white capitalize">
                      {results.anxiety.label}
                    </span>
                    <span className="text-slate-500 dark:text-slate-500 ml-2">
                      (Score: {results.anxiety.score?.toFixed(2) || 'N/A'})
                    </span>
                  </div>
                </div>
              )}

              {results.depression_text && (
                <div>
                  <p className="text-sm text-slate-600 dark:text-slate-400 mb-2">Depression Indicators</p>
                  <div className="text-sm">
                    <span className="font-medium text-slate-800 dark:text-white capitalize">
                      {results.depression_text.label}
                    </span>
                    <span className="text-slate-500 dark:text-slate-500 ml-2">
                      ({Math.round((results.depression_text.probs?.[results.depression_text.label] || 0) * 100)}%)
                    </span>
                  </div>
                </div>
              )}
            </div>

            {/* Quick Recommendations */}
            {results.recommendations && results.recommendations.length > 0 && (
              <div className="mt-6 pt-6 border-t border-slate-200 dark:border-slate-700">
                <p className="text-sm font-medium text-slate-800 dark:text-white mb-3">
                  Quick Recommendations
                </p>
                <div className="space-y-2">
                  {results.recommendations.slice(0, 2).map((rec, index) => (
                    <div key={index} className="text-xs bg-blue-50 dark:bg-blue-900/20 rounded-lg p-2">
                      <p className="font-medium text-blue-800 dark:text-blue-200">
                        {rec.title}
                      </p>
                      {rec.duration && (
                        <p className="text-blue-600 dark:text-blue-400">
                          Duration: {rec.duration} min
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        </div>

        {/* Charts Section - Spans 3 columns */}
        <div className="lg:col-span-3 space-y-6">
          {/* Chart Type Selector */}
          {(analysisMode === 'eeg' || analysisMode === 'combined') && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="flex space-x-1 bg-slate-100 dark:bg-slate-700 rounded-lg p-1 w-fit"
            >
              {[
                { id: 'bands', label: 'Band Powers', icon: Activity },
                { id: 'psd', label: 'PSD', icon: TrendingUp },
                { id: 'spectrogram', label: 'Spectrogram', icon: Zap },
              ].map((chart) => {
                const Icon = chart.icon;
                return (
                  <motion.button
                    key={chart.id}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => setActiveChart(chart.id)}
                    className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                      activeChart === chart.id
                        ? 'bg-white dark:bg-slate-600 text-blue-600 dark:text-blue-400 shadow-sm'
                        : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{chart.label}</span>
                  </motion.button>
                );
              })}
            </motion.div>
          )}

          {/* Chart Display */}
          {(analysisMode === 'eeg' || analysisMode === 'combined') && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="bg-white dark:bg-slate-800 rounded-xl p-6 shadow-sm border border-slate-200 dark:border-slate-700"
            >
              {activeChart === 'bands' && (
                <BandChart
                  data={results.charts?.bands || results.bands_timeseries}
                  selectedEpoch={selectedEpoch}
                  onEpochSelect={setSelectedEpoch}
                />
              )}

              {activeChart === 'psd' && (
                <PSDChart
                  data={results.charts?.psd || results.psd}
                  selectedEpoch={selectedEpoch}
                />
              )}

              {activeChart === 'spectrogram' && (
                <SpectrogramView
                  data={results.charts?.spectrogram || results.spectrogram_image_base64}
                  onTimeSelect={(time) => console.log('Time selected:', time)}
                />
              )}
            </motion.div>
          )}

          {/* Text Analysis Results */}
          {(analysisMode === 'text' || analysisMode === 'combined') && results.depression_text && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="bg-white dark:bg-slate-800 rounded-xl p-6 shadow-sm border border-slate-200 dark:border-slate-700"
            >
              <div className="flex items-center space-x-2 mb-4">
                <Info className="w-5 h-5 text-purple-600" />
                <h2 className="text-lg font-semibold text-slate-800 dark:text-white">
                  Text Analysis Results
                </h2>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {Object.entries(results.depression_text.probs || {}).map(([label, prob]) => (
                  <div key={label} className="text-center">
                    <div className={`w-16 h-16 mx-auto rounded-full flex items-center justify-center mb-2 ${
                      label === results.depression_text.label
                        ? getRiskColor(label)
                        : 'bg-slate-100 dark:bg-slate-700 text-slate-500'
                    }`}>
                      <span className="text-lg font-bold">
                        {Math.round(prob * 100)}%
                      </span>
                    </div>
                    <p className="text-sm font-medium text-slate-800 dark:text-white capitalize">
                      {label}
                    </p>
                  </div>
                ))}
              </div>
            </motion.div>
          )}
        </div>
      </div>

      {/* Explanation Panel */}
      <ExplanationPanel
        results={results}
        analysisMode={analysisMode}
      />

      {/* Safety Notice */}
      {(results.fusion?.risk === 'high' || results.overall_risk === 'severe') && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl p-6"
        >
          <div className="flex items-start space-x-3">
            <AlertTriangle className="w-6 h-6 text-red-600 dark:text-red-400 mt-0.5" />
            <div>
              <h3 className="text-lg font-semibold text-red-800 dark:text-red-200 mb-2">
                Important Notice
              </h3>
              <p className="text-red-700 dark:text-red-300 mb-4">
                Your analysis indicates elevated risk levels. While this tool provides insights, 
                it's not a substitute for professional medical advice.
              </p>
              <div className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-3">
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium"
                >
                  Find Professional Help
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="px-4 py-2 border border-red-300 dark:border-red-700 text-red-700 dark:text-red-300 rounded-lg hover:bg-red-100 dark:hover:bg-red-900/30 transition-colors"
                >
                  Emergency Resources
                </motion.button>
              </div>
            </div>
          </div>
        </motion.div>
      )}

      {/* Next Steps */}
      {results.next_actions && results.next_actions.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="bg-white dark:bg-slate-800 rounded-xl p-6 shadow-sm border border-slate-200 dark:border-slate-700"
        >
          <h2 className="text-lg font-semibold text-slate-800 dark:text-white mb-4">
            Recommended Next Steps
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {results.next_actions.map((action, index) => (
              <motion.div
                key={index}
                whileHover={{ scale: 1.02 }}
                className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800 cursor-pointer"
              >
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium">
                    {index + 1}
                  </div>
                  <p className="text-blue-800 dark:text-blue-200 font-medium">
                    {action}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}
    </motion.div>
  );
};

export default EEGResultGrid;