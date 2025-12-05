import { useEffect, useState } from 'react';
import { useStore } from '../store/useStore';
import type { Hotspot } from '../types';
import { AlertTriangle, Info, TrendingUp } from 'lucide-react';
import { motion } from 'framer-motion';

export default function Statistics() {
  const { filteredHotspots, loading } = useStore();
  const [sortedHotspots, setSortedHotspots] = useState<Hotspot[]>([]);

  useEffect(() => {
    const sorted = [...filteredHotspots].sort((a, b) => b.total_risk_score - a.total_risk_score);
    setSortedHotspots(sorted.slice(0, 20)); // Top 20
  }, [filteredHotspots]);

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'High':
        return 'bg-danger-100 dark:bg-danger-900 text-danger-800 dark:text-danger-200 border-danger-200 dark:border-danger-800';
      case 'Medium':
        return 'bg-warning-100 dark:bg-warning-900 text-warning-800 dark:text-warning-200 border-warning-200 dark:border-warning-800';
      case 'Low':
        return 'bg-success-100 dark:bg-success-900 text-success-800 dark:text-success-200 border-success-200 dark:border-success-800';
      default:
        return 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600 dark:text-gray-400">Loading statistics...</p>
        </div>
      </div>
    );
  }

  const totalIncidents = filteredHotspots.reduce((sum, h) => sum + h.total_incidents, 0);
  const highRiskCount = filteredHotspots.filter((h) => h.severity === 'High').length;
  const mediumRiskCount = filteredHotspots.filter((h) => h.severity === 'Medium').length;
  const lowRiskCount = filteredHotspots.filter((h) => h.severity === 'Low').length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Crime Hotspot Statistics</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          Detailed analysis of high-risk areas in Nashville
        </p>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card"
        >
          <p className="text-sm text-gray-600 dark:text-gray-400">Total Hotspots</p>
          <p className="text-3xl font-bold mt-2">{filteredHotspots.length}</p>
        </motion.div>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card"
        >
          <p className="text-sm text-gray-600 dark:text-gray-400">High Risk Areas</p>
          <p className="text-3xl font-bold text-danger-600 mt-2">{highRiskCount}</p>
          <p className="text-xs text-gray-500 mt-1">
            {((highRiskCount / filteredHotspots.length) * 100).toFixed(1)}% of total
          </p>
        </motion.div>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="card"
        >
          <p className="text-sm text-gray-600 dark:text-gray-400">Total Incidents</p>
          <p className="text-3xl font-bold mt-2">{totalIncidents.toLocaleString()}</p>
        </motion.div>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="card"
        >
          <p className="text-sm text-gray-600 dark:text-gray-400">Medium Risk</p>
          <p className="text-3xl font-bold text-warning-600 mt-2">{mediumRiskCount}</p>
        </motion.div>
      </div>

      {/* Hotspot Cards */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          High-Risk Areas to Avoid
        </h2>
        <div className="space-y-4">
          {sortedHotspots.map((hotspot, index) => (
            <motion.div
              key={hotspot.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.05 }}
              className={`card border-l-4 ${getSeverityColor(hotspot.severity)}`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <AlertTriangle className="w-5 h-5" />
                    <h3 className="text-lg font-semibold">
                      Hotspot #{hotspot.id} - {hotspot.severity} Risk
                    </h3>
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
                    <div>
                      <p className="text-xs text-gray-500 dark:text-gray-400">Location</p>
                      <p className="text-sm font-medium">
                        {hotspot.latitude.toFixed(4)}, {hotspot.longitude.toFixed(4)}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500 dark:text-gray-400">Total Incidents</p>
                      <p className="text-sm font-medium">{hotspot.total_incidents.toLocaleString()}</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500 dark:text-gray-400">High Risk</p>
                      <p className="text-sm font-medium">{hotspot.high_risk_count.toLocaleString()}</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500 dark:text-gray-400">Radius</p>
                      <p className="text-sm font-medium">{hotspot.radius_meters.toFixed(0)}m</p>
                    </div>
                  </div>
                  <div className="mt-4 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                    <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">Why avoid?</p>
                    <p className="text-sm text-gray-700 dark:text-gray-300">{hotspot.explanation}</p>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}

