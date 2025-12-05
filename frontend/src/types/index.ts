export interface Hotspot {
  id: number;
  latitude: number;
  longitude: number;
  radius_meters: number;
  severity: 'High' | 'Medium' | 'Low';
  total_incidents: number;
  high_risk_count: number;
  medium_risk_count: number;
  low_risk_count: number;
  total_risk_score: number;
  explanation: string;
}

export interface Route {
  waypoints: Array<[number, number]>;
  safety_score: number;
  distance_meters: number;
  route_type: string;
  hotspots_avoided: number;
}

export interface UserLocation {
  latitude: number;
  longitude: number;
  timestamp: number;
}

export interface EmergencyContact {
  name: string;
  phone: string;
  description: string;
  icon: string;
}

export interface NearbyPlace {
  name: string;
  latitude: number;
  longitude: number;
  distance: number;
  type: string;
  address?: string;
}

export interface WeatherData {
  temperature: number;
  condition: string;
  description: string;
  humidity: number;
  wind_speed: number;
  api_available: boolean;
}

export interface TimeFilter {
  type: string;
  current_hour: number;
}

export interface UserPreferences {
  risk_tolerance: string;
  alert_distance: number;
  high_risk_alerts: boolean;
  medium_risk_alerts: boolean;
  low_risk_alerts: boolean;
}

export interface FavoriteLocation {
  name: string;
  latitude: number;
  longitude: number;
  saved_at: string;
}

