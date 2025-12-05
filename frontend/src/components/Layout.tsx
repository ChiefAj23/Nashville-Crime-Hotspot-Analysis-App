import { ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useStore } from '../store/useStore';
import {
  Map,
  Navigation,
  BarChart3,
  Shield,
  TrendingUp,
  Settings,
  Moon,
  Sun,
  AlertCircle
} from 'lucide-react';
import { motion } from 'framer-motion';

interface LayoutProps {
  children: ReactNode;
}

const navigation = [
  { name: 'Map View', path: '/', icon: Map },
  { name: 'Route Planner', path: '/route-planner', icon: Navigation },
  { name: 'Statistics', path: '/statistics', icon: BarChart3 },
  { name: 'Safety Calculator', path: '/safety-calculator', icon: Shield },
  { name: 'Trends', path: '/trends', icon: TrendingUp },
  { name: 'Settings', path: '/settings', icon: Settings },
];

export default function Layout({ children }: LayoutProps) {
  const location = useLocation();
  const { darkMode, toggleDarkMode, error } = useStore();

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Navigation Sidebar */}
      <aside className="fixed left-0 top-0 h-full w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 z-50">
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-600 to-primary-400 bg-clip-text text-transparent">
              🗺️ Nashville Safe
            </h1>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              Tourist Safety Guide
            </p>
            <p className="text-xs text-gray-400 dark:text-gray-500 mt-2 pt-2 border-t border-gray-200 dark:border-gray-700">
              Developed by <span className="font-semibold text-primary-600 dark:text-primary-400">Abhijeet Solanki</span>
            </p>
          </div>

          {/* Navigation Links */}
          <nav className="flex-1 overflow-y-auto p-4 space-y-2">
            {navigation.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;

              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                    isActive
                      ? 'bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300 font-semibold'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </nav>

          {/* Dark Mode Toggle */}
          <div className="p-4 border-t border-gray-200 dark:border-gray-700">
            <button
              onClick={toggleDarkMode}
              className="w-full flex items-center justify-center space-x-2 px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors duration-200"
            >
              {darkMode ? (
                <>
                  <Sun className="w-5 h-5" />
                  <span>Light Mode</span>
                </>
              ) : (
                <>
                  <Moon className="w-5 h-5" />
                  <span>Dark Mode</span>
                </>
              )}
            </button>
          </div>

          {/* Developer Attribution */}
          <div className="p-4 border-t border-gray-200 dark:border-gray-700">
            <p className="text-xs text-center text-gray-500 dark:text-gray-400">
              Developed by{' '}
              <span className="font-semibold text-primary-600 dark:text-primary-400">
                Abhijeet Solanki
              </span>
            </p>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="ml-64">
        {/* Error Banner */}
        {error && (
          <motion.div
            initial={{ y: -50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            className="bg-danger-100 dark:bg-danger-900 border-b border-danger-200 dark:border-danger-800"
          >
            <div className="max-w-7xl mx-auto px-6 py-3 flex items-center space-x-3">
              <AlertCircle className="w-5 h-5 text-danger-600 dark:text-danger-400" />
              <p className="text-danger-800 dark:text-danger-200">{error}</p>
            </div>
          </motion.div>
        )}

        {/* Page Content */}
        <div className="p-6 pb-20">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            {children}
          </motion.div>
        </div>

        {/* Footer */}
        <footer className="fixed bottom-0 left-64 right-0 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 py-3 px-6 z-40">
          <div className="max-w-7xl mx-auto flex items-center justify-between">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              © {new Date().getFullYear()} Nashville Safe Tourist Guide
            </p>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Developed by{' '}
              <span className="font-semibold text-primary-600 dark:text-primary-400">
                Abhijeet Solanki
              </span>
            </p>
          </div>
        </footer>
      </main>
    </div>
  );
}

