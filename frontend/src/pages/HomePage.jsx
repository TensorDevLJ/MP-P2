// frontend/src/pages/HomePage.jsx
import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { 
  Brain, 
  Heart, 
  TrendingUp, 
  Calendar,
  AlertTriangle,
  CheckCircle,
  Clock,
  Users
} from 'lucide-react';

import StateCard from '../components/dashboard/StateCard';
import QuickActions from '../components/dashboard/QuickActions';
import RecentAnalysis from '../components/dashboard/RecentAnalysis';
import TrendChart from '../components/trends/TrendChart';
import { api } from '../services/api';

const HomePage = () => {
  // Fetch dashboard data
  const { data: dashboardData, isLoading } = useQuery({
    queryKey: ['dashboard'],
    queryFn: () => api.get('/dashboard/summary'),
  });

  const { data: recentSessions } = useQuery({
    queryKey: ['recent-sessions'],
    queryFn: () => api.get('/sessions/recent?limit=5'),
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  const currentState = dashboardData?.current_state || {};
  const stats = dashboardData?.stats || {};

  return (
    <div className="space-y-6">
      {/* Welcome Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg p-6">
        <h1 className="text-3xl font-bold mb-2">Welcome to Your Mental Health Dashboard</h1>
        <p className="text-indigo-100">
          Track your mental wellness journey with AI-powered insights from EEG data and self-assessments.
        </p>
      </div>

      {/* Current State Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StateCard
          title="Current State"
          value={currentState.risk_level || 'No data'}
          icon={Brain}
          color={getStateColor(currentState.risk_level)}
          subtitle={`${Math.round(currentState.confidence * 100)}% confidence`}
        />
        <StateCard
          title="Mood Trend"
          value={stats.mood_trend || 'Stable'}
          icon={TrendingUp}
          color="blue"
          subtitle="Last 7 days"
        />
        <StateCard
          title="Total Sessions"
          value={stats.total_sessions || 0}
          icon={Calendar}
          color="green"
          subtitle="All time"
        />
        <StateCard
          title="Last Analysis"
          value={formatTimeAgo(stats.last_analysis)}
          icon={Clock}
          color="purple"
          subtitle="Days ago"
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Quick Actions */}
        <div className="lg:col-span-1">
          <QuickActions />
        </div>

        {/* Middle Column - Trend Chart */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <TrendingUp className="w-5 h-5 mr-2 text-indigo-500" />
              Mental State Trends
            </h2>
            <TrendChart data={dashboardData?.trend_data || []} />
          </div>
        </div>
      </div>

      {/* Recent Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <RecentAnalysis sessions={recentSessions?.data || []} />
        
        {/* Recommendations */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <Heart className="w-5 h-5 mr-2 text-red-500" />
            Today's Recommendations
          </h2>
          <div className="space-y-4">
            {currentState.recommendations?.map((rec, index) => (
              <div key={index} className="flex items-start space-x-3 p-3 bg-blue-50 rounded-lg">
                <CheckCircle className="w-5 h-5 text-blue-500 mt-0.5" />
                <div>
                  <p className="text-sm font-medium text-blue-900">{rec.title}</p>
                  <p className="text-xs text-blue-700">{rec.description}</p>
                </div>
              </div>
            )) || (
              <p className="text-gray-500">Complete an analysis to get personalized recommendations.</p>
            )}
          </div>
        </div>
      </div>

      {/* Safety Notice */}
      {currentState.risk_level === 'high' && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded-lg">
          <div className="flex items-center">
            <AlertTriangle className="w-5 h-5 text-red-400 mr-3" />
            <div>
              <h3 className="text-sm font-medium text-red-800">Important Notice</h3>
              <p className="text-sm text-red-700 mt-1">
                Our analysis indicates elevated risk factors. Please consider speaking with a mental health professional.
              </p>
              <div className="mt-3">
                <button 
                  onClick={() => window.location.href = '/care'}
                  className="bg-red-600 text-white px-4 py-2 rounded-md text-sm hover:bg-red-700 transition-colors"
                >
                  Find Professional Help
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Helper functions
function getStateColor(riskLevel) {
  const colors = {
    'stable': 'green',
    'mild': 'yellow',
    'moderate': 'orange',
    'high': 'red'
  };
  return colors[riskLevel] || 'gray';
}

function formatTimeAgo(timestamp) {
  if (!timestamp) return 'Never';
  const days = Math.floor((new Date() - new Date(timestamp)) / (1000 * 60 * 60 * 24));
  return days === 0 ? 'Today' : `${days}`;
}

export default HomePage;