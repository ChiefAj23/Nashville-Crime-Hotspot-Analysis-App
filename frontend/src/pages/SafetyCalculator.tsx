import { useState } from 'react';
import { Calculator, Shield, MapPin } from 'lucide-react';
import { motion } from 'framer-motion';

export default function SafetyCalculator() {
  const [latitude, setLatitude] = useState('36.1627');
  const [longitude, setLongitude] = useState('-86.7816');
  const [radius, setRadius] = useState(1000);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleCalculate = async () => {
    setLoading(true);
    try {
      const { calculateSafetyScore } = await import('../services/api');
      const score = await calculateSafetyScore(
        parseFloat(latitude),
        parseFloat(longitude),
        radius
      );
      setResult(score);
    } catch (error) {
      console.error('Error calculating safety score:', error);
      alert('Failed to calculate safety score. Please check if backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const getSafetyLevel = (score: number) => {
    if (score >= 80) return { level: 'Very Safe', color: 'success', emoji: '✅' };
    if (score >= 60) return { level: 'Safe', color: 'success', emoji: '✅' };
    if (score >= 40) return { level: 'Moderate Risk', color: 'warning', emoji: '⚠️' };
    if (score >= 20) return { level: 'High Risk', color: 'danger', emoji: '🚨' };
    return { level: 'Very High Risk', color: 'danger', emoji: '🚨' };
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Safety Score Calculator</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          Calculate the safety score for any location in Nashville
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <div className="card space-y-4">
          <h2 className="text-xl font-semibold">Location Details</h2>

          <div>
            <label className="block text-sm font-medium mb-2">Coordinates</label>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <input
                  type="number"
                  step="any"
                  value={latitude}
                  onChange={(e) => setLatitude(e.target.value)}
                  placeholder="Latitude"
                  className="input"
                />
              </div>
              <div>
                <input
                  type="number"
                  step="any"
                  value={longitude}
                  onChange={(e) => setLongitude(e.target.value)}
                  placeholder="Longitude"
                  className="input"
                />
              </div>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">
              Search Radius: {radius}m
            </label>
            <input
              type="range"
              min="100"
              max="5000"
              step="100"
              value={radius}
              onChange={(e) => setRadius(parseInt(e.target.value))}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>100m</span>
              <span>5000m</span>
            </div>
          </div>

          <button
            onClick={handleCalculate}
            disabled={loading}
            className="btn-primary w-full flex items-center justify-center space-x-2"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                <span>Calculating...</span>
              </>
            ) : (
              <>
                <Calculator className="w-5 h-5" />
                <span>Calculate Safety Score</span>
              </>
            )}
          </button>
        </div>

        {/* Results */}
        {result && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="card space-y-4"
          >
            <h2 className="text-xl font-semibold">Safety Analysis</h2>

            <div className="text-center py-8">
              <div className="text-6xl font-bold mb-2">{result.score.toFixed(0)}</div>
              <div className="text-2xl text-gray-600 dark:text-gray-400">/ 100</div>
            </div>

            {(() => {
              const safety = getSafetyLevel(result.score);
              return (
                <div className={`p-4 bg-${safety.color}-100 dark:bg-${safety.color}-900 rounded-lg text-center`}>
                  <p className="text-2xl mb-2">{safety.emoji}</p>
                  <p className={`text-lg font-semibold text-${safety.color}-800 dark:text-${safety.color}-200`}>
                    {safety.level}
                  </p>
                </div>
              );
            })()}

            {result.details && (
              <div className="mt-4 space-y-2">
                <h3 className="font-semibold">Details:</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">{result.details.recommendation}</p>
              </div>
            )}
          </motion.div>
        )}
      </div>
    </div>
  );
}

