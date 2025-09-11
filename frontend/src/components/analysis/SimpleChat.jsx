import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { MessageCircle, Send, Brain, AlertTriangle, Phone } from 'lucide-react';
import { chatAPI } from '../../services/api';

const SimpleChat = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm your mental health assistant. I can help you understand your feelings and provide support. How are you feeling today?",
      isBot: true,
      timestamp: new Date(),
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: inputValue,
      isBot: false,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);

    try {
      const response = await chatAPI.sendMessage(inputValue);
      
      const botMessage = {
        id: Date.now() + 1,
        text: response.data.response,
        isBot: true,
        timestamp: new Date(),
        crisisDetected: response.data.crisis_detected,
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        text: "I'm having trouble responding right now. Please try again or contact support if this persists.",
        isBot: true,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-xl shadow-lg p-6 border border-gray-200"
      >
        <div className="flex items-center space-x-4">
          <div className="p-3 bg-primary-100 rounded-xl">
            <MessageCircle className="h-8 w-8 text-primary-600" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Mental Health Assistant</h1>
            <p className="text-gray-600">Get support and guidance for your mental wellness</p>
          </div>
        </div>
      </motion.div>

      {/* Chat Container */}
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 flex flex-col h-96">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((message) => (
            <div key={message.id} className={`flex ${message.isBot ? 'justify-start' : 'justify-end'}`}>
              <div className={`max-w-3xl px-4 py-3 rounded-2xl ${
                message.isBot 
                  ? 'bg-gray-100 text-gray-800' 
                  : 'bg-primary-600 text-white'
              }`}>
                {message.crisisDetected && (
                  <div className="mb-3 p-3 bg-error-100 border border-error-200 rounded-lg">
                    <div className="flex items-center space-x-2 text-error-700">
                      <Phone className="h-4 w-4" />
                      <span className="font-medium">Crisis Support: Call 988 immediately</span>
                    </div>
                  </div>
                )}
                <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.text}</p>
                <p className="text-xs opacity-70 mt-2">
                  {message.timestamp.toLocaleTimeString()}
                </p>
              </div>
            </div>
          ))}
          
          {isTyping && (
            <div className="flex justify-start">
              <div className="bg-gray-100 px-4 py-3 rounded-2xl">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input */}
        <div className="border-t border-gray-200 p-4">
          <div className="flex space-x-3">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              disabled={isTyping}
            />
            <button
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || isTyping}
              className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Send className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Disclaimer */}
      <div className="bg-warning-50 border border-warning-200 rounded-lg p-4">
        <div className="flex items-start space-x-2">
          <AlertTriangle className="h-4 w-4 text-warning-600 flex-shrink-0 mt-0.5" />
          <div className="text-sm text-warning-700">
            <p className="font-medium mb-1">Important Disclaimer</p>
            <p>
              This AI assistant provides general information and support. It cannot diagnose conditions or replace professional medical advice.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SimpleChat;