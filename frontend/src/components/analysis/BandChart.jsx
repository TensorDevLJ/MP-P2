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
  TimeScale,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import 'chartjs-adapter-date-fns';
import { EEG_BANDS } from '../../utils/constants';
import { Eye, EyeOff, ZoomIn, ZoomOut, RotateCcw } from 'lucide-react';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  TimeScale
);

const BandChart = ({ bandsTimeSeries, times, title = "EEG Band Powers Over Time" }) => {
  const [visibleBands, setVisibleBands] = useState({
    delta: true,
    theta: true,
    alpha: true,
    beta: true,
    gamma: true,
  });
  
  const [zoomLevel, setZoomLevel] = useState(1);

  const toggleBand = (band) => {
    setVisibleBands(prev => ({
      ...prev,
      [band]: !prev[band],
    }));
  };

  const data = useMemo(() => {
    const datasets = [];
    
    Object.entries(EEG_BANDS).forEach(([band, config]) => {
      if (visibleBands[band] && bandsTimeSeries[band]) {
        datasets.push({
          label: `${config.name} (${config.range})`,
          data: times.map((time, index) => ({
            x: new Date(time),
            y: bandsTimeSeries[band][index],
          })),
          borderColor: config.color,
          backgroundColor: `${config.color}20`,
          fill: false,
          tension: 0.3,
          pointRadius: 2,
          pointHoverRadius: 6,
          borderWidth: 2,
        });
      }
    });

    return { datasets };
  }, [bandsTimeSeries, times, visibleBands]);

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    plugins: {
      legend: {
        display: false, // We have custom legend
      },
      tooltip: {
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        titleColor: '#1f2937',
        bodyColor: '#374151',
        borderColor: '#d1d5db',
        borderWidth: 1,
        cornerRadius: 8,
        titleFont: {
          weight: 'bold',
        },
        callbacks: {
          title: (context) => {
            return new Date(context[0].parsed.x).toLocaleTimeString();
          },
          label: (context) => {
            return `${context.dataset.label}: ${context.parsed.y.toFixed(3)} μV²`;
          },
        },
      },
    },
    scales: {
      x: {
        type: 'time',
        time: {
          displayFormats: {
            second: 'HH:mm:ss',
            minute: 'HH:mm',
          },
        },
        title: {
          display: true,
          text: 'Time',
          font: {
            weight: 'bold',
          },
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        },
      },
      y: {
        title: {
          display: true,
          text: 'Power (μV²)',
          font: {
            weight: 'bold',
          },
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        },
        beginAtZero: true,
      },
    },
    animation: {
      duration: 1000,
      easing: 'easeInOutCubic',
    },
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          <p className="text-sm text-gray-500">Interactive frequency band analysis</p>
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
        </div>
      </div>

      {/* Band Toggle Legend */}
      <div className="flex flex-wrap gap-2 mb-6">
        {Object.entries(EEG_BANDS).map(([band, config]) => (
          <button
            key={band}
            onClick={() => toggleBand(band)}
            className={`flex items-center space-x-2 px-3 py-2 rounded-lg border transition-all ${
              visibleBands[band]
                ? 'border-gray-300 bg-white shadow-sm'
                : 'border-gray-200 bg-gray-50 opacity-60'
            }`}
          >
            {visibleBands[band] ? (
              <Eye className="h-4 w-4 text-gray-600" />
            ) : (
              <EyeOff className="h-4 w-4 text-gray-400" />
            )}
            <div
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: config.color }}
            />
            <span className={`text-sm font-medium ${
              visibleBands[band] ? 'text-gray-900' : 'text-gray-500'
            }`}>
              {config.name}
            </span>
            <span className="text-xs text-gray-500">{config.range}</span>
          </button>
        ))}
      </div>

      {/* Chart */}
      <div className="h-80 mb-4">
        <Line data={data} options={options} />
      </div>

      <div className="text-xs text-gray-500 text-center">
        Click legend items to show/hide bands • Hover over chart for detailed values
      </div>
    </div>
  );
};

export default BandChart;