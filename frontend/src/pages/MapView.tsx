import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Circle, Popup, Marker, useMap } from 'react-leaflet';
import { useStore } from '../store/useStore';
import FilterPanel from '../components/FilterPanel';
import GPSTracker from '../components/GPSTracker';
import { haversineDistance } from '../utils/distance';
import type { Hotspot, UserLocation } from '../types';
import { MapPin, AlertTriangle } from 'lucide-react';
import { motion } from 'framer-motion';
import 'leaflet/dist/leaflet.css';

// Fix for default marker icons in React-Leaflet
import L from 'leaflet';
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

const NASHVILLE_CENTER: [number, number] = [36.1627, -86.7816];

export default function MapView() {
  const { filteredHotspots, hotspots, userLocation, loading, error } = useStore();
  const [map, setMap] = useState<any>(null);

  // Debug log
  useEffect(() => {
    console.log('MapView - Hotspots loaded:', hotspots.length);
    console.log('MapView - Filtered hotspots:', filteredHotspots.length);
    console.log('MapView - Loading:', loading);
    console.log('MapView - Error:', error);
    if (filteredHotspots.length > 0) {
      console.log('MapView - First hotspot:', filteredHotspots[0]);
    }
  }, [hotspots, filteredHotspots, loading, error]);

  // Map center updater component
  function MapCenterUpdater({ center }: { center: [number, number] }) {
    const map = useMap();
    useEffect(() => {
      map.setView(center, map.getZoom());
    }, [center, map]);
    return null;
  }

  const getColorBySeverity = (severity: string) => {
    switch (severity) {
      case 'High':
        return '#ef4444';
      case 'Medium':
        return '#f59e0b';
      case 'Low':
        return '#22c55e';
      default:
        return '#6b7280';
    }
  };

  const getRiskLevel = (hotspot: Hotspot) => {
    const { latitude: userLat, longitude: userLon } = userLocation || {};
    if (!userLat || !userLon) return null;

    const distance = haversineDistance(userLat, userLon, hotspot.latitude, hotspot.longitude);

    if (distance <= hotspot.radius_meters + 50) {
      return { distance, inRange: true };
    }
    return { distance, inRange: false };
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600 dark:text-gray-400">Loading map data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Filter Panel */}
      <FilterPanel />

      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Interactive Safety Map</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Explore Nashville with real-time crime hotspot data
          </p>
          <p className="text-xs text-gray-500 dark:text-gray-500 mt-2">
            Developed by{' '}
            <span className="font-semibold text-primary-600 dark:text-primary-400">
              Abhijeet Solanki
            </span>
          </p>
        </div>
      </div>

      {/* GPS Tracker */}
      <GPSTracker />

      {/* Error Message */}
      {error && (
        <div className="bg-danger-100 dark:bg-danger-900 border border-danger-200 dark:border-danger-800 rounded-xl p-4">
          <p className="text-danger-800 dark:text-danger-200">{error}</p>
        </div>
      )}


      {/* Alert Banner */}
      {userLocation && filteredHotspots.some((h) => {
        const risk = getRiskLevel(h);
        return risk?.inRange && h.severity === 'High';
      }) && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-danger-100 dark:bg-danger-900 border border-danger-200 dark:border-danger-800 rounded-xl p-4 flex items-start space-x-3"
        >
          <AlertTriangle className="w-6 h-6 text-danger-600 dark:text-danger-400 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-semibold text-danger-900 dark:text-danger-100">High Risk Area Detected!</h3>
            <p className="text-danger-800 dark:text-danger-200 mt-1">
              You are currently in or near a high-risk area. Exercise extreme caution.
            </p>
          </div>
        </motion.div>
      )}

      {/* Legend */}
      <div className="flex flex-wrap gap-4">
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 rounded-full bg-danger-500"></div>
          <span className="text-sm">High Risk</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 rounded-full bg-warning-500"></div>
          <span className="text-sm">Medium Risk</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 rounded-full bg-success-500"></div>
          <span className="text-sm">Low Risk</span>
        </div>
        {userLocation && (
          <div className="flex items-center space-x-2">
            <MapPin className="w-4 h-4 text-primary-600" />
            <span className="text-sm">Your Location</span>
          </div>
        )}
      </div>

      {/* Map */}
      <div className="card p-0 overflow-hidden" style={{ position: 'relative', zIndex: 1 }}>
        <MapContainer
          center={NASHVILLE_CENTER}
          zoom={12}
          style={{ height: '600px', width: '100%', position: 'relative', zIndex: 1 }}
          ref={setMap}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {/* Hotspots */}
          {filteredHotspots && filteredHotspots.length > 0 ? (
            filteredHotspots.map((hotspot) => {
              // Ensure hotspot has valid coordinates
              if (!hotspot.latitude || !hotspot.longitude) {
                console.warn('Invalid hotspot coordinates:', hotspot);
                return null;
              }

              return (
                <Circle
                  key={hotspot.id}
                  center={[hotspot.latitude, hotspot.longitude]}
                  radius={hotspot.radius_meters || 500}
                  pathOptions={{
                    color: getColorBySeverity(hotspot.severity),
                    fillColor: getColorBySeverity(hotspot.severity),
                    fillOpacity: 0.2,
                    weight: 2,
                  }}
                >
                  <Popup>
                    <div className="p-2">
                      <h3 className="font-semibold">Hotspot #{hotspot.id}</h3>
                      <p className="text-sm text-gray-600">Severity: {hotspot.severity}</p>
                      <p className="text-sm text-gray-600">Incidents: {hotspot.total_incidents?.toLocaleString() || 0}</p>
                      <p className="text-xs text-gray-500 mt-2">{hotspot.explanation || 'No explanation available'}</p>
                    </div>
                  </Popup>
                </Circle>
              );
            })
          ) : (
            !loading && (
              <div className="absolute top-4 left-4 z-[1000] bg-yellow-100 dark:bg-yellow-900 border border-yellow-300 dark:border-yellow-700 rounded-lg p-3 max-w-md">
                <p className="text-sm text-yellow-800 dark:text-yellow-200 font-semibold">No hotspots to display</p>
                <p className="text-xs text-yellow-700 dark:text-yellow-300 mt-1">
                  {hotspots.length === 0
                    ? 'Hotspots data not loaded. Check backend server connection.'
                    : `Filtered out all ${hotspots.length} hotspots. Try adjusting filters.`}
                </p>
              </div>
            )
          )}

          {/* User Location */}
          {userLocation && (
            <>
              <Marker
                position={[userLocation.latitude, userLocation.longitude]}
                icon={L.divIcon({
                  className: 'custom-user-marker',
                  html: '<div style="background-color: #0ea5e9; width: 20px; height: 20px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div>',
                  iconSize: [20, 20],
                  iconAnchor: [10, 10],
                })}
              >
                <Popup>
                  <div className="p-2">
                    <h3 className="font-semibold">📍 Your Location</h3>
                    <p className="text-sm text-gray-600">
                      {userLocation.latitude.toFixed(6)}, {userLocation.longitude.toFixed(6)}
                    </p>
                  </div>
                </Popup>
              </Marker>

              {/* Update map center to user location */}
              <MapCenterUpdater center={[userLocation.latitude, userLocation.longitude]} />
            </>
          )}
        </MapContainer>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card"
        >
          <p className="text-sm text-gray-600 dark:text-gray-400">Total Hotspots</p>
          <p className="text-2xl font-bold mt-1">{filteredHotspots.length}</p>
        </motion.div>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card"
        >
          <p className="text-sm text-gray-600 dark:text-gray-400">High Risk</p>
          <p className="text-2xl font-bold text-danger-600 mt-1">
            {filteredHotspots.filter((h) => h.severity === 'High').length}
          </p>
        </motion.div>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="card"
        >
          <p className="text-sm text-gray-600 dark:text-gray-400">Medium Risk</p>
          <p className="text-2xl font-bold text-warning-600 mt-1">
            {filteredHotspots.filter((h) => h.severity === 'Medium').length}
          </p>
        </motion.div>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="card"
        >
          <p className="text-sm text-gray-600 dark:text-gray-400">Total Incidents</p>
          <p className="text-2xl font-bold mt-1">
            {filteredHotspots.reduce((sum, h) => sum + (h.total_incidents || 0), 0).toLocaleString()}
          </p>
        </motion.div>
      </div>
    </div>
  );
}
