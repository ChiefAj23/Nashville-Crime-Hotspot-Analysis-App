"""
Test cases for Time-of-Day Risk Analysis Service
TDD: Tests written before implementation
"""
import unittest
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestTimeAnalysisService(unittest.TestCase):
    """Test cases for TimeAnalysisService"""

    def setUp(self):
        """Set up test fixtures"""
        self.hotspot = {
            'id': 1,
            'latitude': 36.1627,
            'longitude': -86.7816,
            'total_incidents': 100
        }

    def test_analyze_hourly_patterns_exists(self):
        """Test that analyze_hourly_patterns method exists"""
        from services.time_analysis_service import TimeAnalysisService
        self.assertTrue(hasattr(TimeAnalysisService, 'analyze_hourly_patterns'))

    def test_get_risk_by_hour(self):
        """Test getting risk level for specific hour"""
        from services.time_analysis_service import TimeAnalysisService

        risk = TimeAnalysisService.get_risk_by_hour(self.hotspot, 22)  # 10 PM

        self.assertIn(risk, ['High', 'Medium', 'Low'])

    def test_get_safe_hours(self):
        """Test getting safe hours for a hotspot"""
        from services.time_analysis_service import TimeAnalysisService

        safe_hours = TimeAnalysisService.get_safe_hours(self.hotspot)

        self.assertIsInstance(safe_hours, list)
        self.assertLessEqual(len(safe_hours), 24)

    def test_get_peak_crime_hours(self):
        """Test identifying peak crime hours"""
        from services.time_analysis_service import TimeAnalysisService

        peak_hours = TimeAnalysisService.get_peak_crime_hours(self.hotspot)

        self.assertIsInstance(peak_hours, list)
        self.assertLessEqual(len(peak_hours), 24)

    def test_get_current_risk_level(self):
        """Test getting current time risk level"""
        from services.time_analysis_service import TimeAnalysisService

        current_risk = TimeAnalysisService.get_current_risk_level(self.hotspot)

        self.assertIn(current_risk, ['High', 'Medium', 'Low'])

if __name__ == '__main__':
    unittest.main()

