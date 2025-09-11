export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const ROUTES = {
  HOME: '/',
  DASHBOARD: '/dashboard',
  ANALYZE: '/analyze',
  ASSISTANT: '/assistant',
  SETTINGS: '/settings',
  LOGIN: '/login',
  SIGNUP: '/signup',
};

export const DEPRESSION_LEVELS = {
  not_depressed: { 
    label: 'Not Depressed', 
    color: 'success', 
    description: 'No significant depression indicators detected' 
  },
  mild: { 
    label: 'Mild Depression', 
    color: 'warning', 
    description: 'Early stage depression, manageable with self-care' 
  },
  moderate: { 
    label: 'Moderate Depression', 
    color: 'error', 
    description: 'Clear symptoms present, professional support recommended' 
  },
  severe: { 
    label: 'Severe Depression', 
    color: 'error', 
    description: 'Significant impairment, immediate professional help needed' 
  },
};

export const CRISIS_RESOURCES = [
  {
    name: 'National Suicide Prevention Lifeline',
    phone: '988',
    description: '24/7 crisis counseling and suicide prevention'
  },
  {
    name: 'Crisis Text Line',
    phone: 'Text HOME to 741741',
    description: 'Free 24/7 support via text message'
  },
  {
    name: 'Emergency Services',
    phone: '911',
    description: 'Immediate emergency medical assistance'
  }
];