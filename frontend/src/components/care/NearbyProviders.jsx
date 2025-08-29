import React, { useState, useEffect } from 'react';
import { GoogleMap, LoadScript, Marker, InfoWindow } from '@react-google-maps/api';
import { MapPin, Filter, Phone, Star, Clock, ExternalLink } from 'lucide-react';
import ProviderCard from './ProviderCard';
import LoadingSpinner from '../common/LoadingSpinner';

const mapContainerStyle = {
  width: '100%',
  height: '400px',
};

const defaultCenter = {
  lat: 28.6139, // New Delhi coordinates as default
  lng: 77.2090,
};

const NearbyProviders = () => {
  const [userLocation, setUserLocation] = useState(null);
  const [selectedProvider, setSelectedProvider] = useState(null);
  const [providers, setProviders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({
    type: 'all', // all, psychiatrist, psychologist, counselor
    radius: 10, // km
    rating: 0,
    openNow: false,
  });
  const [viewMode, setViewMode] = useState('grid'); // grid, map

  // Mock providers data
  const mockProviders = [
    {
      id: '1',
      name: 'Dr. Priya Sharma',
      type: 'Psychiatrist',
      rating: 4.8,
      reviewCount: 124,
      distance: 2.3,
      address: 'Connaught Place, New Delhi, 110001',
      phone: '+91-98765-43210',
      openNow: true,
      nextAvailable: '2025-01-15T10:00:00Z',
      specialties: ['Depression', 'Anxiety', 'Bipolar Disorder'],
      languages: ['Hindi', 'English'],
      fees: '₹1,500 - ₹2,000',
      coordinates: { lat: 28.6304, lng: 77.2177 },
    },
    {
      id: '2',
      name: 'MindWell Psychology Center',
      type: 'Psychology Clinic',
      rating: 4.6,
      reviewCount: 89,
      distance: 4.1,
      address: 'Karol Bagh, New Delhi, 110005',
      phone: '+91-98765-43211',
      openNow: false,
      nextAvailable: '2025-01-16T09:00:00Z',
      specialties: ['Cognitive Therapy', 'Family Counseling', 'Stress Management'],
      languages: ['Hindi', 'English', 'Punjabi'],
      fees: '₹800 - ₹1,200',
      coordinates: { lat: 28.6507, lng: 77.1909 },
    },
    {
      id: '3',
      name: 'Dr. Rajesh Kumar',
      type: 'Clinical Psychologist',
      rating: 4.9,
      reviewCount: 156,
      distance: 3.7,
      address: 'Vasant Kunj, New Delhi, 110070',
      phone: '+91-98765-43212',
      openNow: true,
      nextAvailable: '2025-01-15T14:30:00Z',
      specialties: ['PTSD', 'Depression', 'Addiction Counseling'],
      languages: ['Hindi', 'English'],
      fees: '₹1,200 - ₹1,800',
      coordinates: { lat: 28.5244, lng: 77.1580 },
    },
  ];

  useEffect(() => {
    // Get user's location
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setUserLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          });
        },
        (error) => {
          console.error('Error getting location:', error);
          setUserLocation(defaultCenter); // Fallback to default
        }
      );
    } else {
      setUserLocation(defaultCenter);
    }
  }, []);

  useEffect(() => {
    if (userLocation) {
      setLoading(true);
      // Simulate API call delay
      setTimeout(() => {
        setProviders(mockProviders);
        setLoading(false);
      }, 1000);
    }
  }, [userLocation, filters]);

  const filteredProviders = providers.filter(provider => {
    if (filters.type !== 'all' && !provider.type.toLowerCase().includes(filters.type)) {
      return false;
    }
    if (provider.distance > filters.radius) {
      return false;
    }
    if (provider.rating < filters.rating) {
      return false;
    }
    if (filters.openNow && !provider.openNow) {
      return false;
    }
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-success-100 rounded-xl">
              <MapPin className="h-8 w-8 text-success-600" />
            </div>
            <div>
              <h1 className="text-2xl lg:text-3xl font-bold text-gray-900">Find Mental Health Care</h1>
              <p className="text-gray-600">
                Locate qualified mental health professionals in your area
              </p>
            </div>
          </div>
          
          <div className="hidden lg:flex items-center space-x-3">
            <button
              onClick={() => setViewMode('grid')}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                viewMode === 'grid'
                  ? 'bg-primary-100 text-primary-700'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              List View
            </button>
            <button
              onClick={() => setViewMode('map')}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                viewMode === 'map'
                  ? 'bg-primary-100 text-primary-700'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Map View
            </button>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
        <div className="flex items-center space-x-3 mb-4">
          <Filter className="h-5 w-5 text-gray-600" />
          <span className="text-lg font-semibold text-gray-900">Filters</span>
        </div>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Provider Type</label>
            <select
              value={filters.type}
              onChange={(e) => setFilters(prev => ({ ...prev, type: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="all">All Types</option>
              <option value="psychiatrist">Psychiatrist</option>
              <option value="psychologist">Psychologist</option>
              <option value="counselor">Counselor</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Distance (km)</label>
            <select
              value={filters.radius}
              onChange={(e) => setFilters(prev => ({ ...prev, radius: Number(e.target.value) }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              <option value={5}>Within 5 km</option>
              <option value={10}>Within 10 km</option>
              <option value={25}>Within 25 km</option>
              <option value={50}>Within 50 km</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Min. Rating</label>
            <select
              value={filters.rating}
              onChange={(e) => setFilters(prev => ({ ...prev, rating: Number(e.target.value) }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              <option value={0}>Any Rating</option>
              <option value={4}>4+ Stars</option>
              <option value={4.5}>4.5+ Stars</option>
            </select>
          </div>
          
          <div className="flex items-end">
            <label className="flex items-center space-x-2 cursor-pointer">
              <input
                type="checkbox"
                checked={filters.openNow}
                onChange={(e) => setFilters(prev => ({ ...prev, openNow: e.target.checked }))}
                className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500 border-gray-300"
              />
              <span className="text-sm font-medium text-gray-700">Open Now</span>
            </label>
          </div>
        </div>
      </div>

      {/* Results */}
      {loading ? (
        <div className="bg-white rounded-xl shadow-lg p-12 border border-gray-200 text-center">
          <LoadingSpinner size="large" message="Finding providers near you..." />
        </div>
      ) : (
        <>
          {/* Results Header */}
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-gray-900">
              {filteredProviders.length} providers found
            </h2>
            <p className="text-sm text-gray-600">
              Showing results within {filters.radius} km
            </p>
          </div>

          {viewMode === 'grid' ? (
            /* Grid View */
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {filteredProviders.map((provider) => (
                <ProviderCard
                  key={provider.id}
                  provider={provider}
                  onSelect={() => setSelectedProvider(provider)}
                />
              ))}
            </div>
          ) : (
            /* Map View */
            <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
              <LoadScript googleMapsApiKey="YOUR_GOOGLE_MAPS_API_KEY">
                <GoogleMap
                  mapContainerStyle={mapContainerStyle}
                  center={userLocation || defaultCenter}
                  zoom={12}
                >
                  {/* User location marker */}
                  {userLocation && (
                    <Marker
                      position={userLocation}
                      icon={{
                        url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(`
                          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <circle cx="12" cy="12" r="8" fill="#3B82F6" stroke="white" stroke-width="2"/>
                          </svg>
                        `),
                      }}
                    />
                  )}

                  {/* Provider markers */}
                  {filteredProviders.map((provider) => (
                    <Marker
                      key={provider.id}
                      position={provider.coordinates}
                      onClick={() => setSelectedProvider(provider)}
                    >
                      {selectedProvider?.id === provider.id && (
                        <InfoWindow onCloseClick={() => setSelectedProvider(null)}>
                          <div className="p-2 max-w-xs">
                            <h3 className="font-semibold text-gray-900 mb-1">{provider.name}</h3>
                            <p className="text-sm text-gray-600 mb-2">{provider.type}</p>
                            <div className="flex items-center space-x-2 text-sm">
                              <Star className="h-4 w-4 text-warning-500" />
                              <span>{provider.rating}</span>
                              <span className="text-gray-500">({provider.reviewCount})</span>
                            </div>
                          </div>
                        </InfoWindow>
                      )}
                    </Marker>
                  ))}
                </GoogleMap>
              </LoadScript>
            </div>
          )}
        </>
      )}

      {filteredProviders.length === 0 && !loading && (
        <div className="bg-white rounded-xl shadow-lg p-12 border border-gray-200 text-center">
          <MapPin className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No providers found</h3>
          <p className="text-gray-600 mb-4">
            Try adjusting your filters or expanding the search radius
          </p>
          <button
            onClick={() => setFilters(prev => ({ ...prev, radius: prev.radius + 10 }))}
            className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition-colors"
          >
            Expand Search Area
          </button>
        </div>
      )}
    </div>
  );
};

export default NearbyProviders;