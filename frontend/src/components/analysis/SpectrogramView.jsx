import React, { useState } from 'react';
import { ZoomIn, ZoomOut, RotateCcw, Download, MousePointer } from 'lucide-react';

const SpectrogramView = ({ 
  spectrogramImage, 
  timeRange,
  frequencyRange,
  onTimeWindowSelect,
  title = "EEG Spectrogram"
}) => {
  const [selectedWindow, setSelectedWindow] = useState(null);
  const [zoomLevel, setZoomLevel] = useState(1);

  const handleImageClick = (event) => {
    if (!onTimeWindowSelect) return;
    
    const rect = event.target.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const relativeX = x / rect.width;
    
    // Calculate time window based on click position
    const totalDuration = timeRange.end - timeRange.start;
    const clickTime = timeRange.start + (totalDuration * relativeX);
    const windowSize = 2000; // 2 seconds in ms
    
    const windowStart = Math.max(timeRange.start, clickTime - windowSize / 2);
    const windowEnd = Math.min(timeRange.end, clickTime + windowSize / 2);
    
    setSelectedWindow({ start: windowStart, end: windowEnd });
    onTimeWindowSelect({ start: windowStart, end: windowEnd });
  };

  const downloadImage = () => {
    if (!spectrogramImage) return;
    
    const link = document.createElement('a');
    link.href = `data:image/png;base64,${spectrogramImage}`;
    link.download = `spectrogram-${Date.now()}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          <p className="text-sm text-gray-500">Time-frequency representation of EEG signals</p>
        </div>
        
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setZoomLevel(prev => Math.max(0.5, prev - 0.25))}
            className="p-2 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
            title="Zoom Out"
          >
            <ZoomOut className="h-4 w-4 text-gray-600" />
          </button>
          <button
            onClick={() => setZoomLevel(prev => Math.min(3, prev + 0.25))}
            className="p-2 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
            title="Zoom In"
          >
            <ZoomIn className="h-4 w-4 text-gray-600" />
          </button>
          <button
            onClick={() => setZoomLevel(1)}
            className="p-2 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
            title="Reset Zoom"
          >
            <RotateCcw className="h-4 w-4 text-gray-600" />
          </button>
          <button
            onClick={downloadImage}
            className="p-2 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
            title="Download Image"
          >
            <Download className="h-4 w-4 text-gray-600" />
          </button>
        </div>
      </div>

      {onTimeWindowSelect && (
        <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="flex items-center space-x-2">
            <MousePointer className="h-4 w-4 text-blue-600" />
            <span className="text-sm text-blue-700">
              Click on the spectrogram to select a time window for detailed analysis
            </span>
          </div>
        </div>
      )}

      {/* Spectrogram Display */}
      <div className="relative overflow-hidden rounded-lg border border-gray-200">
        {spectrogramImage ? (
          <div 
            className="relative cursor-crosshair"
            style={{ transform: `scale(${zoomLevel})`, transformOrigin: 'center top' }}
          >
            <img
              src={`data:image/png;base64,${spectrogramImage}`}
              alt="EEG Spectrogram"
              onClick={handleImageClick}
              className="w-full h-auto"
            />
            
            {/* Selected window overlay */}
            {selectedWindow && (
              <div 
                className="absolute top-0 bg-blue-200 bg-opacity-30 border-l-2 border-r-2 border-blue-500"
                style={{
                  left: `${((selectedWindow.start - timeRange.start) / (timeRange.end - timeRange.start)) * 100}%`,
                  width: `${((selectedWindow.end - selectedWindow.start) / (timeRange.end - timeRange.start)) * 100}%`,
                  height: '100%',
                }}
              />
            )}
          </div>
        ) : (
          <div className="h-64 flex items-center justify-center bg-gray-50">
            <div className="text-center text-gray-500">
              <Activity className="h-8 w-8 mx-auto mb-2" />
              <p>Generating spectrogram...</p>
            </div>
          </div>
        )}
      </div>

      {/* Color Scale Legend */}
      <div className="mt-4 flex items-center justify-between text-xs text-gray-600">
        <div className="flex items-center space-x-2">
          <span>Time →</span>
          <div className="w-4 h-2 bg-gradient-to-r from-blue-900 to-yellow-400 rounded"></div>
          <span>← Frequency</span>
        </div>
        <div className="flex items-center space-x-2">
          <span>Low Power</span>
          <div className="w-16 h-2 bg-gradient-to-r from-blue-900 via-green-500 to-yellow-400 rounded"></div>
          <span>High Power</span>
        </div>
      </div>

      {selectedWindow && (
        <div className="mt-4 p-3 bg-primary-50 border border-primary-200 rounded-lg">
          <p className="text-sm text-primary-700">
            Selected window: {((selectedWindow.end - selectedWindow.start) / 1000).toFixed(1)}s 
            ({new Date(selectedWindow.start).toLocaleTimeString()} - {new Date(selectedWindow.end).toLocaleTimeString()})
          </p>
        </div>
      )}

      <div className="mt-4 text-xs text-gray-500 text-center">
        Spectrogram visualizes how frequency content changes over time • Warmer colors indicate higher power
      </div>
    </div>
  );
};

export default SpectrogramView;