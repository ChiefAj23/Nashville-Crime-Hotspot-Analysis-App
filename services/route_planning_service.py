"""
Safe Route Planning Service - Microservice for calculating safe routes
"""
import streamlit as st
from typing import List, Dict, Tuple, Optional
import numpy as np
from .distance_service import DistanceService

class RoutePlanningService:
    """Service for calculating safe routes avoiding hotspots"""

    # Penalty weights for route calculation
    PENALTY_WEIGHTS = {
        'high_risk': 100,
        'medium_risk': 50,
        'low_risk': 10,
        'distance': 1
    }

    @staticmethod
    def calculate_route_penalty(
        start_lat: float, start_lon: float,
        end_lat: float, end_lon: float,
        hotspots: List[Dict]
    ) -> float:
        """
        Calculate penalty for a direct route through hotspots

        Args:
            start_lat: Start latitude
            start_lon: Start longitude
            end_lat: End latitude
            end_lon: End longitude
            hotspots: List of hotspots to avoid

        Returns:
            Total penalty score (higher = more dangerous)
        """
        total_penalty = 0

        # Simple approach: check if route passes near hotspots
        # In production, would use proper routing algorithm

        # Calculate direct distance
        direct_distance = DistanceService.haversine_distance(start_lat, start_lon, end_lat, end_lon)

        # Check each hotspot
        for hotspot in hotspots:
            # Calculate distance from route midpoint to hotspot
            mid_lat = (start_lat + end_lat) / 2
            mid_lon = (start_lon + end_lon) / 2

            distance_to_hotspot = DistanceService.haversine_distance(
                mid_lat, mid_lon,
                hotspot['latitude'], hotspot['longitude']
            )

            # If route passes through or near hotspot
            if distance_to_hotspot < hotspot.get('radius_meters', 500) + 200:  # 200m buffer
                severity = hotspot.get('severity', 'Medium')
                penalty = RoutePlanningService.PENALTY_WEIGHTS.get(f'{severity.lower()}_risk', 50)
                total_penalty += penalty

        return total_penalty

    @staticmethod
    def calculate_route(
        start_lat: float, start_lon: float,
        end_lat: float, end_lon: float,
        hotspots: List[Dict],
        avoid_hotspots: bool = True
    ) -> Dict:
        """
        Calculate safe route from start to end

        Args:
            start_lat: Start latitude
            start_lon: Start longitude
            end_lat: End latitude
            end_lon: End longitude
            hotspots: List of hotspots
            avoid_hotspots: Whether to avoid hotspots

        Returns:
            Route dictionary with waypoints, safety score, distance
        """
        # Calculate direct route
        direct_distance = DistanceService.haversine_distance(start_lat, start_lon, end_lat, end_lon)

        # Simple waypoint calculation (in production, use routing API)
        waypoints = [
            [start_lat, start_lon],
            [end_lat, end_lon]
        ]

        # Calculate safety score
        if avoid_hotspots:
            penalty = RoutePlanningService.calculate_route_penalty(
                start_lat, start_lon, end_lat, end_lon, hotspots
            )
            # Convert penalty to safety score (0-100)
            max_penalty = len(hotspots) * RoutePlanningService.PENALTY_WEIGHTS['high_risk']
            safety_score = max(0, 100 - (penalty / max_penalty * 100)) if max_penalty > 0 else 100
        else:
            safety_score = 50  # Neutral if not avoiding

        return {
            'waypoints': waypoints,
            'safety_score': safety_score,
            'distance_meters': direct_distance,
            'route_type': 'direct',
            'hotspots_avoided': len([h for h in hotspots if RoutePlanningService._route_near_hotspot(
                waypoints, h
            )]) if avoid_hotspots else 0
        }

    @staticmethod
    def _route_near_hotspot(waypoints: List[List[float]], hotspot: Dict) -> bool:
        """Check if route passes near a hotspot"""
        for waypoint in waypoints:
            distance = DistanceService.haversine_distance(
                waypoint[0], waypoint[1],
                hotspot['latitude'], hotspot['longitude']
            )
            if distance < hotspot.get('radius_meters', 500) + 200:
                return True
        return False

    @staticmethod
    def get_alternative_routes(
        start_lat: float, start_lon: float,
        end_lat: float, end_lon: float,
        hotspots: List[Dict],
        num_alternatives: int = 3
    ) -> List[Dict]:
        """
        Generate alternative routes

        Args:
            start_lat: Start latitude
            start_lon: Start longitude
            end_lat: End latitude
            end_lon: End longitude
            hotspots: List of hotspots
            num_alternatives: Number of alternative routes to generate

        Returns:
            List of alternative routes
        """
        alternatives = []

        # Generate alternative waypoints (simple approach)
        # In production, would use proper routing algorithm with waypoint optimization

        for i in range(num_alternatives):
            # Create offset waypoint
            offset_lat = (start_lat + end_lat) / 2 + (i - 1) * 0.01  # Small offset
            offset_lon = (start_lon + end_lon) / 2 + (i - 1) * 0.01

            alt_waypoints = [
                [start_lat, start_lon],
                [offset_lat, offset_lon],
                [end_lat, end_lon]
            ]

            # Calculate safety for this route
            penalty = 0
            for hotspot in hotspots:
                for waypoint in alt_waypoints:
                    distance = DistanceService.haversine_distance(
                        waypoint[0], waypoint[1],
                        hotspot['latitude'], hotspot['longitude']
                    )
                    if distance < hotspot.get('radius_meters', 500) + 200:
                        severity = hotspot.get('severity', 'Medium')
                        penalty += RoutePlanningService.PENALTY_WEIGHTS.get(f'{severity.lower()}_risk', 50)

            max_penalty = len(hotspots) * RoutePlanningService.PENALTY_WEIGHTS['high_risk']
            safety_score = max(0, 100 - (penalty / max_penalty * 100)) if max_penalty > 0 else 100

            # Calculate total distance
            total_distance = 0
            for j in range(len(alt_waypoints) - 1):
                total_distance += DistanceService.haversine_distance(
                    alt_waypoints[j][0], alt_waypoints[j][1],
                    alt_waypoints[j+1][0], alt_waypoints[j+1][1]
                )

            alternatives.append({
                'waypoints': alt_waypoints,
                'safety_score': safety_score,
                'distance_meters': total_distance,
                'route_type': f'alternative_{i+1}',
                'hotspots_avoided': len([h for h in hotspots if RoutePlanningService._route_near_hotspot(alt_waypoints, h)])
            })

        # Sort by safety score (highest first)
        alternatives.sort(key=lambda x: x['safety_score'], reverse=True)
        return alternatives

    @staticmethod
    def render_route_planner(hotspots: List[Dict]) -> None:
        """Render route planning UI"""
        st.markdown("### 🗺️ Safe Route Planner")
        st.markdown("Plan your route avoiding high-risk areas")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📍 Starting Point")
            start_lat = st.number_input("Latitude", value=36.1627, format="%.6f", key="route_start_lat")
            start_lon = st.number_input("Longitude", value=-86.7816, format="%.6f", key="route_start_lon")

        with col2:
            st.markdown("#### 🎯 Destination")
            end_lat = st.number_input("Latitude", value=36.2000, format="%.6f", key="route_end_lat")
            end_lon = st.number_input("Longitude", value=-86.8000, format="%.6f", key="route_end_lon")

        avoid_hotspots = st.checkbox("Avoid High-Risk Hotspots", value=True)

        if st.button("🔍 Calculate Safe Route", use_container_width=True):
            route = RoutePlanningService.calculate_route(
                start_lat, start_lon, end_lat, end_lon, hotspots, avoid_hotspots
            )

            # Display route
            st.markdown("---")
            st.markdown("### 📊 Route Details")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Safety Score", f"{route['safety_score']:.1f}/100")
            with col2:
                st.metric("Distance", f"{route['distance_meters']:.0f}m")
            with col3:
                st.metric("Hotspots Avoided", route['hotspots_avoided'])

            # Safety recommendation
            if route['safety_score'] >= 80:
                st.success("✅ This route is relatively safe!")
            elif route['safety_score'] >= 60:
                st.warning("⚠️ This route has moderate risk. Exercise caution.")
            else:
                st.error("🚨 This route passes through high-risk areas. Consider alternatives.")

            # Alternative routes
            st.markdown("---")
            st.markdown("### 🔄 Alternative Routes")

            alternatives = RoutePlanningService.get_alternative_routes(
                start_lat, start_lon, end_lat, end_lon, hotspots, 3
            )

            for i, alt_route in enumerate(alternatives, 1):
                with st.expander(f"Alternative Route {i} - Safety: {alt_route['safety_score']:.1f}/100"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Distance", f"{alt_route['distance_meters']:.0f}m")
                    with col2:
                        st.metric("Hotspots Avoided", alt_route['hotspots_avoided'])

                    if alt_route['safety_score'] > route['safety_score']:
                        st.info("💡 This alternative is safer than the direct route!")

