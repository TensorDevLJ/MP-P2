// frontend/src/components/chat/ChatBot.jsx
import React, { useState, useRef, useEffect } from 'react';
import { useMutation } from '@tanstack/react-query';
import { 
  Send, 
  Bot, 
  User, 
  AlertTriangle,
  Lightbulb,
  Heart,
  MessageSquare
} from 'lucide-react';
import { toast } from 'react-hot-toast';

import { api } from '../../services/api';
import ChatMessage from './ChatMessage';

const ChatBot = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: "Hello! I'm your mental health assistant. I'm here to provide support, answer questions about your analysis results, and help you understand your mental wellness journey. How can I help you today?",
      timestamp: new Date(),
      suggestions: [
        "Explain my latest EEG results",
        "What are some stress management techniques?",
        "How can I improve my sleep quality?"
      ]
    }
  ]);
  
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const chatMutation = useMutation({
    mutationFn: (message) => api.post('/analysis/chat', { message }),
    onSuccess: (response) => {
      const botMessage = {
        id: Date.now(),
        type: 'bot',
        content: response.response,
        timestamp: new Date(),
        suggestions: response.suggestions || [],
        messageType: response.type || 'normal'
      };

      setMessages(prev => [...prev, botMessage]);
      setIsTyping(false);

      if (response.type === 'crisis') {
        toast.error('Crisis support resources provided. Please seek immediate help if needed.');
      }
    },
    onError: (error) => {
      setIsTyping(false);
      toast.error('Sorry, I encountered an error. Please try again.');
      
      const errorMessage = {
        id: Date.now(),
        type: 'bot',
        content: "I apologize, but I'm having trouble responding right now. If you're experiencing a mental health crisis, please contact emergency services or a crisis hotline immediately.",
        timestamp: new Date(),
        messageType: 'error'
      };
      
      setMessages(prev => [...prev, errorMessage]);
    }
  });

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSendMessage = (messageText = null) => {
    const messageToSend = messageText || inputMessage.trim();
    
    if (!messageToSend) return;

    // Add user message
    const userMessage = {
      id: Date.now() - 1,
      type: 'user',
      content: messageToSend,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    // Send to API
    chatMutation.mutate(messageToSend);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleSuggestionClick = (suggestion) => {
    handleSendMessage(suggestion);
  };

  return (
    <div className="bg-white rounded-lg shadow-lg flex flex-col h-[700px]">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-4 rounded-t-lg">
        <div className="flex items-center space-x-3">
          <div className="bg-white/20 p-2 rounded-full">
            <Bot className="w-6 h-6" />
          </div>
          <div>
            <h3 className="font-semibold">Mental Health Assistant</h3>
            <p className="text-sm text-blue-100">
              AI-powered support and guidance
            </p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <ChatMessage
            key={message.id}
            message={message}
            onSuggestionClick={handleSuggestionClick}
          />
        ))}
        
        {isTyping && (
          <div className="flex items-center space-x-3">
            <div className="bg-blue-500 p-2 rounded-full">
              <Bot className="w-4 h-4 text-white" />
            </div>
            <div className="bg-gray-100 p-3 rounded-lg max-w-xs">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Actions */}
      <div className="px-4 py-2 bg-gray-50 border-t">
        <div className="flex flex-wrap gap-2">
          {[
            { icon: Heart, text: "I'm feeling anxious", color: "red" },
            { icon: Lightbulb, text: "Coping strategies", color: "yellow" },
            { icon: MessageSquare, text: "Explain my results", color: "blue" }
          ].map((action, index) => (
            <button
              key={index}
              onClick={() => handleSendMessage(action.text)}
              className={`flex items-center space-x-1 px-3 py-1 rounded-full text-xs bg-${action.color}-100 text-${action.color}-800 hover:bg-${action.color}-200 transition-colors`}
            >
              <action.icon className="w-3 h-3" />
              <span>{action.text}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Input */}
      {/* Input */}
  <div className="p-4 border-t">
    <div className="flex items-end space-x-3">
      <div className="flex-1">
        <textarea
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask me about mental health, your results, or how you're feeling..."
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
          rows={2}
          disabled={chatMutation.isPending}
        />
        <p className="text-xs text-gray-500 mt-1">
          Press Enter to send, Shift+Enter for new line
        </p>
      </div>
      <button
        onClick={() => handleSendMessage()}
        disabled={!inputMessage.trim() || chatMutation.isPending}
        className="bg-blue-500 text-white p-3 rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <Send className="w-5 h-5" />
      </button>
    </div>
  </div>

  {/* Disclaimer */}
  <div className="px-4 pb-4">
    <div className="bg-amber-50 border border-amber-200 rounded-lg p-3">
      <div className="flex items-start space-x-2">
        <AlertTriangle className="w-4 h-4 text-amber-500 mt-0.5" />
        <div className="text-xs text-amber-800">
          <p className="font-medium">Important Disclaimer</p>
          <p>This AI assistant provides supportive information only and is not a substitute for professional medical advice, diagnosis, or treatment.</p>
        </div>
      </div>
    </div>
  </div>
</div>
);
};
export default ChatBot;