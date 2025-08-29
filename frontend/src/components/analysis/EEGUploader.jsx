// frontend/src/components/analysis/EEGUploader.jsx
import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { 
  Upload, 
  File, 
  CheckCircle, 
  AlertCircle, 
  Info,
  X
} from 'lucide-react';

const EEGUploader = ({ onUpload, isUploading, compact = false }) => {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [validationInfo, setValidationInfo] = useState(null);

  const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
    if (rejectedFiles.length > 0) {
      const error = rejectedFiles[0].errors[0];
      alert(`File rejected: ${error.message}`);
      return;
    }

    const file = acceptedFiles[0];
    if (file) {
      setUploadedFile(file);
      
      // Preview CSV content
      const reader = new FileReader();
      reader.onload = (e) => {
        const content = e.target.result;
        const lines = content.split('\n').slice(0, 6); // First 5 rows + header
        setPreview(lines);
        
        // Basic validation
        const header = lines[0];
        const samplingRate = detectSamplingRate(header);
        const channels = detectChannels(header);
        
        setValidationInfo({
          samplingRate,
          channels,
          fileSize: (file.size / 1024 / 1024).toFixed(2) + ' MB',
          rows: content.split('\n').length - 1
        });
      };
      reader.readAsText(file);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv']
    },
    maxSize: 50 * 1024 * 1024, // 50MB
    multiple: false
  });

  const handleUpload = () => {
    if (uploadedFile) {
      onUpload(uploadedFile);
    }
  };

  const handleRemove = () => {
    setUploadedFile(null);
    setPreview(null);
    setValidationInfo(null);
  };

  // Helper functions
  const detectSamplingRate = (header) => {
    const rates = [128, 256, 512, 1000];
    for (const rate of rates) {
      if (header.includes(rate.toString())) {
        return rate;
      }
    }
    return 128; // Default
  };

  const detectChannels = (header) => {
    const channels = [];
    const commonChannels = ['EEG', 'AF3', 'AF4', 'F3', 'F4', 'T7', 'T8'];
    
    for (const channel of commonChannels) {
      if (header.toLowerCase().includes(channel.toLowerCase())) {
        channels.push(channel);
      }
    }
    return channels;
  };

  if (compact) {
    return (
      <div className="space-y-4">
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-4 text-center cursor-pointer transition-colors ${
            isDragActive
              ? 'border-indigo-500 bg-indigo-50'
              : 'border-gray-300 hover:border-indigo-400'
          }`}
        >
          <input {...getInputProps()} />
          <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
          <p className="text-sm text-gray-600">
            {isDragActive ? 'Drop CSV file here' : 'Upload EEG CSV'}
          </p>
        </div>

        {uploadedFile && (
          <div className="bg-green-50 p-3 rounded-lg">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <CheckCircle className="w-4 h-4 text-green-500" />
                <span className="text-sm font-medium">{uploadedFile.name}</span>
              </div>
              <button
                onClick={handleUpload}
                disabled={isUploading}
                className="bg-indigo-600 text-white px-3 py-1 rounded text-xs hover:bg-indigo-700 disabled:opacity-50"
              >
                {isUploading ? 'Processing...' : 'Analyze'}
              </button>
            </div>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Upload Area */}
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-200 ${
          isDragActive
            ? 'border-indigo-500 bg-indigo-50 scale-102'
            : 'border-gray-300 hover:border-indigo-400 hover:bg-gray-50'
        }`}
      >
        <input {...getInputProps()} />
        <div className="space-y-4">
          <div className={`w-16 h-16 rounded-full flex items-center justify-center mx-auto ${
            isDragActive ? 'bg-indigo-100' : 'bg-gray-100'
          }`}>
            <Upload className={`w-8 h-8 ${
              isDragActive ? 'text-indigo-500' : 'text-gray-400'
            }`} />
          </div>
          
          <div>
            <p className="text-lg font-medium text-gray-900">
              {isDragActive ? 'Drop your EEG CSV file here' : 'Upload EEG Data'}
            </p>
            <p className="text-gray-500 mt-1">
              Drag and drop your CSV file or click to browse
            </p>
          </div>

          <div className="flex justify-center">
            <button
              type="button"
              className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Choose File
            </button>
          </div>
        </div>
      </div>

      {/* File Info */}
      {uploadedFile && (
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <div className="flex items-start justify-between mb-4">
            <div className="flex items-center space-x-3">
              <File className="w-8 h-8 text-blue-500" />
              <div>
                <h3 className="font-semibold text-gray-900">{uploadedFile.name}</h3>
                <p className="text-sm text-gray-500">
                  {validationInfo?.fileSize} • {validationInfo?.rows} rows
                </p>
              </div>
            </div>
            <button
              onClick={handleRemove}
              className="text-gray-400 hover:text-gray-600"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Validation Info */}
          {validationInfo && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div className="bg-blue-50 p-3 rounded-lg">
                <div className="flex items-center space-x-2">
                  <Info className="w-4 h-4 text-blue-500" />
                  <span className="text-sm font-medium text-blue-900">Sampling Rate</span>
                </div>
                <p className="text-blue-700 mt-1">{validationInfo.samplingRate} Hz</p>
              </div>
              
              <div className="bg-green-50 p-3 rounded-lg">
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span className="text-sm font-medium text-green-900">Channels</span>
                </div>
                <p className="text-green-700 mt-1">
                  {validationInfo.channels.length > 0 
                    ? validationInfo.channels.join(', ') 
                    : 'Auto-detect'}
                </p>
              </div>
              
              <div className="bg-purple-50 p-3 rounded-lg">
                <div className="flex items-center space-x-2">
                  <File className="w-4 h-4 text-purple-500" />
                  <span className="text-sm font-medium text-purple-900">Duration</span>
                </div>
                <p className="text-purple-700 mt-1">
                  ~{Math.round(validationInfo.rows / validationInfo.samplingRate)}s
                </p>
              </div>
            </div>
          )}

          {/* Preview */}
          {preview && (
            <div className="mb-4">
              <h4 className="text-sm font-medium text-gray-900 mb-2">Data Preview</h4>
              <div className="bg-gray-50 rounded-md p-3 overflow-x-auto">
                <pre className="text-xs font-mono text-gray-600">
                  {preview.slice(0, 5).join('\n')}
                  {preview.length > 5 && '\n...'}
                </pre>
              </div>
            </div>
          )}

          {/* Upload Button */}
          <div className="flex justify-end space-x-3">
            <button
              onClick={handleRemove}
              className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
            >
              Remove
            </button>
            <button
              onClick={handleUpload}
              disabled={isUploading}
              className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
            >
              {isUploading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Processing...</span>
                </>
              ) : (
                <>
                  <Upload className="w-4 h-4" />
                  <span>Start Analysis</span>
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* Instructions */}
      <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
        <div className="flex items-start space-x-3">
          <AlertCircle className="w-5 h-5 text-amber-500 mt-0.5" />
          <div>
            <h4 className="font-medium text-amber-900 mb-2">CSV Format Requirements</h4>
            <ul className="text-sm text-amber-800 space-y-1">
              <li>• Include sampling rate in header (e.g., "EEG_128Hz")</li>
              <li>• Minimum 2 seconds of data required</li>
              <li>• Common channel names: EEG, AF3, AF4, F3, F4, etc.</li>
              <li>• Maximum file size: 50MB</li>
              <li>• Data should be in microvolts (µV)</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EEGUploader;