import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import {
  Activity,
  MessageCircle,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Calendar,
  Clock,
  Brain,
  Heart,
  Zap,
  Plus,
} from 'lucide-react';
import StateCard from '../components/dashboard/StateCard';
import QuickActions from '../components/dashboard/QuickActions';
import RecentAnalysis from '../components/dashboard/RecentAnalysis';
import WellnessScore from '../components/dashboard/WellnessScore';

const HomePage = () => {
  const [currentState] = useState({
    overall: 'moderate',
    confidence: 0.78,
    lastAnalysis: '2 hours ago',
    trend: 'improving',
  });

  const [todayStats] = useState({
    analyses: 3,
    chatSessions: 2,
    recommendationsCompleted: 5,
    moodScore: 7.2,
  });

  const [upcomingReminders] = useState([
    {
      id: 1,
      title: 'Evening Meditation',
      time: '8:00 PM',
      type: 'mindfulness',
      completed: false,
    },
    {
      id: 2,
      title: 'Mood Check-in',
      time: '9:00 PM',
      type: 'assessment',
      completed: false,
    },
    {
      id: 3,
      title: 'Sleep Routine',
      time: '10:30 PM',
      type: 'sleep',
      completed: false,
    },
  ]);

  const [recentInsights] = useState([
    {
      id: 1,
      title: 'Alpha waves showing improvement',
      description: 'Your relaxation patterns have increased by 15% this week',
      type: 'positive',
      timestamp: '1 hour ago',
    },
    {
      id: 2,
      title: 'Stress indicators elevated',
      description: 'Beta activity suggests increased cognitive load',
      type: 'warning',
      timestamp: '3 hours ago',
    },
    {
      id: 3,
      title: 'Sleep quality impact',
      description: 'Your EEG patterns show better rest quality',
      type: 'positive',
      timestamp: '1 day ago',
    },
  ]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="p-6 space-y-6"
    >
      {/* Welcome Header */}
      <div className="mb-8">
        <motion.h1
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="text-3xl font-bold text-slate-800 dark:text-white mb-2"
        >
          Welcome back! 👋
        </motion.h1>
        <motion.p
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.1 }}
          className="text-slate-600 dark:text-slate-400"
        >
          Here's your mental wellness overview for today
        </motion.p>
      </div>

      {/* Main Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 rounded-xl p-6 border border-blue-200 dark:border-blue-800"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-blue-600 dark:text-blue-400 text-sm font-medium">
                Analyses Today
              </p>
              <p className="text-2xl font-bold text-blue-700 dark:text-blue-300">
                {todayStats.analyses}
              </p>
            </div>
            <Activity className="w-8 h-8 text-blue-500" />
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 rounded-xl p-6 border border-green-200 dark:border-green-800"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-600 dark:text-green-400 text-sm font-medium">
                Mood Score
              </p>
              <p className="text-2xl font-bold text-green-700 dark:text-green-300">
                {todayStats.moodScore}/10
              </p>
            </div>
            <Heart className="w-8 h-8 text-green-500" />
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/20 rounded-xl p-6 border border-purple-200 dark:border-purple-800"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-purple-600 dark:text-purple-400 text-sm font-medium">
                Chat Sessions
              </p>
              <p className="text-2xl font-bold text-purple-700 dark:text-purple-300">
                {todayStats.chatSessions}
              </p>
            </div>
            <MessageCircle className="w-8 h-8 text-purple-500" />
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-gradient-to-br from-orange-50 to-orange-100 dark:from-orange-900/20 dark:to-orange-800/20 rounded-xl p-6 border border-orange-200 dark:border-orange-800"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-orange-600 dark:text-orange-400 text-sm font-medium">
                Completed Tasks
              </p>
              <p className="text-2xl font-bold text-orange-700 dark:text-orange-300">
                {todayStats.recommendationsCompleted}
              </p>
            </div>
            <CheckCircle className="w-8 h-8 text-orange-500" />
          </div>
        </motion.div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column */}
        <div className="lg:col-span-2 space-y-6">
          {/* Current State */}
          <StateCard currentState={currentState} />

          {/* Quick Actions */}
          <QuickActions />

          {/* Recent Insights */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="bg-white dark:bg-slate-800 rounded-xl p-6 shadow-sm border border-slate-200 dark:border-slate-700"
          >
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-slate-800 dark:text-white">
                Recent Insights
              </h2>
              <Link
                to="/trends"
                className="text-blue-600 dark:text-blue-400 hover:underline text-sm"
              >
                View all
              </Link>
            </div>

            <div className="space-y-4">
              {recentInsights.map((insight) => (
                <motion.div
                  key={insight.id}
                  whileHover={{ scale: 1.02 }}
                  className="flex items-start space-x-3 p-4 rounded-lg bg-slate-50 dark:bg-slate-700/50"
                >
                  <div className={`w-2 h-2 rounded-full mt-2 ${
                    insight.type === 'positive' ? 'bg-green-500' : 'bg-yellow-500'
                  }`} />
                  <div className="flex-1">
                    <p className="font-medium text-slate-800 dark:text-white">
                      {insight.title}
                    </p>
                    <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
                      {insight.description}
                    </p>
                    <p className="text-xs text-slate-500 dark:text-slate-500 mt-2">
                      {insight.timestamp}
                    </p>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Right Column */}
        <div className="space-y-6">
          {/* Wellness Score */}
          <WellnessScore score={todayStats.moodScore} />

          {/* Today's Reminders */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="bg-white dark:bg-slate-800 rounded-xl p-6 shadow-sm border border-slate-200 dark:border-slate-700"
          >
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-slate-800 dark:text-white">
                Today's Schedule
              </h2>
              <Calendar className="w-5 h-5 text-slate-500" />
            </div>

            <div className="space-y-3">
              {upcomingReminders.map((reminder) => (
                <motion.div
                  key={reminder.id}
                  whileHover={{ scale: 1.02 }}
                  className={`flex items-center space-x-3 p-3 rounded-lg ${
                    reminder.completed
                      ? 'bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800'
                      : 'bg-slate-50 dark:bg-slate-700/50 border border-slate-200 dark:border-slate-600'
                  }`}
                >
                  <div className={`w-3 h-3 rounded-full ${
                    reminder.completed ? 'bg-green-500' : 'bg-slate-400'
                  }`} />
                  <div className="flex-1">
                    <p className={`font-medium ${
                      reminder.completed
                        ? 'text-green-700 dark:text-green-300 line-through'
                        : 'text-slate-800 dark:text-white'
                    }`}>
                      {reminder.title}
                    </p>
                    <div className="flex items-center space-x-1 mt-1">
                      <Clock className="w-3 h-3 text-slate-500" />
                      <span className="text-xs text-slate-500">
                        {reminder.time}
                      </span>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>

            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="w-full mt-4 p-3 border-2 border-dashed border-slate-300 dark:border-slate-600 rounded-lg text-slate-500 dark:text-slate-400 hover:border-blue-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors flex items-center justify-center space-x-2"
            >
              <Plus className="w-4 h-4" />
              <span>Add reminder</span>
            </motion.button>
          </motion.div>

          {/* Emergency Resources */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7 }}
            className="bg-gradient-to-br from-red-50 to-pink-50 dark:from-red-900/20 dark:to-pink-900/20 rounded-xl p-6 border border-red-200 dark:border-red-800"
          >
            <div className="flex items-center space-x-2 mb-3">
              <AlertTriangle className="w-5 h-5 text-red-600 dark:text-red-400" />
              <h3 className="font-semibold text-red-700 dark:text-red-300">
                Need immediate help?
              </h3>
            </div>
            <p className="text-sm text-red-600 dark:text-red-400 mb-4">
              If you're experiencing a mental health crisis, please reach out immediately.
            </p>
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="w-full bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-lg font-medium transition-colors"
            >
              Emergency Resources
            </motion.button>
          </motion.div>
        </div>
      </div>
    </motion.div>
  );
};

export default HomePage;