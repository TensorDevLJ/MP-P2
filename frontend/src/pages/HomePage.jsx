import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Brain, 
  Shield, 
  Zap, 
  Users, 
  ChevronRight, 
  CheckCircle,
  Star,
  Play,
  ArrowRight,
  Heart,
  Lock,
  Award
} from 'lucide-react';
import { ROUTES } from '../utils/constants';

const HomePage = () => {
  const features = [
    {
      icon: Brain,
      title: 'Advanced EEG Analysis',
      description: 'AI-powered analysis of brainwave patterns for mental health insights',
      color: 'primary',
    },
    {
      icon: Shield,
      title: 'Privacy First',
      description: 'End-to-end encryption with complete data control and transparency',
      color: 'success',
    },
    {
      icon: Zap,
      title: 'Real-time Insights',
      description: 'Get immediate feedback and personalized recommendations',
      color: 'warning',
    },
    {
      icon: Users,
      title: 'Care Integration',
      description: 'Connect with mental health professionals in your area',
      color: 'error',
    },
  ];

  const benefits = [
    'AI-powered EEG signal analysis',
    'Depression and anxiety screening',
    'Personalized wellness recommendations',
    'Progress tracking and trends',
    'Crisis support resources',
    'Professional care finder',
  ];

  const testimonials = [
    {
      name: 'Dr. Sarah Chen',
      role: 'Neuropsychologist',
      content: 'This platform provides valuable supplementary insights for understanding brain activity patterns.',
      rating: 5,
    },
    {
      name: 'Alex Kumar',
      role: 'Wellness Researcher',
      content: 'The combination of objective EEG data with subjective reports creates a comprehensive mental health picture.',
      rating: 5,
    },
    {
      name: 'Dr. Maria Rodriguez',
      role: 'Clinical Psychologist',
      content: 'An excellent tool for encouraging self-awareness and connecting patients with appropriate care.',
      rating: 5,
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-blue-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-gray-200 px-6 py-4 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <Brain className="h-8 w-8 text-primary-600" />
            <span className="text-xl font-bold text-gray-900">EEG Health Assistant</span>
          </div>
          <div className="flex items-center space-x-4">
            <Link 
              to={ROUTES.LOGIN}
              className="text-gray-600 hover:text-gray-900 transition-colors font-medium"
            >
              Login
            </Link>
            <Link 
              to={ROUTES.SIGNUP}
              className="bg-primary-600 text-white px-6 py-2.5 rounded-lg hover:bg-primary-700 transition-colors font-medium shadow-sm hover:shadow-md"
            >
              Get Started
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="px-6 py-12 lg:py-20">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="text-center lg:text-left"
            >
              <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 mb-6 leading-tight">
                AI-Powered
                <span className="text-primary-600 block">Mental Health</span>
                Insights
              </h1>
              
              <p className="text-xl text-gray-600 mb-8 leading-relaxed">
                Combine objective EEG brain signals with subjective self-reports for comprehensive 
                mental health analysis, personalized recommendations, and professional care connections.
              </p>

              <div className="flex flex-col sm:flex-row gap-4 mb-8">
                <Link
                  to={ROUTES.SIGNUP}
                  className="bg-primary-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-primary-700 transition-all duration-300 shadow-lg hover:shadow-xl flex items-center justify-center space-x-2"
                >
                  <span>Start Free Analysis</span>
                  <ArrowRight className="h-5 w-5" />
                </Link>
                
                <button className="bg-white text-primary-600 border-2 border-primary-600 px-8 py-4 rounded-xl font-semibold hover:bg-primary-50 transition-colors flex items-center justify-center space-x-2">
                  <Play className="h-5 w-5" />
                  <span>Watch Demo</span>
                </button>
              </div>

              <div className="flex items-center space-x-6 text-sm text-gray-500">
                <div className="flex items-center space-x-2">
                  <Shield className="h-4 w-4 text-success-600" />
                  <span>HIPAA Compliant</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Lock className="h-4 w-4 text-success-600" />
                  <span>Privacy First</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Award className="h-4 w-4 text-success-600" />
                  <span>Clinical Grade</span>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="relative"
            >
              <div className="bg-white rounded-2xl shadow-2xl p-6 border border-gray-200">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-3 h-3 bg-error-500 rounded-full"></div>
                  <div className="w-3 h-3 bg-warning-500 rounded-full"></div>
                  <div className="w-3 h-3 bg-success-500 rounded-full"></div>
                </div>
                
                <div className="space-y-4">
                  <div className="bg-gradient-to-r from-primary-100 to-blue-100 p-4 rounded-lg">
                    <h3 className="font-semibold text-gray-900 mb-2">Current Mental State</h3>
                    <div className="flex items-center space-x-3">
                      <div className="flex-1">
                        <div className="text-sm text-gray-600 mb-1">Stable - 87% Confidence</div>
                        <div className="w-full bg-white rounded-full h-2">
                          <div className="bg-success-500 h-2 rounded-full w-5/6 transition-all duration-1000"></div>
                        </div>
                      </div>
                      <Heart className="h-5 w-5 text-success-500" />
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-3">
                    <div className="bg-gray-50 p-3 rounded-lg text-center">
                      <div className="text-lg font-bold text-primary-600">Alpha</div>
                      <div className="text-xs text-gray-500">8-13 Hz</div>
                    </div>
                    <div className="bg-gray-50 p-3 rounded-lg text-center">
                      <div className="text-lg font-bold text-warning-600">Beta</div>
                      <div className="text-xs text-gray-500">13-30 Hz</div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="absolute -top-4 -right-4 w-24 h-24 bg-primary-200 rounded-full opacity-20 animate-pulse"></div>
              <div className="absolute -bottom-6 -left-6 w-32 h-32 bg-success-200 rounded-full opacity-20 animate-pulse-soft"></div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="px-6 py-16 bg-white">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
              Advanced Mental Health Technology
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Combining cutting-edge neuroscience with AI to provide unprecedented insights into your mental wellbeing
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  viewport={{ once: true }}
                  className="text-center group"
                >
                  <div className={`w-16 h-16 mx-auto mb-4 bg-${feature.color}-100 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300`}>
                    <Icon className={`h-8 w-8 text-${feature.color}-600`} />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">{feature.title}</h3>
                  <p className="text-gray-600">{feature.description}</p>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="px-6 py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
            >
              <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-6">
                Complete Mental Health Ecosystem
              </h2>
              <p className="text-lg text-gray-600 mb-8">
                Our platform combines objective brain data with your personal experiences to create 
                a comprehensive understanding of your mental health journey.
              </p>
              
              <div className="space-y-4">
                {benefits.map((benefit, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.4, delay: index * 0.1 }}
                    viewport={{ once: true }}
                    className="flex items-center space-x-3"
                  >
                    <CheckCircle className="h-5 w-5 text-success-600 flex-shrink-0" />
                    <span className="text-gray-700">{benefit}</span>
                  </motion.div>
                ))}
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              viewport={{ once: true }}
              className="bg-white rounded-2xl shadow-xl p-8"
            >
              <h3 className="text-xl font-bold text-gray-900 mb-6">How It Works</h3>
              <div className="space-y-6">
                <div className="flex items-start space-x-4">
                  <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <span className="text-sm font-bold text-primary-600">1</span>
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-1">Upload EEG Data</h4>
                    <p className="text-sm text-gray-600">Securely upload your brainwave recordings for analysis</p>
                  </div>
                </div>
                
                <div className="flex items-start space-x-4">
                  <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <span className="text-sm font-bold text-primary-600">2</span>
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-1">Share Your Feelings</h4>
                    <p className="text-sm text-gray-600">Provide context through text about your current state</p>
                  </div>
                </div>
                
                <div className="flex items-start space-x-4">
                  <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <span className="text-sm font-bold text-primary-600">3</span>
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-1">Get Insights</h4>
                    <p className="text-sm text-gray-600">Receive AI-powered analysis and personalized recommendations</p>
                  </div>
                </div>
                
                <div className="flex items-start space-x-4">
                  <div className="w-8 h-8 bg-success-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <CheckCircle className="h-5 w-5 text-success-600" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-1">Take Action</h4>
                    <p className="text-sm text-gray-600">Follow guided activities or connect with care providers</p>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="px-6 py-16 bg-white">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
              Trusted by Healthcare Professionals
            </h2>
            <p className="text-xl text-gray-600">
              Leading researchers and clinicians recognize the value of our approach
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-gray-50 rounded-xl p-6 border border-gray-200"
              >
                <div className="flex items-center space-x-1 mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="h-4 w-4 text-warning-500 fill-current" />
                  ))}
                </div>
                
                <blockquote className="text-gray-700 mb-4 italic">
                  "{testimonial.content}"
                </blockquote>
                
                <div>
                  <div className="font-semibold text-gray-900">{testimonial.name}</div>
                  <div className="text-sm text-gray-500">{testimonial.role}</div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="px-6 py-16 bg-gradient-to-r from-primary-600 to-blue-600">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl lg:text-4xl font-bold text-white mb-6">
              Ready to Understand Your Mental Health Better?
            </h2>
            <p className="text-xl text-primary-100 mb-8">
              Join thousands of users taking a proactive approach to mental wellness with AI-powered insights.
            </p>
            
            <Link
              to={ROUTES.SIGNUP}
              className="inline-flex items-center space-x-2 bg-white text-primary-600 px-8 py-4 rounded-xl font-semibold hover:bg-primary-50 transition-colors shadow-lg hover:shadow-xl"
            >
              <span>Start Your Journey</span>
              <ChevronRight className="h-5 w-5" />
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white px-6 py-12">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <Brain className="h-6 w-6 text-primary-400" />
                <span className="text-lg font-bold">EEG Health Assistant</span>
              </div>
              <p className="text-gray-400 text-sm">
                AI-powered mental health insights combining objective brain data with personal experiences.
              </p>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Platform</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><Link to={ROUTES.HOW_TO_USE} className="hover:text-white transition-colors">How It Works</Link></li>
                <li><Link to="#" className="hover:text-white transition-colors">Security</Link></li>
                <li><Link to="#" className="hover:text-white transition-colors">Privacy Policy</Link></li>
                <li><Link to="#" className="hover:text-white transition-colors">Terms of Service</Link></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><Link to="#" className="hover:text-white transition-colors">Help Center</Link></li>
                <li><Link to="#" className="hover:text-white transition-colors">Contact Us</Link></li>
                <li><Link to="#" className="hover:text-white transition-colors">Community</Link></li>
                <li><Link to="#" className="hover:text-white transition-colors">Crisis Resources</Link></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Connect</h4>
              <p className="text-sm text-gray-400 mb-4">
                Stay updated with the latest in mental health technology
              </p>
              <div className="flex space-x-4">
                <button className="w-8 h-8 bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors"></button>
                <button className="w-8 h-8 bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors"></button>
                <button className="w-8 h-8 bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors"></button>
              </div>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-sm text-gray-400">
            <p>&copy; 2025 EEG Health Assistant. All rights reserved. This platform provides supportive insights, not medical diagnosis.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;