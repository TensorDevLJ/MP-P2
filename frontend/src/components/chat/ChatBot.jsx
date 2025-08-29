import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Brain, AlertTriangle, Phone, ExternalLink } from 'lucide-react';
import ChatMessage from './ChatMessage';
import { useAPIMutation } from '../../hooks/useAPI';
import { chatAPI } from '../../services/api';
import { CRISIS_RESOURCES } from '../../utils/constants';

const ChatBot = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      message: "Hello! I'm your AI health assistant. I can help you understand your EEG results, discuss mental health topics, and guide you to appropriate resources. How can I support you today?",
      isBot: true,
      timestamp: new Date(),
      hasWarning: true,
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [showCrisisAlert, setShowCrisisAlert] = useState(false);
  
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  // Mock chat mutation - in real app would call actual API
  const chatMutation = useAPIMutation(
    async (messageData) => {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Mock crisis detection
      const crisisKeywords = ['suicide', 'kill myself', 'end it all', 'hurt myself'];
      const hasCrisisContent = crisisKeywords.some(keyword => 
        messageData.message.toLowerCase().includes(keyword)
      );
      
      if (hasCrisisContent) {
        setShowCrisisAlert(true);
        return {
          message: "I'm very concerned about what you've shared. Please know that you're not alone, and help is available. I strongly encourage you to reach out to a crisis counselor immediately. Your life has value, and there are people who want to help you through this difficult time.",
          hasWarning: true,
          showCrisisResources: true,
        };
      }

      // Mock different response types based on message content
      const lowerMessage = messageData.message.toLowerCase();
      
      if (lowerMessage.includes('eeg') || lowerMessage.includes('brain') || lowerMessage.includes('analysis')) {
        return {
          message: "EEG analysis measures electrical activity in your brain across different frequency bands. Alpha waves (8-13 Hz) typically indicate relaxed awareness, while beta waves (13-30 Hz) are associated with active thinking. The AI looks for patterns that research has linked to emotional states and mental health indicators. Would you like me to explain any specific part of your results?",
          hasWarning: false,
        };
      }
      
      if (lowerMessage.includes('anxiety') || lowerMessage.includes('stressed') || lowerMessage.includes('worry')) {
        return {
          message: "Anxiety is a common experience that can show up in both your thoughts and your brain activity. Some helpful techniques include:\n\n• Box breathing (4-4-4-4 count)\n• Progressive muscle relaxation\n• Mindfulness meditation\n• Regular exercise\n\nYour EEG data can help identify when your nervous system is in a heightened state. Would you like specific guidance for any anxiety symptoms you're experiencing?",
          hasWarning: true,
        };
      }
      
      if (lowerMessage.includes('depression') || lowerMessage.includes('sad') || lowerMessage.includes('down')) {
        return {
          message: "I understand you're asking about depression. While EEG patterns can show some correlations with mood, depression is complex and involves many factors. The platform can identify certain brainwave patterns, but professional evaluation is important for proper assessment and treatment.\n\nIf you're experiencing persistent low mood, please consider speaking with a mental health professional. Would you like help finding care providers in your area?",
          hasWarning: true,
        };
      }

      // Default supportive response
      return {
        message: "Thank you for sharing that with me. I'm here to provide information and support based on current mental health research and your EEG analysis results. Remember that while I can offer insights and evidence-based suggestions, I'm not a replacement for professional medical advice.\n\nIs there something specific about your mental health or EEG results you'd like to explore?",
        hasWarning: true,
      };
    },
    {
      onSuccess: (response) => {
        setMessages(prev => [
          ...prev,
          {
            id: Date.now(),
            message: response.message,
            isBot: true,
            timestamp: new Date(),
            hasWarning: response.hasWarning,
            showCrisisResources: response.showCrisisResources,
          }
        ]);
        setIsTyping(false);
      },
      onError: () => {
        setMessages(prev => [
          ...prev,
          {
            id: Date.now(),
            message: "I apologize, but I'm having trouble processing your message right now. Please try again in a moment, or if this persists, consider reaching out to our support team.",
            isBot: true,
            timestamp: new Date(),
            hasWarning: true,
          }
        ]);
        setIsTyping(false);
      },
    }
  );

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = {
      id: Date.now(),
      message: inputValue,
      isBot: false,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);

    await chatMutation.mutateAsync({ message: inputValue });
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Page Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="bg-white rounded-xl shadow-lg p-6 border border-gray-200"
      >
        <div className="flex items-center space-x-4">
          <div className="p-3 bg-primary-100 rounded-xl">
            <Brain className="h-8 w-8 text-primary-600" />
          </div>
          <div>
            <h1 className="text-2xl lg:text-3xl font-bold text-gray-900">Health Assistant</h1>
            <p className="text-gray-600">
              Ask questions about your mental health, EEG results, or get personalized guidance
            </p>
          </div>
        </div>
      </motion.div>

      {/* Crisis Alert */}
      <AnimatePresence>
        {showCrisisAlert && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="bg-error-50 border-2 border-error-200 rounded-xl p-6 shadow-lg"
          >
            <div className="flex items-center space-x-3 mb-4">
              <AlertTriangle className="h-6 w-6 text-error-600" />
              <h3 className="text-lg font-semibold text-error-900">Crisis Support Available</h3>
            </div>
            
            <p className="text-error-800 mb-6">
              If you're having thoughts of self-harm or suicide, please reach out for immediate support. 
              You don't have to go through this alone.
            </p>
            
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {CRISIS_RESOURCES.map((resource, index) => (
                <div key={index} className="bg-white border border-error-200 rounded-lg p-4">
                  <h4 className="font-semibold text-error-900 mb-1">{resource.name}</h4>
                  <p className="text-sm text-error-700 mb-3">{resource.description}</p>
                  <a
                    href={`tel:${resource.phone.replace(/[^0-9]/g, '')}`}
                    className="inline-flex items-center space-x-2 text-error-600 hover:text-error-800 font-medium"
                  >
                    <Phone className="h-4 w-4" />
                    <span>{resource.phone}</span>
                  </a>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Chat Container */}
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 flex flex-col h-96 lg:h-[600px]">
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          <AnimatePresence>
            {messages.map((message) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.3 }}
              >
                <ChatMessage
                  message={message.message}
                  isBot={message.isBot}
                  timestamp={message.timestamp}
                  hasWarning={message.hasWarning}
                />
              </motion.div>
            ))}
          </AnimatePresence>
          
          {isTyping && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <ChatMessage isBot={true} isTyping={true} />
            </motion.div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-200 p-4">
          <div className="flex items-center space-x-3">
            <div className="flex-1 relative">
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about your mental health, EEG results, or get guidance..."
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 resize-none text-sm"
                rows="1"
                style={{ minHeight: '44px' }}
                disabled={chatMutation.isLoading}
              />
            </div>
            
            <button
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || chatMutation.isLoading}
              className="bg-primary-600 text-white p-3 rounded-lg hover:bg-primary-700 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Send className="h-5 w-5" />
            </button>
          </div>
          
          <div className="mt-3 flex items-center justify-between text-xs text-gray-500">
            <span>Press Enter to send, Shift+Enter for new line</span>
            <span className={`${inputValue.length > 4500 ? 'text-error-600' : ''}`}>
              {inputValue.length}/5000
            </span>
          </div>
        </div>
      </div>

      {/* Safety Disclaimer */}
      <div className="bg-warning-50 border border-warning-200 rounded-lg p-4">
        <div className="flex items-start space-x-2">
          <AlertTriangle className="h-4 w-4 text-warning-600 flex-shrink-0 mt-0.5" />
          <div className="text-sm text-warning-700">
            <p className="font-medium mb-1">Important Disclaimer</p>
            <p>
              This AI assistant provides general information and support based on current research. 
              It cannot diagnose conditions or replace professional medical advice. Always consult 
              qualified healthcare providers for medical concerns.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatBot;