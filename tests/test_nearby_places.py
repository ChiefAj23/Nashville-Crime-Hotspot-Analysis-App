"""
Test cases for Nearby Safe Places Service
TDD: Tests written before implementation
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestNearbyPlacesService(unittest.TestCase):
    """Test cases for NearbyPlacesService"""

    def setUp(self):
        """Set up test fixtures"""
        self.lat, self.lon = 36.1627, -86.7816  # Nashville center
        self.radius = 1000  # 1km

    def test_find_police_stations_exists(self):
        """Test that find_police_stations method exists"""
        from services.nearby_places_service import NearbyPlacesService
        self.assertTrue(hasattr(NearbyPlacesService, 'find_police_stations'))

    def test_find_hospitals_exists(self):
        """Test that find_hospitals method exists"""
        from services.nearby_places_service import NearbyPlacesService
        self.assertTrue(hasattr(NearbyPlacesService, 'find_hospitals'))

    def test_find_safe_places_structure(self):
        """Test that safe places have correct structure"""
        from services.nearby_places_service import NearbyPlacesService

        places = NearbyPlacesService.find_police_stations(self.lat, self.lon, self.radius)

        if places:  # If places are found
            place = places[0]
            self.assertIn('name', place)
            self.assertIn('latitude', place)
            self.assertIn('longitude', place)
            self.assertIn('distance', place)

    def test_places_have_distance(self):
        """Test that places include distance"""
        from services.nearby_places_service import NearbyPlacesService

        places = NearbyPlacesService.find_hospitals(self.lat, self.lon, self.radius)

        if places:
            for place in places:
                self.assertIn('distance', place)
                self.assertIsInstance(place['distance'], (int, float))

    def test_find_safe_restaurants_exists(self):
        """Test that find_safe_restaurants method exists"""
        from services.nearby_places_service import NearbyPlacesService
        self.assertTrue(hasattr(NearbyPlacesService, 'find_safe_restaurants'))

if __name__ == '__main__':
    unittest.main()

