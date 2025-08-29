import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider } from './hooks/useAuth';
import { NotificationProvider } from './hooks/useNotifications';
import { ROUTES } from './utils/constants';

// Layout Components
import Header from './components/common/Header';
import Sidebar from './components/common/Sidebar';
import ErrorBoundary from './components/common/ErrorBoundary';
import ProtectedRoute from './components/auth/ProtectedRoute';
import NotificationCenter from './components/notifications/NotificationCenter';

// Page Components
import HomePage from './pages/HomePage';
import Login from './components/auth/Login';
import SignUp from './components/auth/SignUp';
import Dashboard from './pages/Dashboard';
import AnalyzePage from './pages/AnalyzePage';
import AssistantPage from './pages/AssistantPage';
import CarePage from './pages/CarePage';
import TrendsPage from './pages/TrendsPage';
import SettingsPage from './pages/SettingsPage';
import HowToUsePage from './pages/HowToUsePage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      refetchOnWindowFocus: false,
    },
  },
});

const AppLayout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [notificationCenterOpen, setNotificationCenterOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50">
      <Header 
        onMenuToggle={() => setSidebarOpen(!sidebarOpen)}
        onNotificationToggle={() => setNotificationCenterOpen(!notificationCenterOpen)}
      />
      <div className="flex">
        <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
        <main className="flex-1 lg:ml-0 overflow-hidden">
          <div className="p-4 lg:p-6">
            {children}
          </div>
        </main>
      </div>
      <NotificationCenter 
        isOpen={notificationCenterOpen}
        onClose={() => setNotificationCenterOpen(false)}
      />
    </div>
  );
};

function App() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          <NotificationProvider>
            <Router>
              <Routes>
                {/* Public Routes */}
                <Route path={ROUTES.HOME} element={<HomePage />} />
                <Route path={ROUTES.LOGIN} element={<Login />} />
                <Route path={ROUTES.SIGNUP} element={<SignUp />} />
                
                {/* Protected Routes */}
                <Route path={ROUTES.DASHBOARD} element={
                  <ProtectedRoute>
                    <AppLayout>
                      <Dashboard />
                    </AppLayout>
                  </ProtectedRoute>
                } />
                
                <Route path={ROUTES.ANALYZE} element={
                  <ProtectedRoute>
                    <AppLayout>
                      <AnalyzePage />
                    </AppLayout>
                  </ProtectedRoute>
                } />
                
                <Route path={ROUTES.ASSISTANT} element={
                  <ProtectedRoute>
                    <AppLayout>
                      <AssistantPage />
                    </AppLayout>
                  </ProtectedRoute>
                } />
                
                <Route path={ROUTES.CARE} element={
                  <ProtectedRoute>
                    <AppLayout>
                      <CarePage />
                    </AppLayout>
                  </ProtectedRoute>
                } />
                
                <Route path={ROUTES.TRENDS} element={
                  <ProtectedRoute>
                    <AppLayout>
                      <TrendsPage />
                    </AppLayout>
                  </ProtectedRoute>
                } />
                
                <Route path={ROUTES.SETTINGS} element={
                  <ProtectedRoute>
                    <AppLayout>
                      <SettingsPage />
                    </AppLayout>
                  </ProtectedRoute>
                } />
                
                <Route path={ROUTES.HOW_TO_USE} element={
                  <ProtectedRoute>
                    <AppLayout>
                      <HowToUsePage />
                    </AppLayout>
                  </ProtectedRoute>
                } />
                
                {/* Redirect root to dashboard for authenticated users */}
                <Route path="/" element={<Navigate to={ROUTES.HOME} replace />} />
              </Routes>
            </Router>
          </NotificationProvider>
        </AuthProvider>
      </QueryClientProvider>
    </ErrorBoundary>
  );
}

export default App;