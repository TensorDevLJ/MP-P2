import React from 'react';
import { Brain } from 'lucide-react';

const LoadingSpinner = ({ size = 'medium', message = 'Loading...', className = '' }) => {
  const sizeClasses = {
    small: 'h-4 w-4',
    medium: 'h-8 w-8',
    large: 'h-12 w-12',
  };

  return (
    <div className={`flex flex-col items-center justify-center space-y-3 ${className}`}>
      <div className="relative">
        <Brain 
          className={`${sizeClasses[size]} text-primary-600 animate-pulse`}
        />
        <div className={`absolute inset-0 ${sizeClasses[size]} border-2 border-primary-600 border-t-transparent rounded-full animate-spin`} />
      </div>
      <p className="text-sm text-gray-600 font-medium">{message}</p>
    </div>
  );
};

export default LoadingSpinner;