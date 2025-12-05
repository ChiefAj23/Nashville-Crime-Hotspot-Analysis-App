"""
Distance Service - Utility service for distance calculations
"""
import numpy as np

class DistanceService:
    """Service for calculating distances between locations"""

    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two points using Haversine formula (in meters)

        Args:
            lat1: First point latitude
            lon1: First point longitude
            lat2: Second point latitude
            lon2: Second point longitude

        Returns:
            Distance in meters
        """
        R = 6371000  # Earth radius in meters
        phi1 = np.radians(lat1)
        phi2 = np.radians(lat2)
        delta_phi = np.radians(lat2 - lat1)
        delta_lambda = np.radians(lon2 - lon1)

        a = np.sin(delta_phi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda/2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

        return R * c

