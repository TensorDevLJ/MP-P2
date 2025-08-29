import React, { useState, useMemo } from 'react';
import { Line } from 'react-chartjs-2';
import { motion } from 'framer-motion';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { Eye, EyeOff, Download, ZoomIn } from 'lucide-react';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const BandChart = ({ data, selectedEpoch, onEpochSelect }) => {
  const [visibleBands, setVisibleBands] = useState({
    delta: true,
    theta: true,
    alpha: true,
    beta: true,
    gamma: true,
  });
  const [showAsArea, setShowAsArea] = useState(false);

  const bandConfig = {
    delta: { 
      color: 'rgba(239, 68, 68, 1)', 
      bgColor: 'rgba(239, 68, 68, 0.1)',
      label: 'Delta (0.5-4 Hz)',
      description: 'Deep sleep, healing'
    },
    theta: { 
      color: 'rgba(245, 158, 11, 1)', 
      bgColor: 'rgba(245, 158, 11, 0.1)',
      label: 'Theta (4-8 Hz)',
      description: 'Creativity, meditation'
    },
    alpha: { 
      color: 'rgba(34, 197, 94, 1)', 
      bgColor: 'rgba(34, 197, 94, 0.1)',
      label: 'Alpha (8-13 Hz)',
      description: 'Relaxed awareness'
    },
    beta: { 
      color: 'rgba(59, 130, 246, 1)', 
      bgColor: 'rgba(59, 130, 246, 0.1)',
      label: 'Beta (13-30 Hz)',
      description: 'Active thinking, focus'
    },
    gamma: { 
      color: 'rgba(168, 85, 247, 1)', 
      bgColor: 'rgba(168, 85, 247, 0.1)',
      label: 'Gamma (30-45 Hz)',
      description: 'High-level cognition'
    },
  };

  const chartData = useMemo(() => {
    if (!data || !data.times || !data.bands_timeseries) {
      // Generate mock data for demo
      const mockTimes = Array.from({ length: 50 }, (_, i) => i * 2);
      const generateMockBand = (base, variance) => 
        mockTimes.map(() => base + (Math.random() - 0.5) * variance);

      return {
        times: mockTimes,
        bands_timeseries: {
          delta: generateMockBand(15, 8),
          theta: generateMockBand(20, 10),
          alpha: generateMockBand(25, 12),
          beta: generateMockBand(18, 15),
          gamma: generateMockBand(10, 8),
        }
      };
    }
    return data;
  }, [data]);

  const chartJsData = {
    labels: chartData.times?.map(t => `${t}s`) || [],
    datasets: Object.entries(bandConfig)
      .filter(([band]) => visibleBands[band] && chartData.bands_timeseries?.[band])
      .map(([band, config]) => ({
        label: config.label,
        data: chartData.bands_timeseries[band],
        borderColor: config.color,
        backgroundColor: showAsArea ? config.bgColor : 'transparent',
        borderWidth: 2,
        pointRadius: 0,
        pointHoverRadius: 4,
        fill: showAsArea,
        tension: 0.4,
      })),
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false, // We'll use custom legend
      },
      title: {
        display: true,
        text: 'EEG Band Powers Over Time',
        font: { size: 16, weight: 'bold' },
        color: document.documentElement.classList.contains('dark') ? '#ffffff' : '#1f2937',
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#ffffff',
        bodyColor: '#ffffff',
        borderColor: 'rgba(255, 255, 255, 0.2)',
        borderWidth: 1,
        callbacks: {
          title: (tooltipItems) => {
            return `Time: ${tooltipItems[0].label}`;
          },
          label: (context) => {
            return `${context.dataset.label}: ${context.parsed.y.toFixed(2)} μV²`;
          },
        },
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Time (seconds)',
          color: document.documentElement.classList.contains('dark') ? '#9ca3af' : '#6b7280',
        },
        grid: {
          color: document.documentElement.classList.contains('dark') ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)',
        },
        ticks: {
          color: document.documentElement.classList.contains('dark') ? '#9ca3af' : '#6b7280',
        },
      },
      y: {
        title: {
          display: true,
          text: 'Power (μV²)',
          color: document.documentElement.classList.contains('dark') ? '#9ca3af' : '#6b7280',
        },
        grid: {
          color: document.documentElement.classList.contains('dark') ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)',
        },
        ticks: {
          color: document.documentElement.classList.contains('dark') ? '#9ca3af' : '#6b7280',
        },
        beginAtZero: true,
      },
    },
    interaction: {
      mode: 'nearest',
      axis: 'x',
      intersect: false,
    },
    onHover: (event, activeElements) => {
      if (activeElements.length > 0) {
        const epochIndex = activeElements[0].index;
        if (onEpochSelect && epochIndex !== selectedEpoch) {
          onEpochSelect(epochIndex);
        }
      }
    },
  };

  const toggleBandVisibility = (band) => {
    setVisibleBands(prev => ({ ...prev, [band]: !prev[band] }));
  };

  const downloadChart = () => {
    // Implementation for downloading chart as PNG/PDF
    console.log('Download chart functionality would be implemented here');
  };

  return (
    <div className="space-y-4">
      {/* Chart Controls */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div className="flex flex-wrap gap-2">
          {Object.entries(bandConfig).map(([band, config]) => (
            <motion.button
              key={band}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => toggleBandVisibility(band)}
              className={`flex items-center space-x-2 px-3 py-1.5 rounded-full text-xs font-medium border transition-all ${
                visibleBands[band]
                  ? `bg-opacity-20 border-current text-current`
                  : 'bg-slate-100 dark:bg-slate-700 text-slate-500 dark:text-slate-400 border-slate-200 dark:border-slate-600'
              }`}
              style={{
                color: visibleBands[band] ? config.color : undefined,
                backgroundColor: visibleBands[band] ? config.bgColor : undefined,
              }}
            >
              {visibleBands[band] ? <Eye className="w-3 h-3" /> : <EyeOff className="w-3 h-3" />}
              <span>{config.label}</span>
            </motion.button>
          ))}
        </div>

        <div className="flex items-center space-x-2">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setShowAsArea(!showAsArea)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              showAsArea
                ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300'
                : 'bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-400'
            }`}
          >
            {showAsArea ? 'Line View' : 'Area View'}
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={downloadChart}
            className="p-1.5 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors"
            title="Download Chart"
          >
            <Download className="w-4 h-4" />
          </motion.button>
        </div>
      </div>

      {/* Chart Container */}
      <div className="relative h-96 bg-white dark:bg-slate-900 rounded-lg p-4 border border-slate-200 dark:border-slate-700">
        <Line data={chartJsData} options={options} />
      </div>

      {/* Band Information */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
        {Object.entries(bandConfig).map(([band, config]) => {
          const currentValue = chartData.bands_timeseries?.[band]?.[selectedEpoch] || 0;
          const isVisible = visibleBands[band];

          return (
            <motion.div
              key={band}
              whileHover={{ scale: isVisible ? 1.02 : 1 }}
              className={`p-3 rounded-lg border transition-all ${
                isVisible
                  ? 'border-current bg-opacity-10'
                  : 'border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800'
              }`}
              style={{
                borderColor: isVisible ? config.color : undefined,
                backgroundColor: isVisible ? config.bgColor : undefined,
              }}
            >
              <div className="flex items-center space-x-2 mb-1">
                <div
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: config.color }}
                />
                <span className="font-medium text-sm text-slate-800 dark:text-white">
                  {band.charAt(0).toUpperCase() + band.slice(1)}
                </span>
              </div>
              <p className="text-xs text-slate-600 dark:text-slate-400 mb-2">
                {config.description}
              </p>
              <p className="text-lg font-bold text-slate-900 dark:text-white">
                {currentValue.toFixed(1)}
                <span className="text-xs text-slate-500 dark:text-slate-500 ml-1">μV²</span>
              </p>
            </motion.div>
          );
        })}
      </div>

      {/* Analysis Summary */}
      <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
        <h3 className="font-medium text-blue-800 dark:text-blue-200 mb-2">
          Current Time Window Analysis
        </h3>
        <p className="text-sm text-blue-700 dark:text-blue-300">
          Showing data for epoch {selectedEpoch + 1} of {chartData.times?.length || 0} • 
          Time: {chartData.times?.[selectedEpoch]?.toFixed(1) || 0}s
        </p>
        <div className="mt-2 text-xs text-blue-600 dark:text-blue-400">
          <strong>Dominant band:</strong> {
            Object.entries(chartData.bands_timeseries || {})
              .filter(([band]) => visibleBands[band])
              .reduce((max, [band, values]) => 
                (values[selectedEpoch] || 0) > (chartData.bands_timeseries[max]?.[selectedEpoch] || 0) 
                  ? band : max, 
                'alpha'
              ).charAt(0).toUpperCase() + 
            Object.entries(chartData.bands_timeseries || {})
              .filter(([band]) => visibleBands[band])
              .reduce((max, [band, values]) => 
                (values[selectedEpoch] || 0) > (chartData.bands_timeseries[max]?.[selectedEpoch] || 0) 
                  ? band : max, 
                'alpha'
              ).slice(1)
          } ({
            Math.max(...Object.entries(chartData.bands_timeseries || {})
              .filter(([band]) => visibleBands[band])
              .map(([, values]) => values[selectedEpoch] || 0)
            ).toFixed(1)
          } μV²)
        </div>
      </div>
    </div>
  );
};

export default BandChart;