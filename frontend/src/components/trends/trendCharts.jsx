import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  TimeScale,
} from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';
import 'chartjs-adapter-date-fns';
import { Calendar, TrendingUp, BarChart3, Clock } from 'lucide-react';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  TimeScale
);

const TrendCharts = ({ timeframe = '30d' }) => {
  const [selectedMetric, setSelectedMetric] = useState('confidence');
  const [chartType, setChartType] = useState('line');

  // Mock trend data
  const generateMockData = (days) => {
    const now = new Date();
    const data = [];
    
    for (let i = days - 1; i >= 0; i--) {
      const date = new Date(now.getTime() - i * 24 * 60 * 60 * 1000);
      data.push({
        date: date.toISOString(),
        confidence: 0.7 + Math.random() * 0.25,
        stableCount: Math.floor(Math.random() * 3),
        mildCount: Math.floor(Math.random() * 2),
        moderateCount: Math.floor(Math.random() * 1),
        alphaPower: 0.6 + Math.random() * 0.3,
        betaPower: 0.4 + Math.random() * 0.3,
        anxiety: Math.random() * 0.5,
        stress: Math.random() * 0.6,
      });
    }
    return data;
  };

  const trendData = generateMockData(timeframe === '7d' ? 7 : timeframe === '30d' ? 30 : 90);

  const metrics = {
    confidence: {
      label: 'Analysis Confidence',
      key: 'confidence',
      color: '#3B82F6',
      format: (value) => `${Math.round(value * 100)}%`,
    },
    alpha: {
      label: 'Alpha Power',
      key: 'alphaPower',
      color: '#10B981',
      format: (value) => value.toFixed(2),
    },
    beta: {
      label: 'Beta Power',
      key: 'betaPower',
      color: '#F59E0B',
      format: (value) => value.toFixed(2),
    },
    anxiety: {
      label: 'Anxiety Level',
      key: 'anxiety',
      color: '#EF4444',
      format: (value) => `${Math.round(value * 100)}%`,
    },
  };

  const selectedMetricData = metrics[selectedMetric];

  const chartData = {
    labels: trendData.map(d => new Date(d.date)),
    datasets: [
      {
        label: selectedMetricData.label,
        data: trendData.map(d => d[selectedMetricData.key]),
        borderColor: selectedMetricData.color,
        backgroundColor: `${selectedMetricData.color}20`,
        fill: chartType === 'line',
        tension: 0.3,
        pointRadius: 3,
        pointHoverRadius: 6,
        borderWidth: 2,
      },
    ],
  };

  const options = {
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
          title: (context) => {
            return new Date(context[0].parsed.x).toLocaleDateString();
          },
          label: (context) => {
            return `${selectedMetricData.label}: ${selectedMetricData.format(context.parsed.y)}`;
          },
        },
      },
    },
    scales: {
      x: {
        type: 'time',
        time: {
          displayFormats: {
            day: 'MMM dd',
            week: 'MMM dd',
          },
        },
        title: {
          display: true,
          text: 'Date',
          font: { weight: 'bold' },
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        },
      },
      y: {
        title: {
          display: true,
          text: selectedMetricData.label,
          font: { weight: 'bold' },
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        },
        beginAtZero: selectedMetric === 'anxiety',
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
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-primary-100 rounded-lg">
            <TrendingUp className="h-5 w-5 text-primary-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Trend Analysis</h3>
            <p className="text-sm text-gray-500">Your mental health patterns over time</p>
          </div>
        </div>
        
        <div className="flex items-center space-x-3">
          {/* Chart Type Toggle */}
          <div className="flex bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => setChartType('line')}
              className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                chartType === 'line'
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Line
            </button>
            <button
              onClick={() => setChartType('bar')}
              className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                chartType === 'bar'
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Bar
            </button>
          </div>
        </div>
      </div>

      {/* Metric Selection */}
      <div className="flex flex-wrap gap-2 mb-6">
        {Object.entries(metrics).map(([key, metric]) => (
          <button
            key={key}
            onClick={() => setSelectedMetric(key)}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              selectedMetric === key
                ? 'bg-primary-100 text-primary-700 border-primary-200'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            } border`}
          >
            {metric.label}
          </button>
        ))}
      </div>

      {/* Chart */}
      <motion.div
        key={selectedMetric + chartType}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
        className="h-80 mb-4"
      >
        {chartType === 'line' ? (
          <Line data={chartData} options={options} />
        ) : (
          <Bar data={chartData} options={options} />
        )}
      </motion.div>

      {/* Stats Summary */}
      <div className="grid grid-cols-3 gap-4 pt-4 border-t border-gray-200">
        <div className="text-center">
          <p className="text-2xl font-bold text-success-600">
            {Math.round(trendData[trendData.length - 1]?.[selectedMetricData.key] * 100) || 85}
          </p>
          <p className="text-sm text-gray-500">Current</p>
        </div>
        
        <div className="text-center">
          <p className="text-2xl font-bold text-primary-600">
            {Math.round(trendData.reduce((acc, d) => acc + d[selectedMetricData.key], 0) / trendData.length * 100) || 78}
          </p>
          <p className="text-sm text-gray-500">Average</p>
        </div>
        
        <div className="text-center">
          <p className="text-2xl font-bold text-warning-600">
            {trendData.length}
          </p>
          <p className="text-sm text-gray-500">Data Points</p>
        </div>
      </div>
    </div>
  );
};

export default TrendCharts;