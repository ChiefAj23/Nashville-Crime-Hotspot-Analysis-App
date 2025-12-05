"""
Nearby Safe Places Service - Microservice for finding nearby safe locations
"""
import streamlit as st
from typing import List, Dict, Optional
from .distance_service import DistanceService

class NearbyPlacesService:
    """Service for finding nearby safe places (police, hospitals, etc.)"""

    # Nashville Police Stations (sample data - can be expanded)
    POLICE_STATIONS = [
        {'name': 'Central Precinct', 'latitude': 36.1627, 'longitude': -86.7816, 'address': '601 Korean Veterans Blvd'},
        {'name': 'East Precinct', 'latitude': 36.1800, 'longitude': -86.7500, 'address': '936 E Trinity Ln'},
        {'name': 'West Precinct', 'latitude': 36.1400, 'longitude': -86.8200, 'address': '5500 Charlotte Pike'},
        {'name': 'North Precinct', 'latitude': 36.2200, 'longitude': -86.7800, 'address': '2231 26th Ave N'},
        {'name': 'South Precinct', 'latitude': 36.1000, 'longitude': -86.7500, 'address': '4715 Trousdale Dr'},
        {'name': 'Hermitage Precinct', 'latitude': 36.1900, 'longitude': -86.6100, 'address': '3701 James Kay Ln'},
        {'name': 'Madison Precinct', 'latitude': 36.2600, 'longitude': -86.7100, 'address': '400 Myatt Dr'},
    ]

    # Nashville Hospitals (sample data)
    HOSPITALS = [
        {'name': 'Vanderbilt University Medical Center', 'latitude': 36.1447, 'longitude': -86.8027, 'address': '1211 Medical Center Dr'},
        {'name': 'TriStar Centennial Medical Center', 'latitude': 36.1347, 'longitude': -86.7897, 'address': '2300 Patterson St'},
        {'name': 'Saint Thomas Midtown Hospital', 'latitude': 36.1500, 'longitude': -86.7900, 'address': '2000 Church St'},
        {'name': 'Nashville General Hospital', 'latitude': 36.1600, 'longitude': -86.7600, 'address': '1818 Albion St'},
    ]

    # Safe areas (well-lit, populated areas)
    SAFE_AREAS = [
        {'name': 'Downtown Nashville', 'latitude': 36.1627, 'longitude': -86.7816, 'type': 'Tourist Area'},
        {'name': 'Music Row', 'latitude': 36.1500, 'longitude': -86.7900, 'type': 'Entertainment'},
        {'name': 'Gulch District', 'latitude': 36.1500, 'longitude': -86.7800, 'type': 'Commercial'},
    ]

    @staticmethod
    def find_police_stations(latitude: float, longitude: float, radius_meters: float = 5000) -> List[Dict]:
        """
        Find nearby police stations

        Args:
            latitude: User latitude
            longitude: User longitude
            radius_meters: Search radius in meters

        Returns:
            List of nearby police stations with distance
        """
        nearby = []

        for station in NearbyPlacesService.POLICE_STATIONS:
            distance = DistanceService.haversine_distance(
                latitude, longitude,
                station['latitude'], station['longitude']
            )

            if distance <= radius_meters:
                station_copy = station.copy()
                station_copy['distance'] = distance
                station_copy['type'] = 'Police Station'
                nearby.append(station_copy)

        # Sort by distance
        nearby.sort(key=lambda x: x['distance'])
        return nearby

    @staticmethod
    def find_hospitals(latitude: float, longitude: float, radius_meters: float = 5000) -> List[Dict]:
        """
        Find nearby hospitals

        Args:
            latitude: User latitude
            longitude: User longitude
            radius_meters: Search radius in meters

        Returns:
            List of nearby hospitals with distance
        """
        nearby = []

        for hospital in NearbyPlacesService.HOSPITALS:
            distance = DistanceService.haversine_distance(
                latitude, longitude,
                hospital['latitude'], hospital['longitude']
            )

            if distance <= radius_meters:
                hospital_copy = hospital.copy()
                hospital_copy['distance'] = distance
                hospital_copy['type'] = 'Hospital'
                nearby.append(hospital_copy)

        # Sort by distance
        nearby.sort(key=lambda x: x['distance'])
        return nearby

    @staticmethod
    def find_safe_restaurants(latitude: float, longitude: float, radius_meters: float = 2000) -> List[Dict]:
        """
        Find nearby safe restaurants (well-lit, popular areas)

        Args:
            latitude: User latitude
            longitude: User longitude
            radius_meters: Search radius in meters

        Returns:
            List of safe restaurant areas
        """
        # This would typically use Google Places API
        # For now, return safe areas that likely have restaurants
        safe_areas = []

        for area in NearbyPlacesService.SAFE_AREAS:
            distance = DistanceService.haversine_distance(
                latitude, longitude,
                area['latitude'], area['longitude']
            )

            if distance <= radius_meters:
                area_copy = area.copy()
                area_copy['distance'] = distance
                area_copy['type'] = 'Safe Area'
                area_copy['recommendation'] = 'Well-lit, populated area with restaurants and shops'
                safe_areas.append(area_copy)

        safe_areas.sort(key=lambda x: x['distance'])
        return safe_areas

    @staticmethod
    def find_all_nearby_safe_places(latitude: float, longitude: float, radius_meters: float = 5000) -> Dict[str, List[Dict]]:
        """
        Find all types of nearby safe places

        Args:
            latitude: User latitude
            longitude: User longitude
            radius_meters: Search radius in meters

        Returns:
            Dictionary with all nearby safe places by type
        """
        return {
            'police_stations': NearbyPlacesService.find_police_stations(latitude, longitude, radius_meters),
            'hospitals': NearbyPlacesService.find_hospitals(latitude, longitude, radius_meters),
            'safe_areas': NearbyPlacesService.find_safe_restaurants(latitude, longitude, min(radius_meters, 2000))
        }

    @staticmethod
    def render_nearby_places_ui(latitude: Optional[float] = None, longitude: Optional[float] = None) -> None:
        """Render nearby places UI"""
        st.markdown("### 🏥 Nearby Safe Places")

        if not latitude or not longitude:
            st.info("📍 Enable location tracking to find nearby safe places")
            # Allow manual entry
            col1, col2 = st.columns(2)
            with col1:
                latitude = st.number_input("Latitude", value=36.1627, format="%.6f", key="nearby_lat")
            with col2:
                longitude = st.number_input("Longitude", value=-86.7816, format="%.6f", key="nearby_lon")

        radius = st.slider("Search Radius (meters)", 500, 10000, 2000, 500)

        if st.button("🔍 Find Nearby Places", use_container_width=True):
            places = NearbyPlacesService.find_all_nearby_safe_places(latitude, longitude, radius)

            # Police Stations
            if places['police_stations']:
                st.markdown("#### 👮 Police Stations")
                for station in places['police_stations'][:5]:  # Show top 5
                    st.markdown(f"""
                    <div style="padding: 1rem; background: #e3f2fd; border-radius: 5px; margin: 0.5rem 0;">
                        <strong>{station['name']}</strong><br>
                        📍 {station['address']}<br>
                        📏 {station['distance']:.0f}m away
                    </div>
                    """, unsafe_allow_html=True)

            # Hospitals
            if places['hospitals']:
                st.markdown("#### 🏥 Hospitals")
                for hospital in places['hospitals'][:5]:
                    st.markdown(f"""
                    <div style="padding: 1rem; background: #e8f5e9; border-radius: 5px; margin: 0.5rem 0;">
                        <strong>{hospital['name']}</strong><br>
                        📍 {hospital['address']}<br>
                        📏 {hospital['distance']:.0f}m away
                    </div>
                    """, unsafe_allow_html=True)

            # Safe Areas
            if places['safe_areas']:
                st.markdown("#### ✅ Safe Areas")
                for area in places['safe_areas'][:5]:
                    st.markdown(f"""
                    <div style="padding: 1rem; background: #fff3e0; border-radius: 5px; margin: 0.5rem 0;">
                        <strong>{area['name']}</strong><br>
                        📍 {area.get('recommendation', 'Well-lit, safe area')}<br>
                        📏 {area['distance']:.0f}m away
                    </div>
                    """, unsafe_allow_html=True)

            if not any(places.values()):
                st.warning(f"No safe places found within {radius}m radius. Try increasing the search radius.")

