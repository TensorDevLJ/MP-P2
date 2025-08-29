import { format, formatDistanceToNow } from 'date-fns';

export const formatDate = (date, formatStr = 'MMM dd, yyyy') => {
  return format(new Date(date), formatStr);
};

export const formatRelativeTime = (date) => {
  return formatDistanceToNow(new Date(date), { addSuffix: true });
};

export const getStateColorClasses = (state) => {
  const colorMap = {
    success: 'bg-success-50 text-success-700 border-success-200',
    warning: 'bg-warning-50 text-warning-700 border-warning-200',
    error: 'bg-error-50 text-error-700 border-error-200',
  };
  return colorMap[state] || colorMap.success;
};

export const validateCSVFile = (file) => {
  const errors = [];
  
  if (!file) {
    errors.push('No file selected');
    return errors;
  }
  
  if (file.type !== 'text/csv' && !file.name.endsWith('.csv')) {
    errors.push('File must be a CSV format');
  }
  
  if (file.size > 50 * 1024 * 1024) { // 50MB limit
    errors.push('File size must be less than 50MB');
  }
  
  if (file.size < 100) {
    errors.push('File appears to be too small to contain valid EEG data');
  }
  
  return errors;
};

export const parseCSVSampleRate = (filename) => {
  const match = filename.match(/(\d+)hz/i);
  return match ? parseInt(match[1]) : null;
};

export const formatConfidenceScore = (score) => {
  return Math.round(score * 100);
};

export const debounce = (func, wait) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};