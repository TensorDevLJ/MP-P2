import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Bell, 
  X, 
  CheckCircle, 
  AlertTriangle, 
  Calendar,
  Brain,
  Heart,
  MessageCircle,
  Clock,
  Settings
} from 'lucide-react';
import { formatRelativeTime } from '../../utils/helpers';

const NotificationCenter = ({ isOpen, onClose }) => {
  const [activeTab, setActiveTab] = useState('all');

  // Mock notifications data
  const notifications = [
    {
      id: '1',
      type: 'analysis',
      title: 'EEG Analysis Complete',
      message: 'Your latest brain activity analysis shows stable patterns with 87% confidence.',
      timestamp: new Date(Date.now() - 30 * 60 * 1000), // 30 minutes ago
      read: false,
      priority: 'normal',
      icon: Brain,
      color: 'primary',
    },
    {
      id: '2',
      type: 'reminder',
      title: 'Meditation Reminder',
      message: "Time for your 5-minute morning meditation session. You're 3 days into your streak!",
      timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
      read: true,
      priority: 'normal',
      icon: Heart,
      color: 'success',
    },
    {
      id: '3',
      type: 'alert',
      title: 'Weekly Check-in',
      message: 'How are you feeling this week? Complete a quick mood assessment to track your progress.',
      timestamp: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000), // 1 day ago
      read: false,
      priority: 'high',
      icon: MessageCircle,
      color: 'warning',
    },
    {
      id: '4',
      type: 'achievement',
      title: 'Achievement Unlocked!',
      message: 'Congratulations! You\'ve completed 7 consecutive days of meditation practice.',
      timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000), // 2 days ago
      read: true,
      priority: 'normal',
      icon: CheckCircle,
      color: 'success',
    },
    {
      id: '5',
      type: 'system',
      title: 'Privacy Update',
      message: 'We\'ve updated our privacy policy to enhance data protection. Review the changes.',
      timestamp: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000), // 3 days ago
      read: false,
      priority: 'normal',
      icon: Settings,
      color: 'primary',
    },
  ];

  const tabs = [
    { id: 'all', label: 'All', count: notifications.length },
    { id: 'unread', label: 'Unread', count: notifications.filter(n => !n.read).length },
    { id: 'important', label: 'Important', count: notifications.filter(n => n.priority === 'high').length },
  ];

  const filteredNotifications = notifications.filter(notification => {
    if (activeTab === 'unread') return !notification.read;
    if (activeTab === 'important') return notification.priority === 'high';
    return true;
  });

  const markAsRead = (notificationId) => {
    // In real app, would call API to mark as read
    console.log('Marking as read:', notificationId);
  };

  const deleteNotification = (notificationId) => {
    // In real app, would call API to delete
    console.log('Deleting notification:', notificationId);
  };

  const markAllAsRead = () => {
    // In real app, would call API
    console.log('Marking all as read');
  };

  const getNotificationColorClasses = (color, read) => {
    const baseClasses = {
      primary: read ? 'bg-gray-50 border-gray-200' : 'bg-primary-50 border-primary-200',
      success: read ? 'bg-gray-50 border-gray-200' : 'bg-success-50 border-success-200',
      warning: read ? 'bg-gray-50 border-gray-200' : 'bg-warning-50 border-warning-200',
      error: read ? 'bg-gray-50 border-gray-200' : 'bg-error-50 border-error-200',
    };
    return baseClasses[color] || baseClasses.primary;
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Overlay */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-50 z-50"
            onClick={onClose}
          />

          {/* Notification Panel */}
          <motion.div
            initial={{ opacity: 0, x: 300 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 300 }}
            className="fixed right-0 top-0 h-full w-full max-w-md bg-white shadow-2xl z-50 overflow-hidden"
          >
            {/* Header */}
            <div className="bg-white border-b border-gray-200 p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-primary-100 rounded-lg">
                    <Bell className="h-5 w-5 text-primary-600" />
                  </div>
                  <div>
                    <h2 className="text-xl font-bold text-gray-900">Notifications</h2>
                    <p className="text-sm text-gray-500">Stay updated on your health journey</p>
                  </div>
                </div>
                <button
                  onClick={onClose}
                  className="p-2 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>

              {/* Tabs */}
              <div className="flex space-x-1 bg-gray-100 rounded-lg p-1">
                {tabs.map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex-1 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      activeTab === tab.id
                        ? 'bg-white text-gray-900 shadow-sm'
                        : 'text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    {tab.label}
                    {tab.count > 0 && (
                      <span className={`ml-2 px-2 py-0.5 rounded-full text-xs ${
                        activeTab === tab.id ? 'bg-gray-200 text-gray-700' : 'bg-gray-200 text-gray-600'
                      }`}>
                        {tab.count}
                      </span>
                    )}
                  </button>
                ))}
              </div>

              {filteredNotifications.filter(n => !n.read).length > 0 && (
                <div className="flex justify-end mt-4">
                  <button
                    onClick={markAllAsRead}
                    className="text-primary-600 hover:text-primary-700 text-sm font-medium"
                  >
                    Mark all as read
                  </button>
                </div>
              )}
            </div>

            {/* Notifications List */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4">
              {filteredNotifications.map((notification) => {
                const Icon = notification.icon;
                return (
                  <motion.div
                    key={notification.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    className={`p-4 border rounded-lg transition-all hover:shadow-sm ${getNotificationColorClasses(notification.color, notification.read)}`}
                  >
                    <div className="flex items-start space-x-3">
                      <div className={`p-2 rounded-lg ${
                        notification.read 
                          ? 'bg-gray-100 text-gray-500' 
                          : `bg-${notification.color}-100 text-${notification.color}-600`
                      }`}>
                        <Icon className="h-4 w-4" />
                      </div>
                      
                      <div className="flex-1 min-w-0">
                        <div className="flex items-start justify-between">
                          <h4 className={`font-semibold text-sm ${
                            notification.read ? 'text-gray-700' : 'text-gray-900'
                          }`}>
                            {notification.title}
                          </h4>
                          <button
                            onClick={() => deleteNotification(notification.id)}
                            className="text-gray-400 hover:text-gray-600 transition-colors ml-2"
                          >
                            <X className="h-4 w-4" />
                          </button>
                        </div>
                        
                        <p className={`text-sm mt-1 ${
                          notification.read ? 'text-gray-500' : 'text-gray-700'
                        }`}>
                          {notification.message}
                        </p>
                        
                        <div className="flex items-center justify-between mt-3">
                          <div className="flex items-center space-x-1 text-xs text-gray-500">
                            <Clock className="h-3 w-3" />
                            <span>{formatRelativeTime(notification.timestamp)}</span>
                          </div>
                          
                          {!notification.read && (
                            <button
                              onClick={() => markAsRead(notification.id)}
                              className="text-xs text-primary-600 hover:text-primary-700 font-medium"
                            >
                              Mark as read
                            </button>
                          )}
                        </div>
                      </div>

                      {!notification.read && (
                        <div className="w-2 h-2 bg-primary-600 rounded-full flex-shrink-0 mt-2"></div>
                      )}
                    </div>
                  </motion.div>
                );
              })}

              {filteredNotifications.length === 0 && (
                <div className="text-center py-12">
                  <Bell className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">All caught up!</h3>
                  <p className="text-gray-600">No notifications in this category</p>
                </div>
              )}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};

export default NotificationCenter;