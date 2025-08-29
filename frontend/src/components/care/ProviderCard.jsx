import React from 'react';
import { 
  Phone, 
  Star, 
  MapPin, 
  Clock, 
  CheckCircle, 
  ExternalLink,
  User,
  Globe,
  DollarSign
} from 'lucide-react';

const ProviderCard = ({ provider, onSelect, compact = false }) => {
  const handleCall = (phone) => {
    window.location.href = `tel:${phone.replace(/[^0-9+]/g, '')}`;
  };

  const handleDirections = () => {
    const query = encodeURIComponent(provider.address);
    window.open(`https://maps.google.com/?q=${query}`, '_blank');
  };

  if (compact) {
    return (
      <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h3 className="font-semibold text-gray-900 mb-1">{provider.name}</h3>
            <p className="text-sm text-gray-600 mb-2">{provider.type}</p>
            <div className="flex items-center space-x-4 text-sm text-gray-500">
              <div className="flex items-center space-x-1">
                <Star className="h-4 w-4 text-warning-500" />
                <span>{provider.rating}</span>
              </div>
              <div className="flex items-center space-x-1">
                <MapPin className="h-4 w-4" />
                <span>{provider.distance} km</span>
              </div>
            </div>
          </div>
          <button
            onClick={() => handleCall(provider.phone)}
            className="bg-primary-600 text-white p-2 rounded-lg hover:bg-primary-700 transition-colors"
          >
            <Phone className="h-4 w-4" />
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden hover:shadow-xl transition-shadow">
      {/* Header */}
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center space-x-3 mb-2">
              <h3 className="text-xl font-bold text-gray-900">{provider.name}</h3>
              {provider.openNow && (
                <span className="bg-success-100 text-success-700 px-2 py-1 rounded-full text-xs font-medium">
                  Open Now
                </span>
              )}
            </div>
            
            <p className="text-gray-600 mb-3">{provider.type}</p>
            
            <div className="flex items-center space-x-4 text-sm">
              <div className="flex items-center space-x-1">
                <Star className="h-4 w-4 text-warning-500 fill-current" />
                <span className="font-medium">{provider.rating}</span>
                <span className="text-gray-500">({provider.reviewCount} reviews)</span>
              </div>
              
              <div className="flex items-center space-x-1 text-gray-600">
                <MapPin className="h-4 w-4" />
                <span>{provider.distance} km away</span>
              </div>
            </div>
          </div>
          
          <div className="text-right">
            <p className="text-sm text-gray-500 mb-1">Next Available</p>
            <p className="text-sm font-medium text-gray-900">
              {new Date(provider.nextAvailable).toLocaleDateString('en-IN', {
                month: 'short',
                day: 'numeric',
                hour: 'numeric',
                minute: '2-digit',
              })}
            </p>
          </div>
        </div>
      </div>

      {/* Details */}
      <div className="p-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
          {/* Specialties */}
          <div>
            <div className="flex items-center space-x-2 mb-2">
              <User className="h-4 w-4 text-gray-600" />
              <span className="text-sm font-medium text-gray-700">Specialties</span>
            </div>
            <div className="flex flex-wrap gap-1">
              {provider.specialties.map((specialty, index) => (
                <span
                  key={index}
                  className="bg-primary-100 text-primary-700 px-2 py-1 rounded-full text-xs"
                >
                  {specialty}
                </span>
              ))}
            </div>
          </div>
          
          {/* Languages */}
          <div>
            <div className="flex items-center space-x-2 mb-2">
              <Globe className="h-4 w-4 text-gray-600" />
              <span className="text-sm font-medium text-gray-700">Languages</span>
            </div>
            <div className="flex flex-wrap gap-1">
              {provider.languages.map((language, index) => (
                <span
                  key={index}
                  className="bg-gray-100 text-gray-700 px-2 py-1 rounded-full text-xs"
                >
                  {language}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Address and Fees */}
        <div className="space-y-3 mb-6">
          <div className="flex items-start space-x-2">
            <MapPin className="h-4 w-4 text-gray-600 flex-shrink-0 mt-0.5" />
            <span className="text-sm text-gray-700">{provider.address}</span>
          </div>
          
          <div className="flex items-center space-x-2">
            <DollarSign className="h-4 w-4 text-gray-600" />
            <span className="text-sm text-gray-700">Consultation: {provider.fees}</span>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center space-x-3">
          <button
            onClick={() => handleCall(provider.phone)}
            className="flex-1 bg-primary-600 text-white px-4 py-3 rounded-lg font-medium hover:bg-primary-700 transition-colors flex items-center justify-center space-x-2"
          >
            <Phone className="h-4 w-4" />
            <span>Call Now</span>
          </button>
          
          <button
            onClick={handleDirections}
            className="px-4 py-3 border border-gray-300 rounded-lg text-gray-700 font-medium hover:bg-gray-50 transition-colors flex items-center space-x-2"
          >
            <ExternalLink className="h-4 w-4" />
            <span>Directions</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProviderCard;