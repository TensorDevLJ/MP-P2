import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, AlertTriangle, CheckCircle, Brain, Settings, Eye } from 'lucide-react';
import { validateCSVFile, parseCSVSampleRate } from '../../utils/helpers';
import LoadingSpinner from '../common/LoadingSpinner';

const EEGUploader = ({ 
  onFileUpload, 
  onAnalysisStart, 
  includeTextAnalysis = false,
  setIncludeTextAnalysis 
}) => {
  const [file, setFile] = useState(null);
  const [textInput, setTextInput] = useState('');
  const [samplingRate, setSamplingRate] = useState(256);
  const [selectedChannel, setSelectedChannel] = useState('EEG.AF3');
  const [analysisType, setAnalysisType] = useState('raw');
  const [epochLength, setEpochLength] = useState(2);
  const [overlap, setOverlap] = useState(50);
  const [preview, setPreview] = useState(null);
  const [errors, setErrors] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [showAdvanced, setShowAdvanced] = useState(false);

  const onDrop = useCallback((acceptedFiles) => {
    const uploadedFile = acceptedFiles[0];
    const validationErrors = validateCSVFile(uploadedFile);
    
    if (validationErrors.length > 0) {
      setErrors(validationErrors);
      return;
    }

    setErrors([]);
    setFile(uploadedFile);
    
    // Auto-detect sampling rate from filename
    const detectedSR = parseCSVSampleRate(uploadedFile.name);
    if (detectedSR) {
      setSamplingRate(detectedSR);
    }

    // Read first few rows for preview
    const reader = new FileReader();
    reader.onload = (e) => {
      const text = e.target.result;
      const lines = text.split('\n').slice(0, 11); // Header + 10 rows
      setPreview(lines);
    };
    reader.readAsText(uploadedFile);

    onFileUpload?.(uploadedFile);
  }, [onFileUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'application/json': ['.json'],
      'text/plain': ['.txt'],
    },
    maxSize: 50 * 1024 * 1024, // 50MB
    multiple: false,
  });

  const handleAnalysisStart = () => {
    if (!file && analysisType === 'raw') {
      setErrors(['Please upload a file before starting analysis']);
      return;
    }

    if (includeTextAnalysis && textInput.trim().length < 10) {
      setErrors(['Please provide at least 10 characters of text for meaningful analysis']);
      return;
    }

    setUploading(true);
    
    const analysisData = {
      file: analysisType === 'raw' ? file : null,
      text: includeTextAnalysis ? textInput : null,
      samplingRate,
      selectedChannel,
      analysisType,
      epochLength,
      overlap,
    };

    onAnalysisStart?.(analysisData);
  };

  const channels = [
    'EEG.AF3', 'EEG.AF4', 'EEG.T7', 'EEG.T8', 'EEG.Pz', 'EEG.O1', 'EEG.O2',
    'EEG.F3', 'EEG.F4', 'EEG.C3', 'EEG.C4', 'EEG.P3', 'EEG.P4'
  ];

  const presetConfigs = {
    quick: { epochLength: 2, overlap: 25, samplingRate: 256 },
    standard: { epochLength: 4, overlap: 50, samplingRate: 256 },
    detailed: { epochLength: 8, overlap: 75, samplingRate: 512 },
  };

  const applyPreset = (preset) => {
    const config = presetConfigs[preset];
    setEpochLength(config.epochLength);
    setOverlap(config.overlap);
    setSamplingRate(config.samplingRate);
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
      <div className="flex items-center space-x-3 mb-6">
        <div className="p-2 bg-primary-100 rounded-lg">
          <Upload className="h-5 w-5 text-primary-600" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-gray-900">EEG Data Analysis</h3>
          <p className="text-sm text-gray-500">Upload your EEG data for AI-powered mental health insights</p>
        </div>
      </div>

      {errors.length > 0 && (
        <div className="mb-6 p-4 bg-error-50 border border-error-200 rounded-lg">
          <div className="flex items-start space-x-2">
            <AlertTriangle className="h-5 w-5 text-error-600 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="text-sm font-semibold text-error-700">Upload Issues</h4>
              <ul className="mt-1 text-sm text-error-600 list-disc list-inside">
                {errors.map((error, index) => (
                  <li key={index}>{error}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Analysis Type Toggle */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-3">Analysis Type</label>
        <div className="flex space-x-3">
          <button
            onClick={() => setAnalysisType('raw')}
            className={`flex-1 p-3 border rounded-lg text-sm font-medium transition-colors ${
              analysisType === 'raw'
                ? 'border-primary-500 bg-primary-50 text-primary-700'
                : 'border-gray-300 bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            Raw EEG Data
          </button>
          <button
            onClick={() => setAnalysisType('features')}
            className={`flex-1 p-3 border rounded-lg text-sm font-medium transition-colors ${
              analysisType === 'features'
                ? 'border-primary-500 bg-primary-50 text-primary-700'
                : 'border-gray-300 bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            Precomputed Features
          </button>
        </div>
      </div>

      {analysisType === 'raw' && (
        <>
          {/* File Upload Area */}
          <div
            {...getRootProps()}
            className={`mb-6 p-8 border-2 border-dashed rounded-xl text-center cursor-pointer transition-colors ${
              isDragActive
                ? 'border-primary-400 bg-primary-50'
                : file
                ? 'border-success-400 bg-success-50'
                : 'border-gray-300 bg-gray-50 hover:border-gray-400'
            }`}
          >
            <input {...getInputProps()} />
            
            <div className="space-y-3">
              {file ? (
                <CheckCircle className="h-12 w-12 text-success-600 mx-auto" />
              ) : (
                <FileText className="h-12 w-12 text-gray-400 mx-auto" />
              )}
              
              <div>
                {file ? (
                  <>
                    <p className="text-lg font-semibold text-success-700">{file.name}</p>
                    <p className="text-sm text-success-600">
                      {(file.size / 1024 / 1024).toFixed(2)} MB • Ready for analysis
                    </p>
                  </>
                ) : (
                  <>
                    <p className="text-lg font-semibold text-gray-700">
                      {isDragActive ? 'Drop your file here' : 'Upload EEG Data'}
                    </p>
                    <p className="text-sm text-gray-500">
                      Drag & drop CSV, JSON, or TXT file or click to browse (Max 50MB)
                    </p>
                  </>
                )}
              </div>
            </div>
          </div>

          {/* Configuration Presets */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-3">Quick Presets</label>
            <div className="flex space-x-3">
              {Object.entries(presetConfigs).map(([key, config]) => (
                <button
                  key={key}
                  onClick={() => applyPreset(key)}
                  className="flex-1 p-3 border border-gray-300 rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors capitalize"
                >
                  {key}
                  <div className="text-xs text-gray-500 mt-1">
                    {config.epochLength}s epochs, {config.overlap}% overlap
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Basic Configuration */}
          {file && (
            <div className="mb-6 p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-2">
                  <Settings className="h-4 w-4 text-gray-600" />
                  <span className="text-sm font-medium text-gray-700">Analysis Configuration</span>
                </div>
                <button
                  onClick={() => setShowAdvanced(!showAdvanced)}
                  className="text-primary-600 hover:text-primary-700 text-sm font-medium flex items-center space-x-1"
                >
                  <Eye className="h-4 w-4" />
                  <span>{showAdvanced ? 'Hide' : 'Show'} Advanced</span>
                </button>
              </div>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Sampling Rate (Hz)
                  </label>
                  <input
                    type="number"
                    value={samplingRate}
                    onChange={(e) => setSamplingRate(Number(e.target.value))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    min="1"
                    max="10000"
                  />
                  <p className="text-xs text-gray-500 mt-1">Common: 128, 256, 512 Hz</p>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Primary Channel
                  </label>
                  <select
                    value={selectedChannel}
                    onChange={(e) => setSelectedChannel(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  >
                    {channels.map((channel) => (
                      <option key={channel} value={channel}>{channel}</option>
                    ))}
                  </select>
                </div>

                {showAdvanced && (
                  <>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Epoch Length (seconds)
                      </label>
                      <input
                        type="number"
                        value={epochLength}
                        onChange={(e) => setEpochLength(Number(e.target.value))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                        min="1"
                        max="10"
                        step="0.5"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Overlap (%)
                      </label>
                      <input
                        type="number"
                        value={overlap}
                        onChange={(e) => setOverlap(Number(e.target.value))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                        min="0"
                        max="90"
                        step="5"
                      />
                    </div>
                  </>
                )}
              </div>
            </div>
          )}

          {/* Preview */}
          {preview && (
            <div className="mb-6">
              <h4 className="text-sm font-semibold text-gray-700 mb-3">Data Preview</h4>
              <div className="bg-gray-50 rounded-lg p-4 text-xs font-mono max-h-40 overflow-auto">
                {preview.map((line, index) => (
                  <div key={index} className={index === 0 ? 'font-bold text-gray-800' : 'text-gray-600'}>
                    {line}
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}

      {/* Text Analysis Option */}
      <div className="mb-6">
        <label className="flex items-center space-x-3 cursor-pointer">
          <input
            type="checkbox"
            checked={includeTextAnalysis}
            onChange={(e) => setIncludeTextAnalysis(e.target.checked)}
            className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500 border-gray-300"
          />
          <span className="text-sm font-medium text-gray-700">
            Also analyze text/journal entry for depression screening
          </span>
        </label>
      </div>

      {includeTextAnalysis && (
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            How are you feeling today? Share your thoughts...
          </label>
          <textarea
            value={textInput}
            onChange={(e) => setTextInput(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 resize-none"
            rows="4"
            placeholder="Share your thoughts, mood, or any symptoms you've been experiencing. This helps improve the accuracy of your mental health assessment..."
            maxLength="5000"
          />
          <div className="flex justify-between mt-1 text-xs text-gray-500">
            <span>Minimum 10 characters for meaningful analysis</span>
            <span className={textInput.length > 4500 ? 'text-error-600 font-medium' : ''}>
              {textInput.length}/5000
            </span>
          </div>
        </div>
      )}

      {/* Start Analysis Button */}
      <button
        onClick={handleAnalysisStart}
        disabled={uploading || (!file && analysisType === 'raw')}
        className="w-full bg-primary-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-primary-700 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center space-x-2"
      >
        {uploading ? (
          <LoadingSpinner size="small" message="" />
        ) : (
          <>
            <Brain className="h-5 w-5" />
            <span>
              {analysisType === 'raw' ? 'Start EEG Analysis' : 'Analyze Features'}
              {includeTextAnalysis && ' + Text'}
            </span>
          </>
        )}
      </button>

      <div className="mt-4 p-3 bg-warning-50 border border-warning-200 rounded-lg">
        <div className="flex items-start space-x-2">
          <AlertTriangle className="h-4 w-4 text-warning-600 flex-shrink-0 mt-0.5" />
          <div className="text-xs text-warning-700">
            <p className="font-medium mb-1">Analysis Information</p>
            <p>
              EEG analysis typically takes 15-60 seconds depending on file size and configuration. 
              Results provide supportive insights and should not replace professional medical evaluation. 
              All data is processed securely and deleted after analysis completion.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EEGUploader;