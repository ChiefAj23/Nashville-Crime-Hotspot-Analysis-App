import { useState, useEffect, useRef } from 'react';
import { useStore } from '../store/useStore';
import { MapPin, Navigation, X, AlertTriangle, CheckCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { haversineDistance } from '../utils/distance';
import type { Hotspot } from '../types';

export default function GPSTracker() {
  const { userLocation, setUserLocation, filteredHotspots } = useStore();
  const [isTracking, setIsTracking] = useState(false);
  const [locationError, setLocationError] = useState<string | null>(null);
  const [locationMethod, setLocationMethod] = useState<'gps' | 'manual'>('gps');
  const [manualLat, setManualLat] = useState('36.1627');
  const [manualLon, setManualLon] = useState('-86.7816');
  const watchIdRef = useRef<number | null>(null);

  // Continuous location tracking
  useEffect(() => {
    if (isTracking && locationMethod === 'gps') {
      if (!navigator.geolocation) {
        setLocationError('Geolocation is not supported by your browser');
        setIsTracking(false);
        return;
      }

      const options = {
        enableHighAccuracy: true,
        timeout: 15000,
        maximumAge: 0,
      };

      // Get initial position
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setUserLocation({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            timestamp: Date.now(),
          });
          setLocationError(null);
        },
        (error) => {
          setLocationError(getLocationErrorMessage(error));
          setIsTracking(false);
        },
        options
      );

      // Watch position for continuous updates
      watchIdRef.current = navigator.geolocation.watchPosition(
        (position) => {
          setUserLocation({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            timestamp: Date.now(),
          });
          setLocationError(null);
        },
        (error) => {
          setLocationError(getLocationErrorMessage(error));
        },
        options
      );
    } else {
      // Stop watching
      if (watchIdRef.current !== null) {
        navigator.geolocation.clearWatch(watchIdRef.current);
        watchIdRef.current = null;
      }
    }

    return () => {
      if (watchIdRef.current !== null) {
        navigator.geolocation.clearWatch(watchIdRef.current);
      }
    };
  }, [isTracking, locationMethod, setUserLocation]);

  const getLocationErrorMessage = (error: GeolocationPositionError): string => {
    switch (error.code) {
      case error.PERMISSION_DENIED:
        return 'Location permission denied. Please enable location access in your browser settings.';
      case error.POSITION_UNAVAILABLE:
        return 'Location information unavailable. Please check your GPS signal.';
      case error.TIMEOUT:
        return 'Location request timed out. Please try again.';
      default:
        return 'An unknown error occurred while getting location.';
    }
  };

  const handleManualLocation = () => {
    const lat = parseFloat(manualLat);
    const lon = parseFloat(manualLon);

    if (isNaN(lat) || isNaN(lon)) {
      setLocationError('Please enter valid coordinates');
      return;
    }

    if (lat < -90 || lat > 90 || lon < -180 || lon > 180) {
      setLocationError('Invalid coordinate range. Lat: -90 to 90, Lon: -180 to 180');
      return;
    }

    setUserLocation({
      latitude: lat,
      longitude: lon,
      timestamp: Date.now(),
    });
    setLocationError(null);
    setIsTracking(true);
  };

  const stopTracking = () => {
    setIsTracking(false);
    setUserLocation(null);
    setLocationError(null);
    if (watchIdRef.current !== null) {
      navigator.geolocation.clearWatch(watchIdRef.current);
      watchIdRef.current = null;
    }
  };

  // Check if user is near hotspots
  const nearbyHotspots = userLocation
    ? filteredHotspots
        .map((hotspot) => {
          const distance = haversineDistance(
            userLocation.latitude,
            userLocation.longitude,
            hotspot.latitude,
            hotspot.longitude
          );
          return { hotspot, distance };
        })
        .filter((item) => item.distance <= item.hotspot.radius_meters + 50)
        .map((item) => item.hotspot)
    : [];

  return (
    <div className="space-y-4">
      {/* GPS Tracker Card */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold flex items-center space-x-2">
            <Navigation className="w-5 h-5 text-primary-600" />
            <span>📍 GPS Location Tracker</span>
          </h3>
          {userLocation && (
            <button
              onClick={stopTracking}
              className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
              aria-label="Stop tracking"
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>

        {/* Location Method Selection */}
        <div className="mb-4">
          <div className="flex space-x-2">
            <button
              onClick={() => {
                setLocationMethod('gps');
                setIsTracking(false);
              }}
              className={`flex-1 px-4 py-2 rounded-lg transition-colors duration-200 text-sm font-medium ${
                locationMethod === 'gps'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
              }`}
            >
              📍 Browser GPS
            </button>
            <button
              onClick={() => {
                setLocationMethod('manual');
                setIsTracking(false);
              }}
              className={`flex-1 px-4 py-2 rounded-lg transition-colors duration-200 text-sm font-medium ${
                locationMethod === 'manual'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
              }`}
            >
              ✏️ Manual Entry
            </button>
          </div>
        </div>

        {/* GPS Mode */}
        {locationMethod === 'gps' && (
          <div className="space-y-3">
            <button
              onClick={() => setIsTracking(!isTracking)}
              className={`w-full flex items-center justify-center space-x-2 px-4 py-2 rounded-lg font-semibold transition-colors duration-200 ${
                isTracking
                  ? 'bg-danger-600 hover:bg-danger-700 text-white'
                  : 'bg-primary-600 hover:bg-primary-700 text-white'
              }`}
            >
              <Navigation className="w-5 h-5" />
              <span>{isTracking ? 'Stop Tracking' : 'Start GPS Tracking'}</span>
            </button>

            {isTracking && (
              <div className="p-3 bg-primary-50 dark:bg-primary-900 rounded-lg border border-primary-200 dark:border-primary-800">
                <p className="text-sm text-primary-800 dark:text-primary-200">
                  📍 Tracking your location... Allow browser location access if prompted.
                </p>
                <p className="text-xs text-primary-700 dark:text-primary-300 mt-1">
                  You'll receive alerts when entering high-risk areas.
                </p>
              </div>
            )}
          </div>
        )}

        {/* Manual Entry Mode */}
        {locationMethod === 'manual' && (
          <div className="space-y-3">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-sm font-medium mb-1">Latitude</label>
                <input
                  type="number"
                  step="any"
                  value={manualLat}
                  onChange={(e) => setManualLat(e.target.value)}
                  placeholder="36.1627"
                  className="input"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Longitude</label>
                <input
                  type="number"
                  step="any"
                  value={manualLon}
                  onChange={(e) => setManualLon(e.target.value)}
                  placeholder="-86.7816"
                  className="input"
                />
              </div>
            </div>
            <button
              onClick={handleManualLocation}
              className="w-full btn-primary flex items-center justify-center space-x-2"
            >
              <MapPin className="w-5 h-5" />
              <span>Set Location</span>
            </button>
          </div>
        )}

        {/* Current Location Display */}
        {userLocation && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-4 p-3 bg-success-50 dark:bg-success-900 rounded-lg border border-success-200 dark:border-success-800"
          >
            <div className="flex items-start space-x-2">
              <CheckCircle className="w-5 h-5 text-success-600 dark:text-success-400 flex-shrink-0 mt-0.5" />
              <div className="flex-1">
                <p className="text-sm font-semibold text-success-900 dark:text-success-100">
                  Current Location
                </p>
                <p className="text-xs text-success-800 dark:text-success-200 mt-1">
                  {userLocation.latitude.toFixed(6)}, {userLocation.longitude.toFixed(6)}
                </p>
                {isTracking && locationMethod === 'gps' && (
                  <p className="text-xs text-success-700 dark:text-success-300 mt-1">
                    🔄 Tracking active - Updates automatically
                  </p>
                )}
              </div>
            </div>
          </motion.div>
        )}

        {/* Error Display */}
        {locationError && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-3 p-3 bg-danger-50 dark:bg-danger-900 rounded-lg border border-danger-200 dark:border-danger-800"
          >
            <p className="text-sm text-danger-800 dark:text-danger-200">{locationError}</p>
          </motion.div>
        )}

        {/* Nearby Hotspots Warning */}
        <AnimatePresence>
          {nearbyHotspots.length > 0 && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="mt-4 p-4 bg-danger-100 dark:bg-danger-900 rounded-lg border border-danger-200 dark:border-danger-800"
            >
              <div className="flex items-start space-x-2">
                <AlertTriangle className="w-5 h-5 text-danger-600 dark:text-danger-400 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <p className="text-sm font-semibold text-danger-900 dark:text-danger-100">
                    ⚠️ You are near {nearbyHotspots.length} hotspot{nearbyHotspots.length > 1 ? 's' : ''}!
                  </p>
                  {nearbyHotspots.filter((h) => h.severity === 'High').length > 0 && (
                    <p className="text-xs text-danger-800 dark:text-danger-200 mt-1">
                      🚨 HIGH RISK AREA DETECTED - Exercise extreme caution!
                    </p>
                  )}
                  {nearbyHotspots.filter((h) => h.severity === 'Medium').length > 0 && (
                    <p className="text-xs text-danger-700 dark:text-danger-300 mt-1">
                      ⚠️ Medium risk areas nearby - Stay alert.
                    </p>
                  )}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
