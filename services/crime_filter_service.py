"""
Crime Filter Service - Microservice for filtering hotspots by crime type
"""
import streamlit as st
from typing import List, Dict, Set

class CrimeFilterService:
    """Service for filtering hotspots by crime type"""

    CRIME_CATEGORIES = {
        'Violent Crime': ['SHOTS FIRED', 'PERSON WITH WEAPON', 'HOLDUP / ROBBERY', 'FIGHT / ASSAULT'],
        'Property Crime': ['BURGLARY - RESIDENCE', 'BURGLARY - NON-RESIDENCE', 'THEFT'],
        'Traffic': ['TRAFFIC VIOLATION', 'VEHICLE ACCIDENT - PROPERTY DAMAGE',
                   'VEHICLE ACCIDENT - PERSONAL INJURY', 'VEHICLE BLOCKING RIGHT OF WAY'],
        'Public Safety': ['SAFETY HAZARD', 'DISORDERLY PERSON', 'DANGEROUS / INJURED ANIMAL'],
        'Police Activity': ['WANT OFFICER FOR INVESTIGATION / ASSISTA', 'INVESTIGATE 911 HANG-UP CALL',
                          'SUSPICIOUS PERSON', 'MISSING PERSON', 'COMMUNITY POLICING ACTIVITY'],
        'Medical': ['VEHICLE ACCIDENT - PERSONAL INJURY', 'FIGHT / ASSAULT']
    }

    @staticmethod
    def get_crime_types_from_hotspots(hotspots: List[Dict]) -> Set[str]:
        """
        Extract unique crime types from hotspots

        Args:
            hotspots: List of hotspot dictionaries

        Returns:
            Set of unique crime types
        """
        crime_types = set()
        for hotspot in hotspots:
            if 'top_incidents' in hotspot:
                crime_types.update(hotspot['top_incidents'].keys())
        return crime_types

    @staticmethod
    def categorize_crime_type(incident_type: str) -> str:
        """
        Categorize an incident type into a category

        Args:
            incident_type: Name of the incident type

        Returns:
            Category name or 'Other'
        """
        incident_upper = str(incident_type).upper()

        for category, types in CrimeFilterService.CRIME_CATEGORIES.items():
            if any(crime_type in incident_upper for crime_type in types):
                return category

        return 'Other'

    @staticmethod
    def filter_by_crime_type(hotspots: List[Dict], selected_types: List[str]) -> List[Dict]:
        """
        Filter hotspots by selected crime types

        Args:
            hotspots: List of hotspot dictionaries
            selected_types: List of crime type names to filter by

        Returns:
            Filtered list of hotspots
        """
        if not selected_types:
            return hotspots

        filtered = []
        for hotspot in hotspots:
            if 'top_incidents' in hotspot:
                hotspot_types = set(hotspot['top_incidents'].keys())
                # Check if any selected type matches hotspot types
                if any(selected_type in hotspot_types for selected_type in selected_types):
                    filtered.append(hotspot)

        return filtered

    @staticmethod
    def filter_by_category(hotspots: List[Dict], selected_categories: List[str]) -> List[Dict]:
        """
        Filter hotspots by crime category

        Args:
            hotspots: List of hotspot dictionaries
            selected_categories: List of category names to filter by

        Returns:
            Filtered list of hotspots
        """
        if not selected_categories:
            return hotspots

        filtered = []
        for hotspot in hotspots:
            if 'top_incidents' in hotspot:
                hotspot_types = hotspot['top_incidents'].keys()
                hotspot_categories = {
                    CrimeFilterService.categorize_crime_type(crime_type)
                    for crime_type in hotspot_types
                }

                # Check if any selected category matches
                if any(cat in hotspot_categories for cat in selected_categories):
                    filtered.append(hotspot)

        return filtered

    @staticmethod
    def render_filter_ui(hotspots: List[Dict]) -> List[str]:
        """
        Render crime type filter UI in sidebar

        Args:
            hotspots: List of hotspot dictionaries

        Returns:
            List of selected crime types
        """
        st.markdown("### 🔍 Crime Type Filter")

        # Get all unique crime types
        all_crime_types = sorted(CrimeFilterService.get_crime_types_from_hotspots(hotspots))

        # Group by category
        crime_by_category = {}
        for crime_type in all_crime_types:
            category = CrimeFilterService.categorize_crime_type(crime_type)
            if category not in crime_by_category:
                crime_by_category[category] = []
            crime_by_category[category].append(crime_type)

        # Render category filters
        selected_categories = st.multiselect(
            "Filter by Category:",
            options=list(crime_by_category.keys()),
            default=[],
            help="Select crime categories to filter"
        )

        # Get crime types from selected categories
        selected_types = []
        if selected_categories:
            for category in selected_categories:
                selected_types.extend(crime_by_category[category])

        # Also allow direct crime type selection
        st.markdown("---")
        selected_direct_types = st.multiselect(
            "Or select specific crime types:",
            options=all_crime_types[:20],  # Limit to first 20 for UI
            default=[],
            help="Select specific incident types"
        )

        # Combine both selections
        all_selected = list(set(selected_types + selected_direct_types))

        if all_selected:
            st.info(f"🔍 Filtering by {len(all_selected)} crime type(s)")

        return all_selected

    @staticmethod
    def get_hotspot_crime_summary(hotspot: Dict) -> Dict[str, int]:
        """
        Get crime type summary for a hotspot

        Args:
            hotspot: Hotspot dictionary

        Returns:
            Dictionary of crime types and counts
        """
        if 'top_incidents' not in hotspot:
            return {}

        summary = {}
        for crime_type, count in hotspot['top_incidents'].items():
            category = CrimeFilterService.categorize_crime_type(crime_type)
            if category not in summary:
                summary[category] = 0
            summary[category] += count

        return summary

    @staticmethod
    def get_filter_stats(hotspots: List[Dict], filtered: List[Dict]) -> Dict[str, int]:
        """
        Get statistics about filtering

        Args:
            hotspots: Original hotspot list
            filtered: Filtered hotspot list

        Returns:
            Dictionary with filter statistics
        """
        return {
            'total': len(hotspots),
            'filtered': len(filtered),
            'hidden': len(hotspots) - len(filtered),
            'percentage_shown': (len(filtered) / len(hotspots) * 100) if hotspots else 0
        }

