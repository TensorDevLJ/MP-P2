import React, { useState, useMemo } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import { ToggleLeft, ToggleRight, Activity } from 'lucide-react';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const PSDChart = ({ 
  psdData, 
  selectedEpoch = 'aggregated',
  onEpochChange,
  title = "Power Spectral Density"
}) => {
  const [logScale, setLogScale] = useState(true);
  const [selectedFreqRange, setSelectedFreqRange] = useState('full');

  const frequencyRanges = {
    full: { min: 0, max: 50, label: 'Full Range (0-50 Hz)' },
    alpha: { min: 8, max: 13, label: 'Alpha Band (8-13 Hz)' },
    beta: { min: 13, max: 30, label: 'Beta Band (13-30 Hz)' },
    gamma: { min: 30, max: 50, label: 'Gamma Band (30-50 Hz)' },
  };

  const filteredData = useMemo(() => {
    if (!psdData?.freqs || !psdData?.power) return null;

    const range = frequencyRanges[selectedFreqRange];
    const filteredIndices = psdData.freqs
      .map((freq, index) => freq >= range.min && freq <= range.max ? index : null)
      .filter(index => index !== null);

    const freqs = filteredIndices.map(i => psdData.freqs[i]);
    const power = filteredIndices.map(i => psdData.power[i]);

    return {
      labels: freqs.map(f => f.toFixed(1)),
      datasets: [
        {
          label: 'Power Spectral Density',
          data: power,
          borderColor: '#3B82F6',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          fill: true,
          tension: 0.2,
          pointRadius: 0,
          borderWidth: 2,
        },
      ],
    };
  }, [psdData, selectedFreqRange]);

  const options = useMemo(() => ({
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        titleColor: '#1f2937',
        bodyColor: '#374151',
        borderColor: '#d1d5db',
        borderWidth: 1,
        cornerRadius: 8,
        callbacks: {
          title: (context) => `Frequency: ${context[0].label} Hz`,
          label: (context) => `Power: ${context.parsed.y.toFixed(4)} μV²/Hz`,
        },
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Frequency (Hz)',
          font: { weight: 'bold' },
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        },
      },
      y: {
        type: logScale ? 'logarithmic' : 'linear',
        title: {
          display: true,
          text: 'Power (μV²/Hz)',
          font: { weight: 'bold' },
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        },
      },
    },
    animation: {
      duration: 800,
      easing: 'easeInOutCubic',
    },
  }), [logScale]);

  if (!psdData) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200 h-96 flex items-center justify-center">
        <div className="text-center text-gray-500">
          <Activity className="h-8 w-8 mx-auto mb-2" />
          <p>No PSD data available</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          <p className="text-sm text-gray-500">Frequency domain analysis</p>
        </div>
      </div>

      {/* Controls */}
      <div className="flex flex-wrap items-center justify-between gap-4 mb-6 p-4 bg-gray-50 rounded-lg">
        <div className="flex items-center space-x-4">
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Scale</label>
            <button
              onClick={() => setLogScale(!logScale)}
              className="flex items-center space-x-2 px-3 py-1.5 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              {logScale ? (
                <ToggleRight className="h-4 w-4 text-primary-600" />
              ) : (
                <ToggleLeft className="h-4 w-4 text-gray-400" />
              )}
              <span className="text-sm">{logScale ? 'Log' : 'Linear'}</span>
            </button>
          </div>
          
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Range</label>
            <select
              value={selectedFreqRange}
              onChange={(e) => setSelectedFreqRange(e.target.value)}
              className="px-3 py-1.5 bg-white border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              {Object.entries(frequencyRanges).map(([key, range]) => (
                <option key={key} value={key}>{range.label}</option>
              ))}
            </select>
          </div>
        </div>

        {onEpochChange && (
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Epoch</label>
            <select
              value={selectedEpoch}
              onChange={(e) => onEpochChange(e.target.value)}
              className="px-3 py-1.5 bg-white border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="aggregated">Aggregated</option>
              <option value="1">Epoch 1</option>
              <option value="2">Epoch 2</option>
              <option value="3">Epoch 3</option>
              {/* More epochs would be dynamically generated */}
            </select>
          </div>
        )}
      </div>

      {/* Chart */}
      <div className="h-80 mb-4">
        {filteredData ? (
          <Line data={filteredData} options={options} />
        ) : (
          <div className="h-full flex items-center justify-center text-gray-500">
            <div className="text-center">
              <Activity className="h-8 w-8 mx-auto mb-2" />
              <p>Loading PSD data...</p>
            </div>
          </div>
        )}
      </div>

      <div className="text-xs text-gray-500 text-center">
        Power spectral density shows frequency-domain representation of EEG signals
      </div>
    </div>
  );
};

export default PSDChart;