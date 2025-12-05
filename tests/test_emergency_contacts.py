"""
Test cases for Emergency Contacts Service
TDD: Tests written before implementation
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestEmergencyContactsService(unittest.TestCase):
    """Test cases for EmergencyContactsService"""

    def test_get_emergency_contacts_exists(self):
        """Test that get_emergency_contacts method exists"""
        from services.emergency_contacts_service import EmergencyContactsService
        self.assertTrue(hasattr(EmergencyContactsService, 'get_emergency_contacts'))

    def test_emergency_contacts_structure(self):
        """Test that emergency contacts have correct structure"""
        from services.emergency_contacts_service import EmergencyContactsService

        contacts = EmergencyContactsService.get_emergency_contacts()

        self.assertIsInstance(contacts, dict)
        self.assertIn('911', contacts)
        self.assertIn('police', contacts)
        self.assertIn('hospital', contacts)

    def test_contact_has_phone_number(self):
        """Test that each contact has a phone number"""
        from services.emergency_contacts_service import EmergencyContactsService

        contacts = EmergencyContactsService.get_emergency_contacts()

        for key, contact in contacts.items():
            self.assertIn('phone', contact)
            self.assertIsInstance(contact['phone'], str)

    def test_generate_share_location_link(self):
        """Test generating share location link"""
        from services.emergency_contacts_service import EmergencyContactsService

        lat, lon = 36.1627, -86.7816
        link = EmergencyContactsService.generate_share_location_link(lat, lon)

        self.assertIsInstance(link, str)
        self.assertIn(str(lat), link)
        self.assertIn(str(lon), link)

    def test_sos_functionality_exists(self):
        """Test that SOS functionality exists"""
        from services.emergency_contacts_service import EmergencyContactsService
        self.assertTrue(hasattr(EmergencyContactsService, 'generate_sos_message'))

if __name__ == '__main__':
    unittest.main()

