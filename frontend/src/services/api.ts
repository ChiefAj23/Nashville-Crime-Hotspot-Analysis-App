import axios from 'axios';
import type { Hotspot, Route, NearbyPlace, WeatherData, UserPreferences, FavoriteLocation } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Hotspots
export const getHotspots = async (): Promise<Hotspot[]> => {
  const response = await api.get('/hotspots');
  return response.data;
};

export const getFilteredHotspots = async (filters: {
  severity?: string[];
  crimeTypes?: string[];
  timeFilter?: string;
}): Promise<Hotspot[]> => {
  const response = await api.post('/hotspots/filter', filters);
  return response.data;
};

// Route Planning
export const calculateRoute = async (
  startLat: number,
  startLon: number,
  endLat: number,
  endLon: number,
  avoidHotspots: boolean = true
): Promise<Route> => {
  const response = await api.post('/route/calculate', {
    start_lat: startLat,
    start_lon: startLon,
    end_lat: endLat,
    end_lon: endLon,
    avoid_hotspots: avoidHotspots,
  });
  return response.data;
};

export const getAlternativeRoutes = async (
  startLat: number,
  startLon: number,
  endLat: number,
  endLon: number,
  numAlternatives: number = 3
): Promise<Route[]> => {
  const response = await api.post('/route/alternatives', {
    start_lat: startLat,
    start_lon: startLon,
    end_lat: endLat,
    end_lon: endLon,
    num_alternatives: numAlternatives,
  });
  return response.data;
};

// Safety Score
export const calculateSafetyScore = async (
  latitude: number,
  longitude: number,
  radiusMeters: number = 1000
): Promise<{ score: number; details: any }> => {
  const response = await api.post('/safety/calculate', {
    latitude,
    longitude,
    radius_meters: radiusMeters,
  });
  return response.data;
};

// Nearby Places
export const getNearbyPlaces = async (
  latitude: number,
  longitude: number,
  radiusMeters: number = 2000
): Promise<{
  police_stations: NearbyPlace[];
  hospitals: NearbyPlace[];
  safe_areas: NearbyPlace[];
}> => {
  const response = await api.get('/nearby-places', {
    params: { latitude, longitude, radius_meters: radiusMeters },
  });
  return response.data;
};

// Weather
export const getWeather = async (
  latitude: number,
  longitude: number
): Promise<WeatherData> => {
  const response = await api.get('/weather', {
    params: { latitude, longitude },
  });
  return response.data;
};

// Time Analysis
export const getTimeAnalysis = async (
  hotspotId?: number
): Promise<{
  hourly_patterns: Record<number, number>;
  safe_hours: number[];
  peak_hours: number[];
}> => {
  const response = await api.get('/time-analysis', {
    params: { hotspot_id: hotspotId },
  });
  return response.data;
};

// Historical Trends
export const getHistoricalTrends = async (type: 'monthly' | 'seasonal' | 'daily' | 'yearly') => {
  const response = await api.get('/trends', {
    params: { type },
  });
  return response.data;
};

// User Preferences
export const getUserPreferences = async (): Promise<UserPreferences> => {
  const response = await api.get('/user/preferences');
  return response.data;
};

export const saveUserPreferences = async (preferences: Partial<UserPreferences>): Promise<void> => {
  await api.post('/user/preferences', preferences);
};

export const getFavorites = async (): Promise<FavoriteLocation[]> => {
  const response = await api.get('/user/favorites');
  return response.data;
};

export const saveFavorite = async (location: Omit<FavoriteLocation, 'saved_at'>): Promise<void> => {
  await api.post('/user/favorites', location);
};

export const deleteFavorite = async (locationName: string): Promise<void> => {
  await api.delete(`/user/favorites/${encodeURIComponent(locationName)}`);
};

export default api;

