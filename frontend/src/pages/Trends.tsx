import { useState, useEffect } from 'react';
import { TrendingUp, BarChart3 } from 'lucide-react';
import { motion } from 'framer-motion';

export default function Trends() {
  const [trendType, setTrendType] = useState<'monthly' | 'seasonal' | 'daily' | 'yearly'>('monthly');
  const [loading, setLoading] = useState(false);
  const [trendData, setTrendData] = useState<any>(null);

  useEffect(() => {
    loadTrends();
  }, [trendType]);

  const loadTrends = async () => {
    setLoading(true);
    try {
      const { getHistoricalTrends } = await import('../services/api');
      const data = await getHistoricalTrends(trendType);
      setTrendData(data);
    } catch (error) {
      console.error('Error loading trends:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Historical Trends & Patterns</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          Analyze crime patterns over time
        </p>
      </div>

      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold">Trend Analysis</h2>
          <select
            value={trendType}
            onChange={(e) => setTrendType(e.target.value as any)}
            className="input w-auto"
          >
            <option value="monthly">Monthly</option>
            <option value="seasonal">Seasonal</option>
            <option value="daily">Day of Week</option>
            <option value="yearly">Yearly</option>
          </select>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>
        ) : trendData ? (
          <div className="space-y-4">
            <p className="text-gray-600 dark:text-gray-400">
              Trend data will be displayed here. Backend API integration required.
            </p>
          </div>
        ) : (
          <div className="text-center py-12 text-gray-500">
            <BarChart3 className="w-16 h-16 mx-auto mb-4 opacity-50" />
            <p>No trend data available</p>
          </div>
        )}
      </div>
    </div>
  );
}

