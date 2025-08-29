import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Calendar, 
  Target, 
  Award, 
  TrendingUp,
  CheckCircle,
  Clock,
  Star,
  ArrowRight,
  Brain,
  Heart,
  Flame,
  Trophy
} from 'lucide-react';
import { formatDate } from '../../utils/helpers';

const ProgressTracking = () => {
  const [selectedPeriod, setSelectedPeriod] = useState('month');

  // Mock progress data
  const progressData = {
    goals: [
      {
        id: '1',
        title: 'Daily Meditation',
        target: 30, // days
        current: 23,
        type: 'habit',
        streak: 7,
        completed: false,
      },
      {
        id: '2',
        title: 'Weekly EEG Sessions',
        target: 4, // per month
        current: 3,
        type: 'analysis',
        streak: 0,
        completed: false,
      },
      {
        id: '3',
        title: 'Stress Management',
        target: 80, // percentage improvement
        current: 67,
        type: 'wellness',
        streak: 0,
        completed: false,
      },
    ],
    achievements: [
      {
        id: '1',
        title: 'First Analysis Complete',
        description: 'Completed your first EEG analysis',
        earnedAt: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
        icon: Brain,
        color: 'primary',
      },
      {
        id: '2',
        title: 'Meditation Master',
        description: '7-day meditation streak',
        earnedAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000),
        icon: Star,
        color: 'success',
      },
      {
        id: '3',
        title: 'Progress Tracker',
        description: 'Used the platform for 2 weeks',
        earnedAt: new Date(),
        icon: Award,
        color: 'warning',
      },
    ],
    weeklyStats: {
      analysisCount: 3,
      avgConfidence: 0.82,
      topEmotion: 'calm',
      improvementScore: 12,
    },
  };

  const moodCalendar = Array.from({ length: 30 }, (_, i) => {
    const date = new Date();
    date.setDate(date.getDate() - (29 - i));
    
    const moods = ['stable', 'mild', 'moderate'];
    const mood = moods[Math.floor(Math.random() * moods.length)];
    
    return {
      date,
      mood,
      hasData: Math.random() > 0.3, // 70% chance of having data
    };
  });

  const getMoodColor = (mood) => {
    switch (mood) {
      case 'stable': return 'bg-success-500';
      case 'mild': return 'bg-warning-500';
      case 'moderate': return 'bg-error-500';
      default: return 'bg-gray-200';
    }
  };

  const getAchievementColor = (color) => {
    const colors = {
      primary: 'bg-primary-100 text-primary-600 border-primary-200',
      success: 'bg-success-100 text-success-600 border-success-200',
      warning: 'bg-warning-100 text-warning-600 border-warning-200',
      error: 'bg-error-100 text-error-600 border-error-200',
    };
    return colors[color] || colors.primary;
  };

  return (
    <div className="space-y-6">
      {/* Goals Progress */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="bg-white rounded-xl shadow-lg p-6 border border-gray-200"
      >
        <div className="flex items-center space-x-3 mb-6">
          <div className="p-2 bg-primary-100 rounded-lg">
            <Target className="h-5 w-5 text-primary-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Current Goals</h3>
            <p className="text-sm text-gray-500">Track your wellness objectives</p>
          </div>
        </div>

        <div className="space-y-4">
          {progressData.goals.map((goal) => (
            <div key={goal.id} className="p-4 border border-gray-200 rounded-lg hover:shadow-sm transition-shadow">
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-semibold text-gray-900">{goal.title}</h4>
                <div className="flex items-center space-x-2">
                  {goal.streak > 0 && (
                    <div className="flex items-center space-x-1 bg-warning-100 text-warning-700 px-2 py-1 rounded-full text-xs font-medium">
                      <Flame className="h-3 w-3" />
                      <span>{goal.streak} day streak</span>
                    </div>
                  )}
                  <span className="text-sm font-medium text-gray-700">
                    {goal.current}/{goal.target}
                  </span>
                </div>
              </div>
              
              <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
                <div
                  className="bg-primary-600 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${Math.min((goal.current / goal.target) * 100, 100)}%` }}
                />
              </div>
              
              <div className="flex justify-between text-xs text-gray-500">
                <span className="capitalize">{goal.type} goal</span>
                <span>{Math.round((goal.current / goal.target) * 100)}% complete</span>
              </div>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Mood Calendar */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1 }}
        className="bg-white rounded-xl shadow-lg p-6 border border-gray-200"
      >
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-success-100 rounded-lg">
              <Calendar className="h-5 w-5 text-success-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Mood Calendar</h3>
              <p className="text-sm text-gray-500">Last 30 days overview</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2 text-sm">
            <div className="flex items-center space-x-1">
              <div className="w-3 h-3 bg-success-500 rounded-full"></div>
              <span>Stable</span>
            </div>
            <div className="flex items-center space-x-1">
              <div className="w-3 h-3 bg-warning-500 rounded-full"></div>
              <span>Mild</span>
            </div>
            <div className="flex items-center space-x-1">
              <div className="w-3 h-3 bg-error-500 rounded-full"></div>
              <span>Moderate</span>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-7 gap-2">
          {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day) => (
            <div key={day} className="text-center text-xs font-medium text-gray-500 py-2">
              {day}
            </div>
          ))}
          
          {moodCalendar.map((day, index) => (
            <div
              key={index}
              className={`aspect-square rounded-lg border-2 flex items-center justify-center text-xs font-medium transition-all hover:scale-110 cursor-pointer ${
                day.hasData 
                  ? `${getMoodColor(day.mood)} text-white border-transparent shadow-sm` 
                  : 'bg-gray-100 text-gray-400 border-gray-200'
              }`}
              title={day.hasData ? `${formatDate(day.date, 'MMM dd')} - ${day.mood}` : 'No data'}
            >
              {day.date.getDate()}
            </div>
          ))}
        </div>

        <div className="mt-4 text-xs text-gray-500 text-center">
          Click on any day to view detailed mood analysis
        </div>
      </motion.div>

      {/* Achievements */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="bg-white rounded-xl shadow-lg p-6 border border-gray-200"
      >
        <div className="flex items-center space-x-3 mb-6">
          <div className="p-2 bg-warning-100 rounded-lg">
            <Trophy className="h-5 w-5 text-warning-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Achievements</h3>
            <p className="text-sm text-gray-500">Celebrate your wellness milestones</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {progressData.achievements.map((achievement) => {
            const Icon = achievement.icon;
            return (
              <div 
                key={achievement.id}
                className={`p-4 border-2 rounded-lg ${getAchievementColor(achievement.color)} transition-all hover:shadow-md`}
              >
                <div className="flex items-center space-x-3 mb-3">
                  <div className={`p-2 rounded-lg ${getAchievementColor(achievement.color)}`}>
                    <Icon className="h-5 w-5" />
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-sm">{achievement.title}</h4>
                    <p className="text-xs opacity-75">{achievement.description}</p>
                  </div>
                </div>
                <p className="text-xs opacity-60">
                  Earned {formatDate(achievement.earnedAt, 'MMM dd')}
                </p>
              </div>
            );
          })}
        </div>
      </motion.div>

      {/* Weekly Summary */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.3 }}
        className="bg-white rounded-xl shadow-lg p-6 border border-gray-200"
      >
        <div className="flex items-center space-x-3 mb-6">
          <div className="p-2 bg-success-100 rounded-lg">
            <TrendingUp className="h-5 w-5 text-success-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Weekly Summary</h3>
            <p className="text-sm text-gray-500">Your wellness journey this week</p>
          </div>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <Brain className="h-8 w-8 text-primary-600" />
            </div>
            <p className="text-2xl font-bold text-primary-600 mb-1">{progressData.weeklyStats.analysisCount}</p>
            <p className="text-sm text-gray-500">Analyses</p>
          </div>
          
          <div className="text-center">
            <div className="w-16 h-16 bg-success-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <CheckCircle className="h-8 w-8 text-success-600" />
            </div>
            <p className="text-2xl font-bold text-success-600 mb-1">
              {Math.round(progressData.weeklyStats.avgConfidence * 100)}%
            </p>
            <p className="text-sm text-gray-500">Avg Confidence</p>
          </div>
          
          <div className="text-center">
            <div className="w-16 h-16 bg-warning-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <Heart className="h-8 w-8 text-warning-600" />
            </div>
            <p className="text-2xl font-bold text-warning-600 mb-1 capitalize">
              {progressData.weeklyStats.topEmotion}
            </p>
            <p className="text-sm text-gray-500">Top Mood</p>
          </div>
          
          <div className="text-center">
            <div className="w-16 h-16 bg-error-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <TrendingUp className="h-8 w-8 text-error-600" />
            </div>
            <p className="text-2xl font-bold text-error-600 mb-1">
              +{progressData.weeklyStats.improvementScore}%
            </p>
            <p className="text-sm text-gray-500">Improvement</p>
          </div>
        </div>
      </motion.div>

      {/* Personal Insights */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.4 }}
        className="bg-gradient-to-r from-primary-50 to-blue-50 rounded-xl p-6 border border-primary-200"
      >
        <div className="flex items-center space-x-3 mb-4">
          <div className="p-2 bg-primary-600 rounded-lg">
            <Flame className="h-5 w-5 text-white" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Personal Insights</h3>
            <p className="text-sm text-gray-600">AI-powered observations about your progress</p>
          </div>
        </div>

        <div className="bg-white rounded-lg p-4 mb-4">
          <p className="text-gray-700 leading-relaxed">
            Your meditation practice is showing positive effects on your alpha wave patterns. 
            EEG data from the past week indicates improved relaxation states during evening sessions. 
            Consider maintaining this routine as your stress indicators have decreased by 15%.
          </p>
        </div>

        <div className="flex items-center justify-between">
          <div className="text-sm text-gray-600">
            Keep up the excellent work on your wellness journey!
          </div>
          <button className="text-primary-600 hover:text-primary-700 font-medium text-sm flex items-center space-x-1">
            <span>View detailed report</span>
            <ArrowRight className="h-4 w-4" />
          </button>
        </div>
      </motion.div>
    </div>
  );
};

export default ProgressTracking;