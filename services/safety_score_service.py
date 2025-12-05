"""
Safety Score Calculator Service - Microservice for calculating area safety scores
"""
import streamlit as st
from typing import Dict, List, Tuple
import numpy as np

class SafetyScoreService:
    """Service for calculating safety scores for locations"""

    # Weighting factors for different risk components
    WEIGHTS = {
        'high_risk': 3.0,
        'medium_risk': 2.0,
        'low_risk': 1.0,
        'proximity': 1.5,  # Penalty for being near hotspots
        'incident_count': 0.1
    }

    MAX_SAFETY_SCORE = 100
    MIN_SAFETY_SCORE = 0

    @staticmethod
    def calculate_hotspot_score(hotspot: Dict) -> float:
        """
        Calculate safety score for a single hotspot (0-100)
        Lower score = more dangerous

        Args:
            hotspot: Hotspot dictionary

        Returns:
            Safety score (0-100, lower is worse)
        """
        total_incidents = hotspot.get('total_incidents', 0)
        high_risk = hotspot.get('high_risk_count', 0)
        medium_risk = hotspot.get('medium_risk_count', 0)
        low_risk = hotspot.get('low_risk_count', 0)

        # Calculate risk penalty
        risk_penalty = (
            high_risk * SafetyScoreService.WEIGHTS['high_risk'] +
            medium_risk * SafetyScoreService.WEIGHTS['medium_risk'] +
            low_risk * SafetyScoreService.WEIGHTS['low_risk']
        )

        # Normalize by total incidents
        if total_incidents > 0:
            normalized_penalty = risk_penalty / total_incidents
        else:
            normalized_penalty = 0

        # Calculate score (inverse relationship)
        base_score = SafetyScoreService.MAX_SAFETY_SCORE - (normalized_penalty * 10)

        # Apply severity multiplier
        severity_multiplier = {
            'High': 0.5,
            'Medium': 0.7,
            'Low': 0.9
        }.get(hotspot.get('severity', 'Medium'), 0.7)

        score = base_score * severity_multiplier

        # Clamp to valid range
        return max(SafetyScoreService.MIN_SAFETY_SCORE,
                  min(SafetyScoreService.MAX_SAFETY_SCORE, score))

    @staticmethod
    def calculate_location_score(
        latitude: float,
        longitude: float,
        hotspots: List[Dict],
        radius_meters: float = 1000
    ) -> Tuple[float, Dict]:
        """
        Calculate safety score for a specific location

        Args:
            latitude: Location latitude
            longitude: Location longitude
            hotspots: List of all hotspots
            radius_meters: Radius to consider (default 1km)

        Returns:
            Tuple of (safety_score, details_dict)
        """
        # Import distance service
        try:
            from .distance_service import DistanceService
        except ImportError:
            # Fallback for direct import
            from services.distance_service import DistanceService

        nearby_hotspots = []
        proximity_penalty = 0

        for hotspot in hotspots:
            distance = DistanceService.haversine_distance(
                latitude, longitude,
                hotspot['latitude'], hotspot['longitude']
            )

            if distance <= radius_meters:
                nearby_hotspots.append({
                    'hotspot': hotspot,
                    'distance': distance
                })

                # Calculate proximity penalty (closer = worse)
                distance_factor = 1 - (distance / radius_meters)  # 1.0 when at center, 0.0 at edge
                hotspot_score = SafetyScoreService.calculate_hotspot_score(hotspot)
                proximity_penalty += (100 - hotspot_score) * distance_factor * SafetyScoreService.WEIGHTS['proximity']

        # Start with perfect score
        base_score = SafetyScoreService.MAX_SAFETY_SCORE

        # Apply penalties
        if nearby_hotspots:
            # Average proximity penalty
            avg_proximity_penalty = proximity_penalty / len(nearby_hotspots)
            base_score -= min(avg_proximity_penalty, 80)  # Cap penalty at 80

        # Clamp to valid range
        final_score = max(SafetyScoreService.MIN_SAFETY_SCORE,
                         min(SafetyScoreService.MAX_SAFETY_SCORE, base_score))

        # Determine safety level
        if final_score >= 80:
            safety_level = "Very Safe"
            color = "green"
        elif final_score >= 60:
            safety_level = "Safe"
            color = "lightgreen"
        elif final_score >= 40:
            safety_level = "Moderate Risk"
            color = "orange"
        elif final_score >= 20:
            safety_level = "High Risk"
            color = "red"
        else:
            safety_level = "Very High Risk"
            color = "darkred"

        return final_score, {
            'score': final_score,
            'safety_level': safety_level,
            'color': color,
            'nearby_hotspots': len(nearby_hotspots),
            'radius_meters': radius_meters,
            'hotspot_details': nearby_hotspots
        }

    @staticmethod
    def get_safety_recommendation(score: float) -> str:
        """
        Get safety recommendation based on score

        Args:
            score: Safety score (0-100)

        Returns:
            Recommendation text
        """
        if score >= 80:
            return "✅ This area is generally safe. Normal precautions apply."
        elif score >= 60:
            return "⚠️ This area is relatively safe. Stay alert and aware of your surroundings."
        elif score >= 40:
            return "🔶 Exercise caution in this area. Avoid isolated locations, especially at night."
        elif score >= 20:
            return "🔴 High risk area. Strongly recommend avoiding, especially at night. If you must visit, stay in well-lit, populated areas."
        else:
            return "🚨 Very high risk area. Strongly avoid if possible. Use well-lit routes and travel with others."

    @staticmethod
    def render_score_calculator(hotspots: List[Dict]) -> None:
        """Render safety score calculator UI"""
        st.markdown("### 🛡️ Safety Score Calculator")

        st.markdown("Calculate the safety score for any location in Nashville")

        col1, col2 = st.columns(2)

        with col1:
            calc_lat = st.number_input(
                "Latitude",
                value=36.1627,
                format="%.6f",
                key="calc_lat"
            )

        with col2:
            calc_lon = st.number_input(
                "Longitude",
                value=-86.7816,
                format="%.6f",
                key="calc_lon"
            )

        radius = st.slider(
            "Search Radius (meters)",
            min_value=100,
            max_value=5000,
            value=1000,
            step=100,
            help="Radius to consider nearby hotspots"
        )

        if st.button("🔍 Calculate Safety Score", use_container_width=True):
            score, details = SafetyScoreService.calculate_location_score(
                calc_lat, calc_lon, hotspots, radius
            )

            # Display score
            st.markdown("---")

            # Score display with color
            score_color = details['color']
            st.markdown(f"""
            <div style="text-align: center; padding: 2rem;
                        background: linear-gradient(135deg, #{score_color}22 0%, #{score_color}44 100%);
                        border-radius: 10px; margin: 1rem 0;">
                <h1 style="font-size: 4rem; margin: 0; color: {score_color};">
                    {score:.1f}/100
                </h1>
                <h2 style="margin: 0.5rem 0; color: {score_color};">
                    {details['safety_level']}
                </h2>
            </div>
            """, unsafe_allow_html=True)

            # Recommendation
            recommendation = SafetyScoreService.get_safety_recommendation(score)
            st.info(recommendation)

            # Details
            st.markdown("---")
            st.markdown("### 📊 Score Details")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Nearby Hotspots", details['nearby_hotspots'])
            with col2:
                st.metric("Search Radius", f"{radius}m")
            with col3:
                st.metric("Safety Level", details['safety_level'])

            # Nearby hotspots list
            if details['hotspot_details']:
                st.markdown("---")
                st.markdown("### ⚠️ Nearby Hotspots")

                for item in details['hotspot_details'][:5]:  # Show top 5
                    hotspot = item['hotspot']
                    distance = item['distance']

                    hotspot_score = SafetyScoreService.calculate_hotspot_score(hotspot)

                    st.markdown(f"""
                    <div style="padding: 1rem; background: #f0f2f6; border-radius: 5px; margin: 0.5rem 0;">
                        <strong>Hotspot #{hotspot['id']}</strong> - {hotspot['severity']} Risk
                        <br>Distance: {distance:.0f}m | Score: {hotspot_score:.1f}/100
                        <br>Incidents: {hotspot['total_incidents']:,}
                    </div>
                    """, unsafe_allow_html=True)

