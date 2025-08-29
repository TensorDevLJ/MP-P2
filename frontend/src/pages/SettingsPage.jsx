import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Settings, 
  User, 
  Shield, 
  Bell, 
  Globe, 
  Download,
  Trash2,
  Eye,
  EyeOff,
  Save,
  AlertTriangle,
  CheckCircle,
  Lock
} from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import PushNotifications from '../components/notifications/PushNotifications';

const SettingsPage = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('profile');
  const [showPassword, setShowPassword] = useState(false);
  const [saving, setSaving] = useState(false);
  const [deleteConfirm, setDeleteConfirm] = useState('');

  const [profileData, setProfileData] = useState({
    displayName: user?.display_name || '',
    email: user?.email || '',
    timezone: 'Asia/Kolkata',
    language: 'en',
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  });

  const [privacySettings, setPrivacySettings] = useState({
    dataRetention: '12months', // 6months, 12months, 24months, indefinite
    analyticsOptOut: false,
    shareAnonymousData: true,
    emailUpdates: true,
    researchParticipation: false,
  });

  const [notificationSettings, setNotificationSettings] = useState({
    pushEnabled: true,
    emailEnabled: true,
    smsEnabled: false,
    reminderTimes: {
      meditation: '09:00',
      checkin: '20:00',
      analysis: 'weekly',
    },
    crisisAlerts: true,
  });

  const tabs = [
    { id: 'profile', label: 'Profile', icon: User },
    { id: 'privacy', label: 'Privacy & Data', icon: Shield },
    { id: 'notifications', label: 'Notifications', icon: Bell },
    { id: 'preferences', label: 'Preferences', icon: Settings },
  ];

  const handleSaveProfile = async () => {
    setSaving(true);
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      console.log('Saving profile:', profileData);
      // Show success message
    } catch (error) {
      console.error('Error saving profile:', error);
    } finally {
      setSaving(false);
    }
  };

  const handleExportData = async () => {
    try {
      // Mock data export
      console.log('Exporting user data...');
      // In real app, would trigger server-side export and download
    } catch (error) {
      console.error('Error exporting data:', error);
    }
  };

  const handleDeleteAccount = async () => {
    if (deleteConfirm !== 'DELETE') return;
    
    try {
      console.log('Deleting account...');
      // In real app, would call delete API and logout
    } catch (error) {
      console.error('Error deleting account:', error);
    }
  };

  const renderProfileTab = () => (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-6">Personal Information</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Display Name
            </label>
            <input
              type="text"
              value={profileData.displayName}
              onChange={(e) => setProfileData(prev => ({ ...prev, displayName: e.target.value }))}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              placeholder="How should we call you?"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email Address
            </label>
            <input
              type="email"
              value={profileData.email}
              onChange={(e) => setProfileData(prev => ({ ...prev, email: e.target.value }))}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Timezone
            </label>
            <select
              value={profileData.timezone}
              onChange={(e) => setProfileData(prev => ({ ...prev, timezone: e.target.value }))}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="Asia/Kolkata">Asia/Kolkata (GMT+5:30)</option>
              <option value="America/New_York">America/New_York (GMT-5)</option>
              <option value="Europe/London">Europe/London (GMT+0)</option>
              <option value="Asia/Tokyo">Asia/Tokyo (GMT+9)</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Language
            </label>
            <select
              value={profileData.language}
              onChange={(e) => setProfileData(prev => ({ ...prev, language: e.target.value }))}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="en">English</option>
              <option value="hi">Hindi</option>
              <option value="es">Spanish</option>
              <option value="fr">French</option>
            </select>
          </div>
        </div>

        <div className="mt-6 pt-6 border-t border-gray-200">
          <h4 className="text-md font-semibold text-gray-900 mb-4">Change Password</h4>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Current Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={profileData.currentPassword}
                  onChange={(e) => setProfileData(prev => ({ ...prev, currentPassword: e.target.value }))}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 pr-12"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 px-3 flex items-center text-gray-400 hover:text-gray-600"
                >
                  {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                </button>
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                New Password
              </label>
              <input
                type={showPassword ? 'text' : 'password'}
                value={profileData.newPassword}
                onChange={(e) => setProfileData(prev => ({ ...prev, newPassword: e.target.value }))}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Confirm Password
              </label>
              <input
                type={showPassword ? 'text' : 'password'}
                value={profileData.confirmPassword}
                onChange={(e) => setProfileData(prev => ({ ...prev, confirmPassword: e.target.value }))}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
          </div>
        </div>

        <div className="mt-6 flex justify-end">
          <button
            onClick={handleSaveProfile}
            disabled={saving}
            className="bg-primary-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-primary-700 transition-colors flex items-center space-x-2"
          >
            {saving ? (
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            ) : (
              <Save className="h-4 w-4" />
            )}
            <span>{saving ? 'Saving...' : 'Save Changes'}</span>
          </button>
        </div>
      </div>
    </div>
  );

  const renderPrivacyTab = () => (
    <div className="space-y-6">
      {/* Data Control */}
      <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-6">Data Control</h3>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Data Retention Period
            </label>
            <select
              value={privacySettings.dataRetention}
              onChange={(e) => setPrivacySettings(prev => ({ ...prev, dataRetention: e.target.value }))}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="6months">6 Months</option>
              <option value="12months">12 Months</option>
              <option value="24months">24 Months</option>
              <option value="indefinite">Indefinite (until deletion)</option>
            </select>
            <p className="mt-1 text-sm text-gray-500">
              How long we keep your personal data and analysis results
            </p>
          </div>
          
          <div className="space-y-3">
            <label className="flex items-center space-x-3 cursor-pointer">
              <input
                type="checkbox"
                checked={privacySettings.analyticsOptOut}
                onChange={(e) => setPrivacySettings(prev => ({ ...prev, analyticsOptOut: e.target.checked }))}
                className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500 border-gray-300"
              />
              <div>
                <span className="text-sm font-medium text-gray-900">Opt out of analytics</span>
                <p className="text-xs text-gray-500">Disable usage analytics and performance tracking</p>
              </div>
            </label>
            
            <label className="flex items-center space-x-3 cursor-pointer">
              <input
                type="checkbox"
                checked={privacySettings.shareAnonymousData}
                onChange={(e) => setPrivacySettings(prev => ({ ...prev, shareAnonymousData: e.target.checked }))}
                className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500 border-gray-300"
              />
              <div>
                <span className="text-sm font-medium text-gray-900">Share anonymous research data</span>
                <p className="text-xs text-gray-500">Help improve mental health research (fully anonymized)</p>
              </div>
            </label>
            
            <label className="flex items-center space-x-3 cursor-pointer">
              <input
                type="checkbox"
                checked={privacySettings.researchParticipation}
                onChange={(e) => setPrivacySettings(prev => ({ ...prev, researchParticipation: e.target.checked }))}
                className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500 border-gray-300"
              />
              <div>
                <span className="text-sm font-medium text-gray-900">Participate in research studies</span>
                <p className="text-xs text-gray-500">Receive invitations for voluntary research participation</p>
              </div>
            </label>
          </div>
        </div>
      </div>

      {/* Data Export & Delete */}
      <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-6">Data Management</h3>
        
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div>
              <h4 className="font-medium text-gray-900">Export Your Data</h4>
              <p className="text-sm text-gray-600">Download all your personal data and analysis results</p>
            </div>
            <button
              onClick={handleExportData}
              className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors flex items-center space-x-2"
            >
              <Download className="h-4 w-4" />
              <span>Export</span>
            </button>
          </div>
          
          <div className="p-4 bg-error-50 border border-error-200 rounded-lg">
            <h4 className="font-medium text-error-900 mb-2">Delete Account</h4>
            <p className="text-sm text-error-700 mb-4">
              Permanently delete your account and all associated data. This action cannot be undone.
            </p>
            
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-error-700 mb-2">
                  Type "DELETE" to confirm
                </label>
                <input
                  type="text"
                  value={deleteConfirm}
                  onChange={(e) => setDeleteConfirm(e.target.value)}
                  className="w-full px-4 py-3 border border-error-300 rounded-lg focus:ring-2 focus:ring-error-500 focus:border-error-500"
                  placeholder="Type DELETE to confirm"
                />
              </div>
              
              <button
                onClick={handleDeleteAccount}
                disabled={deleteConfirm !== 'DELETE'}
                className="bg-error-600 text-white px-4 py-2 rounded-lg hover:bg-error-700 transition-colors flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Trash2 className="h-4 w-4" />
                <span>Delete Account</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderNotificationsTab = () => (
    <div className="space-y-6">
      <PushNotifications />
      
      <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-6">Notification Preferences</h3>
        
        <div className="space-y-6">
          <div>
            <h4 className="font-medium text-gray-900 mb-3">Delivery Methods</h4>
            <div className="space-y-3">
              <label className="flex items-center justify-between cursor-pointer">
                <div>
                  <span className="text-sm font-medium text-gray-900">Email Notifications</span>
                  <p className="text-xs text-gray-500">Receive updates via email</p>
                </div>
                <input
                  type="checkbox"
                  checked={notificationSettings.emailEnabled}
                  onChange={(e) => setNotificationSettings(prev => ({ ...prev, emailEnabled: e.target.checked }))}
                  className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500 border-gray-300"
                />
              </label>
              
              <label className="flex items-center justify-between cursor-pointer">
                <div>
                  <span className="text-sm font-medium text-gray-900">SMS Notifications</span>
                  <p className="text-xs text-gray-500">Critical alerts via text message</p>
                </div>
                <input
                  type="checkbox"
                  checked={notificationSettings.smsEnabled}
                  onChange={(e) => setNotificationSettings(prev => ({ ...prev, smsEnabled: e.target.checked }))}
                  className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500 border-gray-300"
                />
              </label>
            </div>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-900 mb-3">Reminder Schedule</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Meditation Reminder
                </label>
                <input
                  type="time"
                  value={notificationSettings.reminderTimes.meditation}
                  onChange={(e) => setNotificationSettings(prev => ({
                    ...prev,
                    reminderTimes: { ...prev.reminderTimes, meditation: e.target.value }
                  }))}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Evening Check-in
                </label>
                <input
                  type="time"
                  value={notificationSettings.reminderTimes.checkin}
                  onChange={(e) => setNotificationSettings(prev => ({
                    ...prev,
                    reminderTimes: { ...prev.reminderTimes, checkin: e.target.value }
                  }))}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                />
              </div>
            </div>
          </div>
          
          <div className="pt-4 border-t border-gray-200">
            <label className="flex items-center space-x-3 cursor-pointer">
              <input
                type="checkbox"
                checked={notificationSettings.crisisAlerts}
                onChange={(e) => setNotificationSettings(prev => ({ ...prev, crisisAlerts: e.target.checked }))}
                className="w-4 h-4 text-error-600 rounded focus:ring-error-500 border-gray-300"
              />
              <div>
                <span className="text-sm font-medium text-gray-900">Crisis Support Alerts</span>
                <p className="text-xs text-gray-500">Receive immediate support resources when high-risk patterns are detected</p>
              </div>
            </label>
          </div>
        </div>
      </div>
    </div>
  );

  // const renderPrivacyTab = () => (
  //   <div className="space-y-6">
  //     {/* Privacy Settings */}
  //     <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
  //       <h3 className="text-lg font-semibold text-gray-900 mb-6">Privacy Settings</h3>
        
  //       <div className="space-y-4">
  //         <label className="flex items-center justify-between cursor-pointer">
  //           <div>
  //             <span className="text-sm font-medium text-gray-900">Opt out of analytics</span>
  //             <p className="text-xs text-gray-500">Disable usage analytics and performance tracking</p>
  //           </div>
  //           <input
  //             type="checkbox"
  //             checked={privacySettings.analyticsOptOut}
  //             onChange={(e) => setPrivacySettings(prev => ({ ...prev, analyticsOptOut: e.target.checked }))}
  //             className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500 border-gray-300"
  //           />
  //         </label>
          
  //         <label className="flex items-center justify-between cursor-pointer">
  //           <div>
  //             <span className="text-sm font-medium text-gray-900">Share anonymous research data</span>
  //             <p className="text-xs text-gray-500">Help improve mental health research (fully anonymized)</p>
  //           </div>
  //           <input
  //             type="checkbox"
  //             checked={privacySettings.shareAnonymousData}
  //             onChange={(e) => setPrivacySettings(prev => ({ ...prev, shareAnonymousData: e.target.checked }))}
  //             className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500 border-gray-300"
  //           />
  //         </label>
          
  //         <label className="flex items-center justify-between cursor-pointer">
  //           <div>
  //             <span className="text-sm font-medium text-gray-900">Email updates</span>
  //             <p className="text-xs text-gray-500">Receive newsletters and platform updates</p>
  //           </div>
  //           <input
  //             type="checkbox"
  //             checked={privacySettings.emailUpdates}
  //             onChange={(e) => setPrivacySettings(prev => ({ ...prev, emailUpdates: e.target.checked }))}
  //             className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500 border-gray-300"
  //           />
  //         </label>
  //       </div>
  //     </div>

  //     {/* Data Export & Delete */}
  //     <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
  //       <h3 className="text-lg font-semibold text-gray-900 mb-6">Data Management</h3>
        
  //       <div className="space-y-4">
  //         <div className="flex items-center justify-between p-4 bg-primary-50 border border-primary-200 rounded-lg">
  //           <div>
  //             <h4 className="font-medium text-primary-900">Export Your Data</h4>
  //             <p className="text-sm text-primary-700">Download all your personal data and analysis results</p>
  //           </div>
  //           <button
  //             onClick={handleExportData}
  //             className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors flex items-center space-x-2"
  //           >
  //             <Download className="h-4 w-4" />
  //             <span>Export</span>
  //           </button>
  //         </div>
          
  //         <div className="p-4 bg-error-50 border border-error-200 rounded-lg">
  //           <h4 className="font-medium text-error-900 mb-2">Delete Account</h4>
  //           <p className="text-sm text-error-700 mb-4">
  //             Permanently delete your account and all associated data. This action cannot be undone.
  //           </p>
            
  //           <div className="space-y-3">
  //             <div>
  //               <label className="block text-sm font-medium text-error-700 mb-2">
  //                 Type "DELETE" to confirm
  //               </label>
  //               <input
  //                 type="text"
  //                 value={deleteConfirm}
  //                 onChange={(e) => setDeleteConfirm(e.target.value)}
  //                 className="w-full px-4 py-3 border border-error-300 rounded-lg focus:ring-2 focus:ring-error-500 focus:border-error-500"
  //                 placeholder="Type DELETE to confirm"
  //               />
  //             </div>
              
  //             <button
  //               onClick={handleDeleteAccount}
  //               disabled={deleteConfirm !== 'DELETE'}
  //               className="bg-error-600 text-white px-4 py-2 rounded-lg hover:bg-error-700 transition-colors flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
  //             >
  //               <Trash2 className="h-4 w-4" />
  //               <span>Delete Account</span>
  //             </button>
  //           </div>
  //         </div>
  //       </div>
  //     </div>
  //   </div>
  // );

  const renderPreferencesTab = () => (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-6">Display Preferences</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Date Format
            </label>
            <select className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500">
              <option>MM/DD/YYYY (US)</option>
              <option>DD/MM/YYYY (European)</option>
              <option>YYYY-MM-DD (ISO)</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Time Format
            </label>
            <select className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500">
              <option>12-hour (AM/PM)</option>
              <option>24-hour</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Theme
            </label>
            <select className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500">
              <option>Light</option>
              <option>Dark</option>
              <option>System</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Measurement Units
            </label>
            <select className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500">
              <option>Metric (μV, Hz)</option>
              <option>Imperial</option>
            </select>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-6">Analysis Preferences</h3>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Default Analysis Length
            </label>
            <select className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500">
              <option>2 minutes (quick scan)</option>
              <option>5 minutes (standard)</option>
              <option>10 minutes (detailed)</option>
              <option>Full recording</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Confidence Threshold
            </label>
            <input
              type="range"
              min="50"
              max="95"
              defaultValue="70"
              className="w-full"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>50% (More sensitive)</span>
              <span>95% (More conservative)</span>
            </div>
          </div>
          
          <label className="flex items-center space-x-3 cursor-pointer">
            <input
              type="checkbox"
              defaultChecked={true}
              className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500 border-gray-300"
            />
            <div>
              <span className="text-sm font-medium text-gray-900">Auto-save analysis results</span>
              <p className="text-xs text-gray-500">Automatically save completed analyses to your history</p>
            </div>
          </label>
        </div>
      </div>
    </div>
  );

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Page Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="bg-white rounded-xl shadow-lg p-6 border border-gray-200"
      >
        <div className="flex items-center space-x-4">
          <div className="p-3 bg-gray-100 rounded-xl">
            <Settings className="h-8 w-8 text-gray-600" />
          </div>
          <div>
            <h1 className="text-2xl lg:text-3xl font-bold text-gray-900">Settings</h1>
            <p className="text-gray-600">
              Manage your account, privacy, and preferences
            </p>
          </div>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Sidebar Navigation */}
        <div className="lg:col-span-1">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden"
          >
            <nav className="space-y-1 p-2">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-left font-medium transition-colors ${
                      activeTab === tab.id
                        ? 'bg-primary-100 text-primary-700'
                        : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                    }`}
                  >
                    <Icon className="h-5 w-5" />
                    <span>{tab.label}</span>
                  </button>
                );
              })}
            </nav>
          </motion.div>
        </div>

        {/* Content Area */}
        <div className="lg:col-span-3">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
          >
            {activeTab === 'profile' && renderProfileTab()}
            {activeTab === 'privacy' && renderPrivacyTab()}
            {activeTab === 'notifications' && renderNotificationsTab()}
            {activeTab === 'preferences' && renderPreferencesTab()}
          </motion.div>
        </div>
      </div>

      {/* Security Notice */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.3 }}
        className="bg-success-50 border border-success-200 rounded-lg p-4"
      >
        <div className="flex items-start space-x-3">
          <Lock className="h-5 w-5 text-success-600 flex-shrink-0 mt-0.5" />
          <div className="text-sm text-success-700">
            <p className="font-medium mb-1">Your Data is Secure</p>
            <p>
              All personal data is encrypted using AES-256 encryption. EEG analysis happens on secure servers, 
              and we never store raw brainwave data longer than necessary for processing.
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default SettingsPage;