import React from 'react';
import { Brain, TrendingUp, Calendar, Share2, Save, Clock, Heart, Zap } from 'lucide-react';
import { MENTAL_HEALTH_STATES } from '../../utils/constants';
import { formatDate, formatConfidenceScore, getStateColorClasses } from '../../utils/helpers';

const StateCard = ({ 
  state = 'STABLE', 
  confidence = 0.85, 
  lastUpdated = new Date(),
  emotions = { primary: 'calm', secondary: 'focused' },
  textSentiment = null,
  recommendations = [],
  onSaveSession,
  onScheduleFollowup,
  onShare 
}) => {
  const stateInfo = MENTAL_HEALTH_STATES[state];
  const colorClasses = getStateColorClasses(stateInfo.color);

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
      <div className="flex items-start justify-between mb-6">
        <div className="flex items-center space-x-3">
          <div className="p-3 bg-primary-100 rounded-lg">
            <Brain className="h-6 w-6 text-primary-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Current Mental State</h3>
            <p className="text-sm text-gray-500">Based on recent EEG & text analysis</p>
          </div>
        </div>
        <div className="text-right">
          <p className="text-xs text-gray-500">Last updated</p>
          <p className="text-sm font-medium text-gray-700 flex items-center space-x-1">
            <Clock className="h-3 w-3" />
            <span>{formatDate(lastUpdated, 'MMM dd, HH:mm')}</span>
          </p>
        </div>
      </div>

      {/* State Display */}
      <div className={`p-4 rounded-lg border-2 mb-6 ${colorClasses}`}>
        <div className="flex items-center justify-between mb-3">
          <div>
            <div className="text-2xl font-bold mb-1">{stateInfo.label}</div>
            <div className="flex items-center space-x-4 text-sm opacity-90">
              <div className="flex items-center space-x-1">
                <Heart className="h-4 w-4" />
                <span className="capitalize">{emotions.primary}</span>
              </div>
              {emotions.secondary && (
                <div className="flex items-center space-x-1">
                  <Zap className="h-4 w-4" />
                  <span className="capitalize">{emotions.secondary}</span>
                </div>
              )}
              {textSentiment && (
                <div className="text-xs bg-white bg-opacity-50 px-2 py-1 rounded">
                  Text: {textSentiment.replace('_', ' ')}
                </div>
              )}
            </div>
          </div>
          <div className="text-right">
            <p className="text-sm opacity-75">Confidence</p>
            <p className="text-3xl font-bold">{formatConfidenceScore(confidence)}%</p>
          </div>
        </div>
        <p className="text-sm opacity-90">{stateInfo.description}</p>
      </div>

      {/* Recommendations */}
      {recommendations && recommendations.length > 0 && (
        <div className="mb-6">
          <h4 className="text-sm font-semibold text-gray-700 mb-3 flex items-center space-x-2">
            <TrendingUp className="h-4 w-4" />
            <span>Recommended Actions</span>
          </h4>
          <div className="space-y-2">
            {recommendations.slice(0, 3).map((rec, index) => {
              const Icon = rec.icon || Brain;
              return (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors group cursor-pointer">
                  <div className="flex items-center space-x-3">
                    <Icon className="h-4 w-4 text-gray-600" />
                    <div>
                      <span className="text-sm font-medium text-gray-700 group-hover:text-gray-900">
                        {rec.title}
                      </span>
                      <p className="text-xs text-gray-500">{rec.description}</p>
                    </div>
                  </div>
                  <span className="text-xs text-gray-500 bg-white px-2 py-1 rounded">
                    {rec.duration}min
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex items-center space-x-3">
        <button
          onClick={onSaveSession}
          className="flex-1 bg-primary-600 text-white px-3 py-2 rounded-lg text-sm font-medium hover:bg-primary-700 transition-colors flex items-center justify-center space-x-2"
        >
          <Save className="h-4 w-4" />
          <span>Save Session</span>
        </button>
        
        <button
          onClick={onShare}
          className="p-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200 transition-colors"
          title="Share Results"
        >
          <Share2 className="h-4 w-4" />
        </button>
        
        <button
          onClick={onScheduleFollowup}
          className="p-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200 transition-colors"
          title="Schedule Follow-up"
        >
          <Calendar className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
};

export default StateCard;