export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const ROUTES = {
  HOME: '/',
  DASHBOARD: '/dashboard',
  ANALYZE: '/analyze',
  ASSISTANT: '/assistant',
  CARE: '/care',
  TRENDS: '/trends',
  SETTINGS: '/settings',
  HOW_TO_USE: '/how-to-use',
  LOGIN: '/login',
  SIGNUP: '/signup',
};

export const MENTAL_HEALTH_STATES = {
  STABLE: { 
    label: 'Stable', 
    color: 'success', 
    description: 'Mental state appears balanced and healthy' 
  },
  MILD: { 
    label: 'Mild Concern', 
    color: 'warning', 
    description: 'Some signs of stress or mood changes' 
  },
  MODERATE: { 
    label: 'Moderate Risk', 
    color: 'warning', 
    description: 'Notable symptoms requiring attention' 
  },
  HIGH: { 
    label: 'High Risk', 
    color: 'error', 
    description: 'Significant concerns requiring immediate support' 
  },
};

export const EEG_BANDS = {
  delta: { range: '0.5-4 Hz', color: '#8B5CF6', name: 'Delta' },
  theta: { range: '4-8 Hz', color: '#06B6D4', name: 'Theta' },
  alpha: { range: '8-13 Hz', color: '#10B981', name: 'Alpha' },
  beta: { range: '13-30 Hz', color: '#F59E0B', name: 'Beta' },
  gamma: { range: '30-50 Hz', color: '#EF4444', name: 'Gamma' },
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