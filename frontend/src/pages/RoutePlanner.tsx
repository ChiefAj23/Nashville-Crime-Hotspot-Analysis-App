import { useState } from 'react';
import { Navigation2, MapPin, Shield } from 'lucide-react';
import { motion } from 'framer-motion';

export default function RoutePlanner() {
  const [startLat, setStartLat] = useState('36.1627');
  const [startLon, setStartLon] = useState('-86.7816');
  const [endLat, setEndLat] = useState('36.2000');
  const [endLon, setEndLon] = useState('-86.8000');
  const [avoidHotspots, setAvoidHotspots] = useState(true);
  const [loading, setLoading] = useState(false);
  const [route, setRoute] = useState<any>(null);
  const [alternatives, setAlternatives] = useState<any[]>([]);

  const handleCalculate = async () => {
    setLoading(true);
    try {
      const { calculateRoute, getAlternativeRoutes } = await import('../services/api');
      const calculatedRoute = await calculateRoute(
        parseFloat(startLat),
        parseFloat(startLon),
        parseFloat(endLat),
        parseFloat(endLon),
        avoidHotspots
      );
      setRoute(calculatedRoute);

      const altRoutes = await getAlternativeRoutes(
        parseFloat(startLat),
        parseFloat(startLon),
        parseFloat(endLat),
        parseFloat(endLon),
        3
      );
      setAlternatives(altRoutes);
    } catch (error) {
      console.error('Error calculating route:', error);
      alert('Failed to calculate route. Please check if backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Safe Route Planner</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          Plan your route avoiding high-risk areas
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <div className="card space-y-4">
          <h2 className="text-xl font-semibold">Route Details</h2>

          <div>
            <label className="block text-sm font-medium mb-2">Starting Point</label>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <input
                  type="number"
                  step="any"
                  value={startLat}
                  onChange={(e) => setStartLat(e.target.value)}
                  placeholder="Latitude"
                  className="input"
                />
              </div>
              <div>
                <input
                  type="number"
                  step="any"
                  value={startLon}
                  onChange={(e) => setStartLon(e.target.value)}
                  placeholder="Longitude"
                  className="input"
                />
              </div>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Destination</label>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <input
                  type="number"
                  step="any"
                  value={endLat}
                  onChange={(e) => setEndLat(e.target.value)}
                  placeholder="Latitude"
                  className="input"
                />
              </div>
              <div>
                <input
                  type="number"
                  step="any"
                  value={endLon}
                  onChange={(e) => setEndLon(e.target.value)}
                  placeholder="Longitude"
                  className="input"
                />
              </div>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <input
              type="checkbox"
              id="avoidHotspots"
              checked={avoidHotspots}
              onChange={(e) => setAvoidHotspots(e.target.checked)}
              className="w-4 h-4"
            />
            <label htmlFor="avoidHotspots" className="text-sm">
              Avoid High-Risk Hotspots
            </label>
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
                <Navigation2 className="w-5 h-5" />
                <span>Calculate Safe Route</span>
              </>
            )}
          </button>
        </div>

        {/* Route Results */}
        {route && (
          <div className="card space-y-4">
            <h2 className="text-xl font-semibold">Route Details</h2>

            <div className="grid grid-cols-3 gap-4">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Safety Score</p>
                <p className="text-2xl font-bold mt-1">{route.safety_score.toFixed(1)}/100</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Distance</p>
                <p className="text-2xl font-bold mt-1">{(route.distance_meters / 1000).toFixed(2)} km</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Hotspots Avoided</p>
                <p className="text-2xl font-bold mt-1">{route.hotspots_avoided}</p>
              </div>
            </div>

            {route.safety_score >= 80 && (
              <div className="p-4 bg-success-100 dark:bg-success-900 rounded-lg">
                <p className="text-success-800 dark:text-success-200">✅ This route is relatively safe!</p>
              </div>
            )}
            {route.safety_score < 60 && (
              <div className="p-4 bg-danger-100 dark:bg-danger-900 rounded-lg">
                <p className="text-danger-800 dark:text-danger-200">
                  🚨 This route passes through high-risk areas. Consider alternatives.
                </p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Alternative Routes */}
      {alternatives.length > 0 && (
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Alternative Routes</h2>
          <div className="space-y-3">
            {alternatives.map((alt, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-semibold">Alternative Route {index + 1}</h3>
                    <div className="flex items-center space-x-4 mt-2">
                      <span className="text-sm">
                        Safety: <strong>{alt.safety_score.toFixed(1)}/100</strong>
                      </span>
                      <span className="text-sm">
                        Distance: <strong>{(alt.distance_meters / 1000).toFixed(2)} km</strong>
                      </span>
                    </div>
                  </div>
                  {alt.safety_score > route.safety_score && (
                    <span className="px-3 py-1 bg-success-100 dark:bg-success-900 text-success-800 dark:text-success-200 rounded-full text-sm">
                      Safer Option
                    </span>
                  )}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

