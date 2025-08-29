import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Calendar, 
  TrendingUp, 
  Clock, 
  Activity,
  AlertTriangle,
  CheckCircle,
  ArrowRight
} from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { useAPIQuery } from '../hooks/useAPI';
import StateCard from '../components/dashboard/StateCard';
import QuickActions from '../components/dashboard/QuickActions';
import LoadingSpinner from '../components/common/LoadingSpinner';
import { formatDate, formatRelativeTime } from '../utils/helpers';

const Dashboard = () => {
  const { user } = useAuth();
  const [timeOfDay, setTimeOfDay] = useState('');

  useEffect(() => {
    const hour = new Date().getHours();
    if (hour < 12) setTimeOfDay('morning');
    else if (hour < 17) setTimeOfDay('afternoon');
    else setTimeOfDay('evening');
  }, []);

  const { data: recentSessions, isLoading: sessionsLoading } = useAPIQuery(
    ['recent-sessions'],
    async () => {
      // Mock data for now - would come from API
      return [
        {
          id: '1',
          type: 'eeg',
          state: 'STABLE',
          confidence: 0.87,
          createdAt: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
          emotions: { primary: 'calm', secondary: 'focused' },
        },
        {
          id: '2',
          type: 'text',
          state: 'MILD',
          confidence: 0.73,
          createdAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000), // 1 day ago
          emotions: { primary: 'stressed', secondary: 'tired' },
        },
      ];
    }
  );

  const { data: weeklyStats } = useAPIQuery(
    ['weekly-stats'],
    async () => {
      // Mock data - would come from API
      return {
        sessionsThisWeek: 5,
        avgConfidence: 0.82,
        dominantEmotion: 'calm',
        improvementTrend: 12, // percentage
      };
    }
  );

  const mockRecommendations = [
    {
      title: '5-Minute Morning Breathing',
      description: 'Start your day with calming breathwork',
      duration: 5,
      completed: false,
    },
    {
      title: 'Gratitude Journaling',
      description: 'Write down 3 things you\'re grateful for',
      duration: 8,
      completed: true,
    },
    {
      title: 'Evening Meditation',
      description: 'Wind down with guided mindfulness',
      duration: 15,
      completed: false,
    },
  ];

  const handleSaveSession = (sessionId) => {
    console.log('Saving session:', sessionId);
    // Implementation would call API
  };

  const handleScheduleFollowup = () => {
    console.log('Scheduling follow-up');
    // Implementation would open scheduler
  };

  const handleShare = (sessionId) => {
    console.log('Sharing session:', sessionId);
    // Implementation would generate shareable report
  };

  if (sessionsLoading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <LoadingSpinner size="large" message="Loading your dashboard..." />
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Welcome Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="bg-gradient-to-r from-primary-500 to-blue-600 rounded-2xl text-white p-6"
      >
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl lg:text-3xl font-bold mb-2">
              Good {timeOfDay}, {user?.display_name || 'there'}!
            </h1>
            <p className="text-primary-100 text-lg">
              {recentSessions?.length > 0 
                ? `Your last analysis was ${formatRelativeTime(recentSessions[0].createdAt)}`
                : 'Ready to start your mental health journey?'
              }
            </p>
          </div>
          <div className="hidden lg:block">
            <Activity className="h-16 w-16 text-primary-200" />
          </div>
        </div>
      </motion.div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - State & Actions */}
        <div className="lg:col-span-2 space-y-6">
          {/* Current State */}
          {recentSessions?.[0] && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
            >
              <StateCard
                state={recentSessions[0].state}
                confidence={recentSessions[0].confidence}
                lastUpdated={recentSessions[0].createdAt}
                recommendations={mockRecommendations.slice(0, 2)}
                onSaveSession={() => handleSaveSession(recentSessions[0].id)}
                onScheduleFollowup={handleScheduleFollowup}
                onShare={() => handleShare(recentSessions[0].id)}
              />
            </motion.div>
          )}

          {/* Quick Actions */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <QuickActions />
          </motion.div>
        </div>

        {/* Right Column - Stats & Recommendations */}
        <div className="space-y-6">
          {/* Weekly Stats */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="bg-white rounded-xl shadow-lg p-6 border border-gray-200"
          >
            <div className="flex items-center space-x-3 mb-4">
              <div className="p-2 bg-success-100 rounded-lg">
                <TrendingUp className="h-5 w-5 text-success-600" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900">This Week</h3>
                <p className="text-sm text-gray-500">Your mental health snapshot</p>
              </div>
            </div>

            {weeklyStats && (
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Sessions completed</span>
                  <span className="text-lg font-bold text-gray-900">{weeklyStats.sessionsThisWeek}</span>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Avg. confidence</span>
                  <span className="text-lg font-bold text-success-600">
                    {Math.round(weeklyStats.avgConfidence * 100)}%
                  </span>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Dominant mood</span>
                  <span className="text-lg font-bold text-primary-600 capitalize">
                    {weeklyStats.dominantEmotion}
                  </span>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Improvement</span>
                  <span className="text-lg font-bold text-success-600">
                    +{weeklyStats.improvementTrend}%
                  </span>
                </div>
              </div>
            )}
          </motion.div>

          {/* Today's Recommendations */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="bg-white rounded-xl shadow-lg p-6 border border-gray-200"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-warning-100 rounded-lg">
                  <Calendar className="h-5 w-5 text-warning-600" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">Today's Plan</h3>
                  <p className="text-sm text-gray-500">Personalized wellness activities</p>
                </div>
              </div>
              <span className="text-sm text-gray-500">
                {mockRecommendations.filter(r => r.completed).length}/{mockRecommendations.length} complete
              </span>
            </div>

            <div className="space-y-3">
              {mockRecommendations.map((rec, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    {rec.completed ? (
                      <CheckCircle className="h-5 w-5 text-success-600" />
                    ) : (
                      <div className="w-5 h-5 border-2 border-gray-300 rounded-full"></div>
                    )}
                    <div>
                      <span className={`text-sm font-medium ${rec.completed ? 'text-gray-500 line-through' : 'text-gray-900'}`}>
                        {rec.title}
                      </span>
                      <p className="text-xs text-gray-500">{rec.description}</p>
                    </div>
                  </div>
                  <div className="text-xs text-gray-500 flex items-center space-x-1">
                    <Clock className="h-3 w-3" />
                    <span>{rec.duration}m</span>
                  </div>
                </div>
              ))}
            </div>

            <button className="w-full mt-4 text-primary-600 hover:text-primary-700 text-sm font-medium flex items-center justify-center space-x-1">
              <span>View full plan</span>
              <ArrowRight className="h-4 w-4" />
            </button>
          </motion.div>

          {/* Recent Activity */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.5 }}
            className="bg-white rounded-xl shadow-lg p-6 border border-gray-200"
          >
            <div className="flex items-center space-x-3 mb-4">
              <div className="p-2 bg-gray-100 rounded-lg">
                <Clock className="h-5 w-5 text-gray-600" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Recent Activity</h3>
                <p className="text-sm text-gray-500">Your latest sessions</p>
              </div>
            </div>

            <div className="space-y-3">
              {recentSessions?.map((session, index) => (
                <div key={session.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className={`w-3 h-3 rounded-full ${
                      session.state === 'STABLE' ? 'bg-success-500' :
                      session.state === 'MILD' ? 'bg-warning-500' : 'bg-error-500'
                    }`}></div>
                    <div>
                      <span className="text-sm font-medium text-gray-900 capitalize">
                        {session.type} Analysis
                      </span>
                      <p className="text-xs text-gray-500">
                        {session.emotions.primary} • {Math.round(session.confidence * 100)}% confidence
                      </p>
                    </div>
                  </div>
                  <span className="text-xs text-gray-500">
                    {formatRelativeTime(session.createdAt)}
                  </span>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>

      {/* Safety Notice */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.6 }}
        className="bg-warning-50 border border-warning-200 rounded-lg p-4"
      >
        <div className="flex items-start space-x-3">
          <AlertTriangle className="h-5 w-5 text-warning-600 flex-shrink-0 mt-0.5" />
          <div className="text-sm text-warning-700">
            <p className="font-medium mb-1">Medical Disclaimer</p>
            <p>
              This platform provides supportive insights based on AI analysis and should not replace professional medical advice. 
              If you're experiencing mental health concerns, please consult with a qualified healthcare provider.
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Dashboard;