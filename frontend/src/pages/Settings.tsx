import { Phone, Heart, Settings as SettingsIcon } from 'lucide-react';
import { motion } from 'framer-motion';

export default function Settings() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Settings</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          Manage your preferences and app settings
        </p>
      </div>

      <div className="card">
        <h2 className="text-xl font-semibold mb-4 flex items-center space-x-2">
          <SettingsIcon className="w-5 h-5" />
          <span>App Settings</span>
        </h2>

        <div className="space-y-4">
          <div>
            <h3 className="font-medium mb-2">About This App</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Nashville Safe Tourist Guide helps tourists safely explore Nashville by identifying
              high-risk areas based on 911 call data analysis. It uses machine learning clustering
              algorithms (DBSCAN) to identify crime hotspots and provides real-time warnings.
            </p>
          </div>

          <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
            <h3 className="font-medium mb-2">Developer</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              This application is developed by{' '}
              <span className="font-semibold text-primary-600 dark:text-primary-400">
                Abhijeet Solanki
              </span>
            </p>
          </div>

          <div>
            <h3 className="font-medium mb-2">Features</h3>
            <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
              <li>🗺️ Interactive map with hotspot visualization</li>
              <li>📍 Real-time location tracking</li>
              <li>🚨 Geofencing alerts</li>
              <li>📊 Detailed statistics and explanations</li>
              <li>🗺️ Safe route planning</li>
              <li>⏰ Time-of-day risk analysis</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

