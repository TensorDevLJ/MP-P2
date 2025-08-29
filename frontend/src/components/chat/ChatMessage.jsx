import React from 'react';
import { Brain, User, Clock, AlertTriangle } from 'lucide-react';
import { formatRelativeTime } from '../../utils/helpers';

const ChatMessage = ({ 
  message, 
  isBot = false, 
  timestamp, 
  isTyping = false,
  hasWarning = false 
}) => {
  return (
    <div className={`flex space-x-3 ${isBot ? 'justify-start' : 'justify-end'} mb-6`}>
      {isBot && (
        <div className="flex-shrink-0">
          <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
            <Brain className="h-4 w-4 text-primary-600" />
          </div>
        </div>
      )}

      <div className={`max-w-3xl ${isBot ? 'order-2' : 'order-1'}`}>
        <div
          className={`px-4 py-3 rounded-2xl ${
            isBot
              ? 'bg-gray-100 text-gray-800'
              : 'bg-primary-600 text-white'
          } ${hasWarning ? 'border-l-4 border-warning-500' : ''}`}
        >
          {hasWarning && (
            <div className="flex items-center space-x-2 mb-2 text-warning-600">
              <AlertTriangle className="h-4 w-4" />
              <span className="text-sm font-medium">Medical Disclaimer</span>
            </div>
          )}
          
          {isTyping ? (
            <div className="flex items-center space-x-2">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
              </div>
              <span className="text-sm text-gray-500">Assistant is thinking...</span>
            </div>
          ) : (
            <div className="text-sm leading-relaxed whitespace-pre-wrap">
              {message}
            </div>
          )}
        </div>

        {timestamp && !isTyping && (
          <div className={`flex items-center mt-2 ${isBot ? 'justify-start' : 'justify-end'}`}>
            <div className="flex items-center space-x-1 text-xs text-gray-500">
              <Clock className="h-3 w-3" />
              <span>{formatRelativeTime(timestamp)}</span>
            </div>
          </div>
        )}
      </div>

      {!isBot && (
        <div className="flex-shrink-0 order-2">
          <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center">
            <User className="h-4 w-4 text-white" />
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatMessage;