"""
Weather Integration Service - Microservice for weather-based risk adjustments
"""
import streamlit as st
from typing import Dict, Optional
import requests
from datetime import datetime

class WeatherIntegrationService:
    """Service for integrating weather data with safety analysis"""

    # OpenWeatherMap API (requires API key - using free tier)
    WEATHER_API_KEY = None  # Set in environment or config
    WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

    # Weather risk multipliers
    WEATHER_RISK_MULTIPLIERS = {
        'Clear': 1.0,
        'Clouds': 1.0,
        'Rain': 1.2,  # 20% increase in risk
        'Thunderstorm': 1.5,  # 50% increase
        'Snow': 1.3,
        'Fog': 1.4,
        'Extreme': 2.0  # Double risk
    }

    @staticmethod
    def get_weather(latitude: float, longitude: float, api_key: Optional[str] = None) -> Dict:
        """
        Get current weather for a location

        Args:
            latitude: Location latitude
            longitude: Location longitude
            api_key: Optional OpenWeatherMap API key

        Returns:
            Weather data dictionary
        """
        api_key = api_key or WeatherIntegrationService.WEATHER_API_KEY

        if not api_key:
            # Return mock data if no API key
            return {
                'temperature': 72,
                'condition': 'Clear',
                'description': 'Clear sky',
                'humidity': 60,
                'wind_speed': 5,
                'api_available': False
            }

        try:
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': api_key,
                'units': 'imperial'
            }

            response = requests.get(WeatherIntegrationService.WEATHER_API_URL, params=params, timeout=5)

            if response.status_code == 200:
                data = response.json()
                return {
                    'temperature': data['main']['temp'],
                    'condition': data['weather'][0]['main'],
                    'description': data['weather'][0]['description'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': data.get('wind', {}).get('speed', 0),
                    'api_available': True
                }
        except Exception as e:
            st.warning(f"Weather API unavailable: {str(e)}")

        # Fallback to mock data
        return {
            'temperature': 72,
            'condition': 'Clear',
            'description': 'Weather data unavailable',
            'humidity': 60,
            'wind_speed': 5,
            'api_available': False
        }

    @staticmethod
    def adjust_risk_for_weather(base_risk_score: float, weather: Dict) -> float:
        """
        Adjust risk score based on weather conditions

        Args:
            base_risk_score: Base safety score (0-100)
            weather: Weather data dictionary

        Returns:
            Adjusted risk score
        """
        condition = weather.get('condition', 'Clear')
        multiplier = WeatherIntegrationService.WEATHER_RISK_MULTIPLIERS.get(condition, 1.0)

        # Lower score = more dangerous, so multiply penalty
        # Convert score to risk (inverse), apply multiplier, convert back
        risk = 100 - base_risk_score
        adjusted_risk = risk * multiplier
        adjusted_score = max(0, 100 - adjusted_risk)

        return adjusted_score

    @staticmethod
    def get_travel_recommendation(weather: Dict, base_risk: str = 'Medium') -> str:
        """
        Get travel recommendation based on weather

        Args:
            weather: Weather data dictionary
            base_risk: Base risk level

        Returns:
            Recommendation text
        """
        condition = weather.get('condition', 'Clear')
        temp = weather.get('temperature', 70)

        recommendations = []

        if condition in ['Rain', 'Thunderstorm', 'Snow']:
            recommendations.append("🌧️ Bad weather conditions. Consider postponing travel if possible.")
            recommendations.append("🚗 Drive carefully - wet/slippery roads increase accident risk.")

        if condition == 'Fog':
            recommendations.append("🌫️ Low visibility. Use extra caution when driving.")

        if condition == 'Extreme':
            recommendations.append("⚠️ Extreme weather conditions. Avoid travel if possible.")

        if temp < 32:
            recommendations.append("❄️ Freezing temperatures. Watch for ice on roads.")
        elif temp > 90:
            recommendations.append("☀️ High temperatures. Stay hydrated and avoid prolonged exposure.")

        if not recommendations:
            recommendations.append("✅ Weather conditions are favorable for travel.")

        return " ".join(recommendations)

    @staticmethod
    def render_weather_panel(latitude: Optional[float] = None, longitude: Optional[float] = None) -> Dict:
        """Render weather information panel"""
        st.markdown("### 🌤️ Current Weather")

        if not latitude or not longitude:
            st.info("📍 Enable location tracking to get weather data")
            col1, col2 = st.columns(2)
            with col1:
                latitude = st.number_input("Latitude", value=36.1627, format="%.6f", key="weather_lat")
            with col2:
                longitude = st.number_input("Longitude", value=-86.7816, format="%.6f", key="weather_lon")

        if st.button("🌤️ Get Weather", use_container_width=True):
            weather = WeatherIntegrationService.get_weather(latitude, longitude)

            # Display weather
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Temperature", f"{weather['temperature']:.0f}°F")
            with col2:
                st.metric("Condition", weather['condition'])
            with col3:
                st.metric("Humidity", f"{weather['humidity']}%")

            # Recommendation
            recommendation = WeatherIntegrationService.get_travel_recommendation(weather)
            st.info(recommendation)

            if not weather.get('api_available', False):
                st.warning("💡 Using mock weather data. Add OpenWeatherMap API key for real-time weather.")

            return weather

        return {}

