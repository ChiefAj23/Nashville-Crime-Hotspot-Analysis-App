"""
Historical Trends Service - Microservice for analyzing crime trends over time
"""
import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime
import json

class HistoricalTrendsService:
    """Service for analyzing historical crime trends and patterns"""

    @staticmethod
    def load_crime_data() -> Optional[pd.DataFrame]:
        """Load crime data for trend analysis"""
        try:
            data = pd.read_csv('data/processed/cleaned_nashville_911_data.csv', low_memory=False)
            if 'Call Received' in data.columns:
                data['Call Received'] = pd.to_datetime(data['Call Received'], errors='coerce')
                data['Year'] = data['Call Received'].dt.year
                data['Month'] = data['Call Received'].dt.month
                data['DayOfWeek'] = data['Call Received'].dt.dayofweek
                data['Hour'] = data['Call Received'].dt.hour
            return data
        except Exception:
            return None

    @staticmethod
    def analyze_monthly_trends(hotspots: Optional[List[Dict]] = None) -> Dict[str, int]:
        """
        Analyze monthly crime trends

        Args:
            hotspots: Optional list of hotspots to filter

        Returns:
            Dictionary mapping month names to incident counts
        """
        data = HistoricalTrendsService.load_crime_data()
        if data is None or 'Month' not in data.columns:
            # Return default empty trends
            return {month: 0 for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']}

        monthly_counts = data['Month'].value_counts().to_dict()
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        result = {}
        for i, month_name in enumerate(month_names, 1):
            result[month_name] = monthly_counts.get(i, 0)

        return result

    @staticmethod
    def analyze_seasonal_patterns(hotspots: Optional[List[Dict]] = None) -> Dict[str, int]:
        """
        Analyze seasonal crime patterns

        Args:
            hotspots: Optional list of hotspots to filter

        Returns:
            Dictionary mapping seasons to incident counts
        """
        data = HistoricalTrendsService.load_crime_data()
        if data is None or 'Month' not in data.columns:
            return {'Spring': 0, 'Summer': 0, 'Fall': 0, 'Winter': 0}

        # Define seasons
        spring_months = [3, 4, 5]
        summer_months = [6, 7, 8]
        fall_months = [9, 10, 11]
        winter_months = [12, 1, 2]

        seasonal_counts = {
            'Spring': data[data['Month'].isin(spring_months)].shape[0],
            'Summer': data[data['Month'].isin(summer_months)].shape[0],
            'Fall': data[data['Month'].isin(fall_months)].shape[0],
            'Winter': data[data['Month'].isin(winter_months)].shape[0]
        }

        return seasonal_counts

    @staticmethod
    def analyze_day_of_week_patterns(hotspots: Optional[List[Dict]] = None) -> Dict[str, int]:
        """
        Analyze day of week patterns

        Args:
            hotspots: Optional list of hotspots to filter

        Returns:
            Dictionary mapping day names to incident counts
        """
        data = HistoricalTrendsService.load_crime_data()
        if data is None or 'DayOfWeek' not in data.columns:
            day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            return {day: 0 for day in day_names}

        day_counts = data['DayOfWeek'].value_counts().to_dict()
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        result = {}
        for i, day_name in enumerate(day_names):
            result[day_name] = day_counts.get(i, 0)

        return result

    @staticmethod
    def analyze_yearly_trends() -> Dict[int, int]:
        """
        Analyze yearly crime trends

        Returns:
            Dictionary mapping years to incident counts
        """
        data = HistoricalTrendsService.load_crime_data()
        if data is None or 'Year' not in data.columns:
            return {}

        yearly_counts = data['Year'].value_counts().to_dict()
        return yearly_counts

    @staticmethod
    def generate_chart_data(trend_type: str = 'monthly') -> Dict:
        """
        Generate data for chart visualization

        Args:
            trend_type: Type of trend ('monthly', 'seasonal', 'daily', 'yearly')

        Returns:
            Dictionary with chart data
        """
        if trend_type == 'monthly':
            data = HistoricalTrendsService.analyze_monthly_trends()
            return {
                'labels': list(data.keys()),
                'values': list(data.values()),
                'title': 'Monthly Crime Trends'
            }
        elif trend_type == 'seasonal':
            data = HistoricalTrendsService.analyze_seasonal_patterns()
            return {
                'labels': list(data.keys()),
                'values': list(data.values()),
                'title': 'Seasonal Crime Patterns'
            }
        elif trend_type == 'daily':
            data = HistoricalTrendsService.analyze_day_of_week_patterns()
            return {
                'labels': list(data.keys()),
                'values': list(data.values()),
                'title': 'Day of Week Patterns'
            }
        elif trend_type == 'yearly':
            data = HistoricalTrendsService.analyze_yearly_trends()
            return {
                'labels': [str(year) for year in sorted(data.keys())],
                'values': [data[year] for year in sorted(data.keys())],
                'title': 'Yearly Crime Trends'
            }

        return {'labels': [], 'values': [], 'title': 'No Data'}

    @staticmethod
    def render_trends_dashboard() -> None:
        """Render historical trends dashboard"""
        st.markdown("### 📈 Historical Trends & Patterns")

        trend_type = st.selectbox(
            "Select Trend Type:",
            ['Monthly', 'Seasonal', 'Day of Week', 'Yearly'],
            help="Choose the type of trend to analyze"
        )

        chart_data = HistoricalTrendsService.generate_chart_data(trend_type.lower())

        if chart_data['values']:
            # Display as metrics
            st.markdown(f"#### {chart_data['title']}")

            # Create columns for metrics
            cols = st.columns(min(len(chart_data['labels']), 7))
            for i, (label, value) in enumerate(zip(chart_data['labels'], chart_data['values'])):
                if i < len(cols):
                    with cols[i]:
                        st.metric(label, f"{value:,}")

            # Simple bar chart using Streamlit
            st.bar_chart(dict(zip(chart_data['labels'], chart_data['values'])))

            # Insights
            st.markdown("---")
            st.markdown("### 💡 Insights")

            max_value = max(chart_data['values'])
            max_label = chart_data['labels'][chart_data['values'].index(max_value)]
            min_value = min(chart_data['values'])
            min_label = chart_data['labels'][chart_data['values'].index(min_value)]

            st.info(f"📊 **Peak Period:** {max_label} with {max_value:,} incidents")
            st.success(f"✅ **Safest Period:** {min_label} with {min_value:,} incidents")
        else:
            st.warning("No trend data available. Ensure crime data file is loaded.")

