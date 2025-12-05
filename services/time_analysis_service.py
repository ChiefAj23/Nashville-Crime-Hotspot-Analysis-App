"""
Time-of-Day Risk Analysis Service - Microservice for time-based risk analysis
"""
import streamlit as st
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json

class TimeAnalysisService:
    """Service for analyzing crime patterns by time of day"""

    # Risk thresholds by hour (0-23)
    # Based on typical crime patterns: higher risk at night
    HOUR_RISK_LEVELS = {
        'High': [22, 23, 0, 1, 2, 3, 4],  # 10 PM - 4 AM
        'Medium': [5, 6, 19, 20, 21],      # Early morning, evening
        'Low': [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]  # Daytime
    }

    @staticmethod
    def load_time_data() -> Optional[pd.DataFrame]:
        """Load crime data with time information"""
        try:
            data = pd.read_csv('data/processed/cleaned_nashville_911_data.csv', low_memory=False)
            if 'Call Received' in data.columns:
                data['Call Received'] = pd.to_datetime(data['Call Received'], errors='coerce')
                data['Hour'] = data['Call Received'].dt.hour
                data['DayOfWeek'] = data['Call Received'].dt.dayofweek
                data['Month'] = data['Call Received'].dt.month
            return data
        except Exception:
            return None

    @staticmethod
    def analyze_hourly_patterns(hotspot_id: Optional[int] = None) -> Dict[int, int]:
        """
        Analyze crime patterns by hour

        Args:
            hotspot_id: Optional hotspot ID to filter

        Returns:
            Dictionary mapping hour (0-23) to incident count
        """
        data = TimeAnalysisService.load_time_data()
        if data is None or 'Hour' not in data.columns:
            # Return default pattern if no data
            return {hour: 0 for hour in range(24)}

        if hotspot_id is not None:
            # Filter by hotspot location (would need hotspot coordinates)
            pass

        hourly_counts = data['Hour'].value_counts().to_dict()

        # Fill missing hours with 0
        for hour in range(24):
            if hour not in hourly_counts:
                hourly_counts[hour] = 0

        return hourly_counts

    @staticmethod
    def get_risk_by_hour(hotspot: Dict, hour: int) -> str:
        """
        Get risk level for a specific hour

        Args:
            hotspot: Hotspot dictionary
            hour: Hour of day (0-23)

        Returns:
            Risk level: 'High', 'Medium', or 'Low'
        """
        # Check predefined risk levels
        for risk_level, hours in TimeAnalysisService.HOUR_RISK_LEVELS.items():
            if hour in hours:
                # Adjust based on hotspot severity
                if hotspot.get('severity') == 'High' and risk_level != 'High':
                    return 'Medium'  # Upgrade risk for high-severity hotspots
                return risk_level

        return 'Medium'  # Default

    @staticmethod
    def get_safe_hours(hotspot: Dict) -> List[int]:
        """
        Get list of safe hours for a hotspot

        Args:
            hotspot: Hotspot dictionary

        Returns:
            List of safe hours (0-23)
        """
        safe_hours = []

        # Get hourly patterns if available
        hourly_patterns = TimeAnalysisService.analyze_hourly_patterns()

        # Find hours with lowest activity
        if hourly_patterns:
            avg_incidents = sum(hourly_patterns.values()) / len(hourly_patterns)
            for hour, count in hourly_patterns.items():
                if count < avg_incidents * 0.5:  # Less than 50% of average
                    safe_hours.append(hour)

        # If no data, use default safe hours (daytime)
        if not safe_hours:
            safe_hours = TimeAnalysisService.HOUR_RISK_LEVELS['Low']

        return sorted(safe_hours)

    @staticmethod
    def get_peak_crime_hours(hotspot: Dict) -> List[int]:
        """
        Get peak crime hours for a hotspot

        Args:
            hotspot: Hotspot dictionary

        Returns:
            List of peak hours (0-23)
        """
        peak_hours = []

        hourly_patterns = TimeAnalysisService.analyze_hourly_patterns()

        if hourly_patterns:
            max_incidents = max(hourly_patterns.values())
            threshold = max_incidents * 0.7  # 70% of peak

            for hour, count in hourly_patterns.items():
                if count >= threshold:
                    peak_hours.append(hour)

        # If no data, use default high-risk hours
        if not peak_hours:
            peak_hours = TimeAnalysisService.HOUR_RISK_LEVELS['High']

        return sorted(peak_hours)

    @staticmethod
    def get_current_risk_level(hotspot: Dict) -> str:
        """
        Get current time risk level for a hotspot

        Args:
            hotspot: Hotspot dictionary

        Returns:
            Current risk level
        """
        current_hour = datetime.now().hour
        return TimeAnalysisService.get_risk_by_hour(hotspot, current_hour)

    @staticmethod
    def get_time_recommendation(hotspot: Dict) -> str:
        """
        Get time-based safety recommendation

        Args:
            hotspot: Hotspot dictionary

        Returns:
            Recommendation text
        """
        current_hour = datetime.now().hour
        risk_level = TimeAnalysisService.get_risk_by_hour(hotspot, current_hour)
        safe_hours = TimeAnalysisService.get_safe_hours(hotspot)

        if risk_level == 'High':
            if safe_hours:
                safe_time_str = ", ".join([f"{h}:00" for h in safe_hours[:3]])
                return f"⚠️ High risk at current time. Consider visiting during safer hours: {safe_time_str}"
            return "⚠️ High risk area. Exercise extreme caution, especially at night."
        elif risk_level == 'Medium':
            return "🔶 Moderate risk. Stay alert and avoid isolated areas."
        else:
            return "✅ Relatively safe time. Normal precautions apply."

    @staticmethod
    def render_time_filter_ui() -> Dict:
        """Render time-based filter UI"""
        st.markdown("### ⏰ Time-Based Filter")

        current_hour = datetime.now().hour

        time_filter = st.selectbox(
            "Filter by Time:",
            [
                "Current Time",
                "Morning (6-12)",
                "Afternoon (12-18)",
                "Evening (18-22)",
                "Night (22-6)",
                "All Day"
            ],
            help="Filter hotspots by time of day risk levels"
        )

        filter_info = {
            'type': time_filter,
            'current_hour': current_hour
        }

        if time_filter != "All Day":
            st.info(f"💡 Current time: {current_hour}:00 - Risk levels adjusted for {time_filter}")

        return filter_info

    @staticmethod
    def filter_hotspots_by_time(hotspots: List[Dict], time_filter: Dict) -> List[Dict]:
        """
        Filter hotspots based on time filter

        Args:
            hotspots: List of hotspots
            time_filter: Filter configuration

        Returns:
            Filtered hotspots with time-based risk
        """
        filter_type = time_filter.get('type', 'All Day')
        current_hour = time_filter.get('current_hour', datetime.now().hour)

        if filter_type == "All Day":
            return hotspots

        # Define hour ranges
        hour_ranges = {
            "Morning (6-12)": range(6, 12),
            "Afternoon (12-18)": range(12, 18),
            "Evening (18-22)": range(18, 22),
            "Night (22-6)": list(range(22, 24)) + list(range(0, 6)),
            "Current Time": [current_hour]
        }

        if filter_type not in hour_ranges:
            return hotspots

        target_hours = hour_ranges[filter_type]

        # Add time-based risk to hotspots
        filtered = []
        for hotspot in hotspots:
            # Check risk for target hours
            risks = [TimeAnalysisService.get_risk_by_hour(hotspot, h) for h in target_hours]
            avg_risk = 'High' if 'High' in risks else ('Medium' if 'Medium' in risks else 'Low')

            # Add time-adjusted risk
            hotspot_copy = hotspot.copy()
            hotspot_copy['time_risk'] = avg_risk
            filtered.append(hotspot_copy)

        return filtered

