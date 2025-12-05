"""
Test cases for User Preferences Service
TDD: Tests written before implementation
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestUserPreferencesService(unittest.TestCase):
    """Test cases for UserPreferencesService"""

    def test_save_favorite_location_exists(self):
        """Test that save_favorite_location method exists"""
        from services.user_preferences_service import UserPreferencesService
        self.assertTrue(hasattr(UserPreferencesService, 'save_favorite_location'))

    def test_get_favorites_exists(self):
        """Test that get_favorites method exists"""
        from services.user_preferences_service import UserPreferencesService
        self.assertTrue(hasattr(UserPreferencesService, 'get_favorites'))

    def test_save_risk_settings_exists(self):
        """Test that save_risk_settings method exists"""
        from services.user_preferences_service import UserPreferencesService
        self.assertTrue(hasattr(UserPreferencesService, 'save_risk_settings'))

    def test_get_risk_settings_exists(self):
        """Test that get_risk_settings method exists"""
        from services.user_preferences_service import UserPreferencesService
        self.assertTrue(hasattr(UserPreferencesService, 'get_risk_settings'))

    def test_favorite_location_structure(self):
        """Test that favorite locations have correct structure"""
        from services.user_preferences_service import UserPreferencesService

        location = {
            'name': 'Test Location',
            'latitude': 36.1627,
            'longitude': -86.7816
        }

        UserPreferencesService.save_favorite_location(location)
        favorites = UserPreferencesService.get_favorites()

        self.assertIsInstance(favorites, list)
        if favorites:
            self.assertIn('name', favorites[0])
            self.assertIn('latitude', favorites[0])
            self.assertIn('longitude', favorites[0])

if __name__ == '__main__':
    unittest.main()

