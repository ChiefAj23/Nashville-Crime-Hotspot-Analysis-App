"""
User Preferences Service - Microservice for managing user preferences and favorites
"""
import streamlit as st
import json
import os
from typing import List, Dict, Optional

class UserPreferencesService:
    """Service for managing user preferences, favorites, and settings"""

    PREFERENCES_FILE = 'user_preferences.json'

    @staticmethod
    def _load_preferences() -> Dict:
        """Load user preferences from file"""
        if os.path.exists(UserPreferencesService.PREFERENCES_FILE):
            try:
                with open(UserPreferencesService.PREFERENCES_FILE, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    @staticmethod
    def _save_preferences(prefs: Dict) -> None:
        """Save user preferences to file"""
        try:
            with open(UserPreferencesService.PREFERENCES_FILE, 'w') as f:
                json.dump(prefs, f, indent=2)
        except Exception as e:
            st.error(f"Error saving preferences: {str(e)}")

    @staticmethod
    def save_favorite_location(location: Dict) -> None:
        """
        Save a favorite location

        Args:
            location: Location dictionary with name, latitude, longitude
        """
        prefs = UserPreferencesService._load_preferences()

        if 'favorites' not in prefs:
            prefs['favorites'] = []

        # Check if already exists
        existing = [f for f in prefs['favorites']
                   if f.get('latitude') == location.get('latitude') and
                   f.get('longitude') == location.get('longitude')]

        if not existing:
            location['saved_at'] = str(st.session_state.get('timestamp', 'unknown'))
            prefs['favorites'].append(location)
            UserPreferencesService._save_preferences(prefs)
            st.success(f"✅ Saved {location.get('name', 'Location')} to favorites!")
        else:
            st.info("📍 Location already in favorites")

    @staticmethod
    def get_favorites() -> List[Dict]:
        """
        Get all favorite locations

        Returns:
            List of favorite locations
        """
        prefs = UserPreferencesService._load_preferences()
        return prefs.get('favorites', [])

    @staticmethod
    def remove_favorite(location_name: str) -> None:
        """
        Remove a favorite location

        Args:
            location_name: Name of location to remove
        """
        prefs = UserPreferencesService._load_preferences()

        if 'favorites' in prefs:
            prefs['favorites'] = [f for f in prefs['favorites'] if f.get('name') != location_name]
            UserPreferencesService._save_preferences(prefs)
            st.success(f"✅ Removed {location_name} from favorites")

    @staticmethod
    def save_risk_settings(settings: Dict) -> None:
        """
        Save user risk tolerance settings

        Args:
            settings: Dictionary with risk settings
        """
        prefs = UserPreferencesService._load_preferences()
        prefs['risk_settings'] = settings
        UserPreferencesService._save_preferences(prefs)

    @staticmethod
    def get_risk_settings() -> Dict:
        """
        Get user risk tolerance settings

        Returns:
            Dictionary with risk settings
        """
        prefs = UserPreferencesService._load_preferences()
        return prefs.get('risk_settings', {
            'risk_tolerance': 'medium',
            'alert_distance': 500,
            'show_low_risk': True
        })

    @staticmethod
    def save_alert_preferences(alerts: Dict) -> None:
        """
        Save alert preferences

        Args:
            alerts: Dictionary with alert settings
        """
        prefs = UserPreferencesService._load_preferences()
        prefs['alerts'] = alerts
        UserPreferencesService._save_preferences(prefs)

    @staticmethod
    def get_alert_preferences() -> Dict:
        """
        Get alert preferences

        Returns:
            Dictionary with alert settings
        """
        prefs = UserPreferencesService._load_preferences()
        return prefs.get('alerts', {
            'high_risk_alerts': True,
            'medium_risk_alerts': True,
            'low_risk_alerts': False,
            'sound_alerts': False
        })

    @staticmethod
    def render_favorites_ui() -> None:
        """Render favorites management UI"""
        st.markdown("### ⭐ Favorite Locations")

        favorites = UserPreferencesService.get_favorites()

        if favorites:
            for fav in favorites:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{fav.get('name', 'Unnamed')}**")
                    st.caption(f"📍 {fav.get('latitude', 0):.4f}, {fav.get('longitude', 0):.4f}")
                with col2:
                    if st.button("🗑️", key=f"remove_{fav.get('name')}"):
                        UserPreferencesService.remove_favorite(fav.get('name'))
                        st.rerun()
        else:
            st.info("No favorite locations saved yet. Add locations from the map!")

        # Add new favorite
        st.markdown("---")
        st.markdown("#### ➕ Add Favorite Location")

        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            fav_name = st.text_input("Location Name", key="fav_name")
        with col2:
            fav_lat = st.number_input("Latitude", value=36.1627, format="%.6f", key="fav_lat")
        with col3:
            fav_lon = st.number_input("Longitude", value=-86.7816, format="%.6f", key="fav_lon")

        if st.button("💾 Save Favorite", use_container_width=True):
            if fav_name:
                UserPreferencesService.save_favorite_location({
                    'name': fav_name,
                    'latitude': fav_lat,
                    'longitude': fav_lon
                })
                st.rerun()
            else:
                st.warning("Please enter a location name")

    @staticmethod
    def render_preferences_ui() -> None:
        """Render user preferences UI"""
        st.markdown("### ⚙️ User Preferences")

        # Risk tolerance
        st.markdown("#### 🛡️ Risk Tolerance")
        risk_tolerance = st.select_slider(
            "Risk Tolerance Level:",
            options=['Low', 'Medium', 'High'],
            value='Medium',
            help="How much risk are you comfortable with?"
        )

        # Alert distance
        alert_distance = st.slider(
            "Alert Distance (meters):",
            min_value=100,
            max_value=2000,
            value=500,
            step=100,
            help="Distance at which to receive alerts"
        )

        # Alert preferences
        st.markdown("#### 🔔 Alert Preferences")
        high_alerts = st.checkbox("High Risk Alerts", value=True)
        medium_alerts = st.checkbox("Medium Risk Alerts", value=True)
        low_alerts = st.checkbox("Low Risk Alerts", value=False)

        if st.button("💾 Save Preferences", use_container_width=True):
            UserPreferencesService.save_risk_settings({
                'risk_tolerance': risk_tolerance.lower(),
                'alert_distance': alert_distance
            })

            UserPreferencesService.save_alert_preferences({
                'high_risk_alerts': high_alerts,
                'medium_risk_alerts': medium_alerts,
                'low_risk_alerts': low_alerts
            })

            st.success("✅ Preferences saved!")

