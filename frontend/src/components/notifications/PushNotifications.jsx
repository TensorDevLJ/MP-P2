import React, { useState, useEffect } from 'react';
import { Bell, BellOff, Check, AlertTriangle } from 'lucide-react';

const PushNotifications = () => {
  const [isSupported, setIsSupported] = useState(false);
  const [permission, setPermission] = useState('default');
  const [isSubscribed, setIsSubscribed] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Check if push notifications are supported
    setIsSupported('Notification' in window && 'serviceWorker' in navigator);
    setPermission(Notification.permission);
    
    // Check if already subscribed
    checkSubscriptionStatus();
  }, []);

  const checkSubscriptionStatus = async () => {
    if (!isSupported) return;

    try {
      const registration = await navigator.serviceWorker.ready;
      const subscription = await registration.pushManager.getSubscription();
      setIsSubscribed(!!subscription);
    } catch (error) {
      console.error('Error checking subscription:', error);
    }
  };

  const subscribeToPush = async () => {
    if (!isSupported) return;

    setLoading(true);
    
    try {
      // Request permission
      const permission = await Notification.requestPermission();
      setPermission(permission);

      if (permission === 'granted') {
        // Register service worker
        const registration = await navigator.serviceWorker.register('/service-worker.js');
        
        // Subscribe to push notifications
        const subscription = await registration.pushManager.subscribe({
          userVisibleOnly: true,
          applicationServerKey: urlBase64ToUint8Array(
            process.env.REACT_APP_VAPID_PUBLIC_KEY || 'demo-key'
          ),
        });

        // Send subscription to server
        await fetch('/api/notify/subscribe', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
          },
          body: JSON.stringify(subscription),
        });

        setIsSubscribed(true);
        
        // Show test notification
        showTestNotification();
      }
    } catch (error) {
      console.error('Error subscribing to push notifications:', error);
    } finally {
      setLoading(false);
    }
  };

  const unsubscribeFromPush = async () => {
    if (!isSupported) return;

    setLoading(true);
    
    try {
      const registration = await navigator.serviceWorker.ready;
      const subscription = await registration.pushManager.getSubscription();
      
      if (subscription) {
        await subscription.unsubscribe();
        
        // Notify server
        await fetch('/api/notify/unsubscribe', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
          },
        });
      }
      
      setIsSubscribed(false);
    } catch (error) {
      console.error('Error unsubscribing from push notifications:', error);
    } finally {
      setLoading(false);
    }
  };

  const showTestNotification = () => {
    if (Notification.permission === 'granted') {
      new Notification('EEG Health Assistant', {
        body: 'Push notifications are now enabled! We\'ll keep you updated on your wellness journey.',
        icon: '/brain.svg',
        badge: '/brain.svg',
      });
    }
  };

  // Helper function to convert VAPID key
  const urlBase64ToUint8Array = (base64String) => {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);
    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
  };

  if (!isSupported) {
    return (
      <div className="bg-warning-50 border border-warning-200 rounded-lg p-4">
        <div className="flex items-center space-x-2">
          <AlertTriangle className="h-5 w-5 text-warning-600" />
          <div>
            <p className="font-medium text-warning-800">Push Notifications Not Supported</p>
            <p className="text-sm text-warning-700">
              Your browser doesn't support push notifications. Please use a modern browser for the best experience.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
      <div className="flex items-center space-x-3 mb-6">
        <div className={`p-2 rounded-lg ${
          isSubscribed ? 'bg-success-100' : 'bg-gray-100'
        }`}>
          {isSubscribed ? (
            <Bell className="h-5 w-5 text-success-600" />
          ) : (
            <BellOff className="h-5 w-5 text-gray-600" />
          )}
        </div>
        <div>
          <h3 className="text-lg font-semibold text-gray-900">Push Notifications</h3>
          <p className="text-sm text-gray-500">
            {isSubscribed ? 'You\'ll receive wellness reminders and updates' : 'Enable notifications for wellness reminders'}
          </p>
        </div>
      </div>

      <div className="space-y-4">
        {permission === 'denied' ? (
          <div className="bg-error-50 border border-error-200 rounded-lg p-4">
            <div className="flex items-center space-x-2">
              <AlertTriangle className="h-5 w-5 text-error-600" />
              <div>
                <p className="font-medium text-error-800">Notifications Blocked</p>
                <p className="text-sm text-error-700">
                  You've blocked notifications. To enable them, please allow notifications in your browser settings.
                </p>
              </div>
            </div>
          </div>
        ) : isSubscribed ? (
          <div className="bg-success-50 border border-success-200 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Check className="h-5 w-5 text-success-600" />
                <div>
                  <p className="font-medium text-success-800">Notifications Enabled</p>
                  <p className="text-sm text-success-700">
                    You'll receive wellness reminders and important updates
                  </p>
                </div>
              </div>
              <button
                onClick={unsubscribeFromPush}
                disabled={loading}
                className="text-success-600 hover:text-success-700 text-sm font-medium"
              >
                {loading ? 'Disabling...' : 'Disable'}
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="bg-primary-50 border border-primary-200 rounded-lg p-4">
              <h4 className="font-medium text-primary-800 mb-2">What you'll receive:</h4>
              <ul className="text-sm text-primary-700 space-y-1">
                <li>• Meditation and wellness reminders</li>
                <li>• Analysis completion notifications</li>
                <li>• Progress milestone celebrations</li>
                <li>• Important health insights</li>
              </ul>
            </div>

            <button
              onClick={subscribeToPush}
              disabled={loading}
              className="w-full bg-primary-600 text-white px-4 py-3 rounded-lg font-medium hover:bg-primary-700 transition-colors flex items-center justify-center space-x-2"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>Enabling...</span>
                </>
              ) : (
                <>
                  <Bell className="h-4 w-4" />
                  <span>Enable Notifications</span>
                </>
              )}
            </button>
          </div>
        )}

        {/* Test Notification Button */}
        {isSubscribed && (
          <div className="pt-4 border-t border-gray-200">
            <button
              onClick={showTestNotification}
              className="w-full bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors text-sm"
            >
              Send Test Notification
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default PushNotifications;