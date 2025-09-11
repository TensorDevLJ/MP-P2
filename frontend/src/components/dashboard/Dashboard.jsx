import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { 
  Brain, 
  FileText, 
  MessageCircle, 
  TrendingUp,
  ArrowRight,
  CheckCircle,
  AlertTriangle
} from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';
import { ROUTES } from '../../utils/constants';

const Dashboard = () => {
  const { user } = useAuth();
  const [timeOfDay, setTimeOfDay] = useState('');

  useEffect(() => {
    const hour = new Date().getHours();
    if (hour < 12) setTimeOfDay('morning');
    else if (hour < 17) setTimeOfDay('afternoon');
    else setTimeOfDay('evening');
  }, []);

  const quickActions = [
    {
      title: 'Analyze Your Feelings',
      description: 'Share your thoughts for AI-powered mental health insights',
      icon: FileText,
      href: ROUTES.ANALYZE,
      color: 'primary',
    },
    {
      title: 'Chat with AI Assistant',
      description: 'Get support and guidance from our mental health bot',
      icon: MessageCircle,
      href: ROUTES.ASSISTANT,
      color: 'success',
    },
  ];

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Welcome Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-r from-primary-500 to-blue-600 rounded-2xl text-white p-8"
      >
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold mb-2">
              Good {timeOfDay}, {user?.display_name || 'there'}!
            </h1>
            <p className="text-primary-100 text-lg">
              Ready to check in on your mental health today?
            </p>
          </div>
          <Brain className="h-16 w-16 text-primary-200" />
        </div>
      </motion.div>

      {/* Quick Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="grid grid-cols-1 md:grid-cols-2 gap-6"
      >
        {quickActions.map((action) => {
          const Icon = action.icon;
          return (
            <Link
              key={action.title}
              to={action.href}
              className={`group p-6 rounded-xl text-white transition-all duration-300 bg-${action.color}-600 hover:bg-${action.color}-700 hover:shadow-lg transform hover:scale-105`}
            >
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 bg-white bg-opacity-20 rounded-lg">
                  <Icon className="h-6 w-6" />
                </div>
                <ArrowRight className="h-5 w-5 opacity-70 group-hover:opacity-100 group-hover:translate-x-1 transition-all" />
              </div>
              
              <h3 className="text-lg font-semibold mb-2">{action.title}</h3>
              <p className="text-sm opacity-90">{action.description}</p>
            </Link>
          );
        })}
      </motion.div>

      {/* Features Overview */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-white rounded-xl shadow-lg p-6 border border-gray-200"
      >
        <h2 className="text-xl font-bold text-gray-900 mb-6">How It Works</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <FileText className="h-6 w-6 text-primary-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Share Your Thoughts</h3>
            <p className="text-sm text-gray-600">Write about how you're feeling or what's on your mind</p>
          </div>
          
          <div className="text-center">
            <div className="w-12 h-12 bg-success-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <Brain className="h-6 w-6 text-success-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">AI Analysis</h3>
            <p className="text-sm text-gray-600">Our AI analyzes your text for depression indicators</p>
          </div>
          
          <div className="text-center">
            <div className="w-12 h-12 bg-warning-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <CheckCircle className="h-6 w-6 text-warning-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Get Support</h3>
            <p className="text-sm text-gray-600">Receive personalized recommendations and guidance</p>
          </div>
        </div>
      </motion.div>

      {/* Safety Notice */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
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
      </div>
    </div>
  );
};

export default Dashboard;