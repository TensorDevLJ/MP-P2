import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Brain, 
  MessageCircle, 
  MapPin, 
  TrendingUp, 
  Upload,
  Stethoscope,
  Heart,
  ArrowRight,
  Play,
  BarChart3,
  Users,
  Shield
} from 'lucide-react';
import { ROUTES } from '../../utils/constants';

const QuickActions = () => {
  const primaryActions = [
    {
      title: 'Analyze EEG Data',
      description: 'Upload and analyze your brainwave signals',
      icon: Brain,
      href: ROUTES.ANALYZE,
      color: 'primary',
      highlight: true,
    },
    {
      title: 'Health Assistant',
      description: 'Chat with AI about your mental health',
      icon: MessageCircle,
      href: ROUTES.ASSISTANT,
      color: 'success',
      highlight: true,
    },
    {
      title: 'Find Care Providers',
      description: 'Locate nearby mental health professionals',
      icon: MapPin,
      href: ROUTES.CARE,
      color: 'warning',
      highlight: false,
    },
    {
      title: 'View Progress',
      description: 'Track your mental health journey',
      icon: TrendingUp,
      href: ROUTES.TRENDS,
      color: 'error',
      highlight: false,
    },
  ];

  const secondaryActions = [
    {
      title: 'How to Use',
      description: 'Learn platform features',
      icon: Play,
      href: ROUTES.HOW_TO_USE,
    },
    {
      title: 'Settings',
      description: 'Privacy & preferences',
      icon: Shield,
      href: ROUTES.SETTINGS,
    },
  ];

  const getColorClasses = (color, highlight = false) => {
    const baseColors = {
      primary: highlight ? 'from-primary-500 to-primary-600' : 'bg-primary-600',
      success: highlight ? 'from-success-500 to-success-600' : 'bg-success-600',
      warning: highlight ? 'from-warning-500 to-warning-600' : 'bg-warning-600',
      error: highlight ? 'from-error-500 to-error-600' : 'bg-error-600',
    };
    
    if (highlight) {
      return `bg-gradient-to-br ${baseColors[color]} shadow-lg hover:shadow-xl transform hover:scale-105`;
    }
    
    return `${baseColors[color]} hover:opacity-90`;
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
      <div className="flex items-center space-x-3 mb-6">
        <div className="p-2 bg-gray-100 rounded-lg">
          <Stethoscope className="h-5 w-5 text-gray-600" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-gray-900">Quick Actions</h3>
          <p className="text-sm text-gray-500">Get started with these essential tools</p>
        </div>
      </div>

      {/* Primary Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {primaryActions.map((action) => {
          const Icon = action.icon;
          return (
            <Link
              key={action.title}
              to={action.href}
              className={`group p-6 rounded-xl text-white transition-all duration-300 ${getColorClasses(action.color, action.highlight)}`}
            >
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 bg-white bg-opacity-20 rounded-lg">
                  <Icon className="h-6 w-6" />
                </div>
                <ArrowRight className="h-5 w-5 opacity-70 group-hover:opacity-100 group-hover:translate-x-1 transition-all" />
              </div>
              
              <h4 className="text-lg font-semibold mb-2">
                {action.title}
              </h4>
              <p className="text-sm opacity-90">{action.description}</p>
            </Link>
          );
        })}
      </div>

      {/* Secondary Actions */}
      <div className="grid grid-cols-2 gap-3">
        {secondaryActions.map((action) => {
          const Icon = action.icon;
          return (
            <Link
              key={action.title}
              to={action.href}
              className="group p-4 border border-gray-200 rounded-lg hover:shadow-md transition-all duration-200 hover:border-gray-300"
            >
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-gray-100 rounded-lg group-hover:bg-gray-200 transition-colors">
                  <Icon className="h-4 w-4 text-gray-600" />
                </div>
                <div className="flex-1 min-w-0">
                  <h4 className="text-sm font-semibold text-gray-900 truncate">
                    {action.title}
                  </h4>
                  <p className="text-xs text-gray-600 truncate">{action.description}</p>
                </div>
              </div>
            </Link>
          );
        })}
      </div>

      <div className="mt-6 pt-4 border-t border-gray-200">
        <div className="flex items-center justify-center space-x-2 text-success-600">
          <Heart className="h-4 w-4" />
          <span className="text-sm font-medium">All tools are privacy-first and HIPAA-compliant</span>
        </div>
        <div className="text-center mt-2">
          <p className="text-xs text-gray-500">
            Your data is encrypted and never shared without consent
          </p>
        </div>
      </div>
    </div>
  );
};

export default QuickActions;