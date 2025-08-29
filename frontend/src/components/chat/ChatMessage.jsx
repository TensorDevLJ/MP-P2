jsx
// frontend/src/components/chat/ChatMessage.jsx
import React from 'react';
import { Bot, User, AlertTriangle, Clock } from 'lucide-react';

const ChatMessage = ({ message, onSuggestionClick }) => {
  const isBot = message.type === 'bot';
  const isCrisis = message.messageType === 'crisis';
  const isError = message.messageType === 'error';

  return (
    <div className={`flex ${isBot ? 'justify-start' : 'justify-end'} mb-4`}>
      <div className={`flex items-start space-x-3 max-w-xs lg:max-w-md ${!isBot && 'flex-row-reverse space-x-reverse'}`}>
        {/* Avatar */}
        <div className={`p-2 rounded-full ${
          isBot 
            ? isCrisis 
              ? 'bg-red-500' 
              : isError 
                ? 'bg-gray-500'
                : 'bg-blue-500'
            : 'bg-indigo-500'
        }`}>
          {isBot ? (
            <Bot className="w-4 h-4 text-white" />
          ) : (
            <User className="w-4 h-4 text-white" />
          )}
        </div>

        {/* Message Content */}
        <div className={`flex flex-col ${!isBot && 'items-end'}`}>
          <div className={`p-3 rounded-lg ${
            isBot 
              ? isCrisis
                ? 'bg-red-50 border border-red-200'
                : isError
                  ? 'bg-gray-50 border border-gray-200'
                  : 'bg-gray-100'
              : 'bg-indigo-500 text-white'
          }`}>
            {/* Crisis Header */}
            {isCrisis && (
              <div className="flex items-center space-x-2 mb-2 pb-2 border-b border-red-200">
                <AlertTriangle className="w-4 h-4 text-red-500" />
                <span className="font-semibold text-red-800 text-sm">Crisis Support</span>
              </div>
            )}

            {/* Message Text */}
            <div className={`text-sm whitespace-pre-wrap ${
              isCrisis ? 'text-red-900' : isError ? 'text-gray-700' : isBot ? 'text-gray-800' : 'text-white'
            }`}>
              {message.content}
            </div>

            {/* Timestamp */}
            <div className={`flex items-center space-x-1 mt-2 text-xs ${
              isCrisis ? 'text-red-600' : isError ? 'text-gray-500' : isBot ? 'text-gray-500' : 'text-indigo-200'
            }`}>
              <Clock className="w-3 h-3" />
              <span>{message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
            </div>
          </div>

          {/* Suggestions */}
          {message.suggestions && message.suggestions.length > 0 && (
            <div className="mt-2 space-y-1">
              <p className="text-xs text-gray-500 mb-2">Suggested topics:</p>
              {message.suggestions.map((suggestion, index) => (
                <button
                  key={index}
                  onClick={() => onSuggestionClick(suggestion)}
                  className="block text-left px-3 py-2 text-xs bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors border border-blue-200"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;