"""
Emergency Contacts Service - Microservice for emergency contact management
"""
import streamlit as st
from typing import Dict, List
import urllib.parse

class EmergencyContactsService:
    """Service for managing emergency contacts and SOS functionality"""

    # Nashville emergency contacts
    EMERGENCY_CONTACTS = {
        '911': {
            'name': 'Emergency Services',
            'phone': '911',
            'description': 'General emergency (police, fire, medical)',
            'icon': '🚨'
        },
        'police': {
            'name': 'Nashville Police',
            'phone': '6158628600',
            'description': 'Metro Nashville Police Department',
            'icon': '👮'
        },
        'hospital': {
            'name': 'Emergency Room',
            'phone': '6153421000',
            'description': 'Vanderbilt University Medical Center',
            'icon': '🏥'
        },
        'fire': {
            'name': 'Fire Department',
            'phone': '6158628600',
            'description': 'Nashville Fire Department',
            'icon': '🚒'
        },
        'non_emergency': {
            'name': 'Non-Emergency',
            'phone': '6158628600',
            'description': 'Non-emergency police line',
            'icon': '📞'
        }
    }

    @staticmethod
    def get_emergency_contacts() -> Dict:
        """Get all emergency contacts"""
        return EmergencyContactsService.EMERGENCY_CONTACTS

    @staticmethod
    def generate_share_location_link(latitude: float, longitude: float, label: str = "My Location") -> str:
        """
        Generate shareable location link for emergency contacts

        Args:
            latitude: Location latitude
            longitude: Location longitude
            label: Optional label

        Returns:
            Google Maps URL
        """
        return f"https://www.google.com/maps?q={latitude},{longitude}&label={urllib.parse.quote(label)}"

    @staticmethod
    def generate_sos_message(latitude: float, longitude: float, context: str = "") -> str:
        """
        Generate SOS message with location

        Args:
            latitude: Current latitude
            longitude: Current longitude
            context: Additional context

        Returns:
            Formatted SOS message
        """
        location_link = EmergencyContactsService.generate_share_location_link(latitude, longitude, "EMERGENCY")

        message = f"""
🚨 EMERGENCY - NEED HELP

📍 My Location: {latitude:.6f}, {longitude:.6f}
🔗 View on Map: {location_link}

{context if context else "I need immediate assistance."}

Please share this location with emergency services.
        """.strip()

        return message

    @staticmethod
    def render_emergency_panel() -> None:
        """Render emergency contacts panel in UI"""
        st.markdown("### 🚨 Emergency Contacts")

        contacts = EmergencyContactsService.get_emergency_contacts()

        # Primary emergency (911)
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
                    padding: 1.5rem; border-radius: 10px; text-align: center; margin: 1rem 0;">
            <h2 style="color: white; margin: 0;">🚨 911</h2>
            <p style="color: white; margin: 0.5rem 0;">Emergency Services</p>
            <a href="tel:911" style="color: white; font-size: 1.5rem; font-weight: bold; text-decoration: none;">
                📞 Call Now
            </a>
        </div>
        """, unsafe_allow_html=True)

        # Other emergency contacts
        col1, col2 = st.columns(2)

        with col1:
            police = contacts['police']
            st.markdown(f"""
            <div style="background: #4facfe; padding: 1rem; border-radius: 10px; text-align: center; margin: 0.5rem 0;">
                <h3 style="color: white; margin: 0;">{police['icon']} {police['name']}</h3>
                <p style="color: white; margin: 0.5rem 0; font-size: 0.9rem;">{police['description']}</p>
                <a href="tel:{police['phone']}" style="color: white; font-weight: bold; text-decoration: none;">
                    📞 {police['phone']}
                </a>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            hospital = contacts['hospital']
            st.markdown(f"""
            <div style="background: #11998e; padding: 1rem; border-radius: 10px; text-align: center; margin: 0.5rem 0;">
                <h3 style="color: white; margin: 0;">{hospital['icon']} {hospital['name']}</h3>
                <p style="color: white; margin: 0.5rem 0; font-size: 0.9rem;">{hospital['description']}</p>
                <a href="tel:{hospital['phone']}" style="color: white; font-weight: bold; text-decoration: none;">
                    📞 {hospital['phone']}
                </a>
            </div>
            """, unsafe_allow_html=True)

        # Share location feature
        st.markdown("---")
        st.markdown("### 📍 Share My Location")

        if st.button("🚨 Generate SOS Message", use_container_width=True):
            # Get user location from session state
            user_lat = st.session_state.get('user_lat')
            user_lon = st.session_state.get('user_lon')

            if user_lat and user_lon:
                sos_message = EmergencyContactsService.generate_sos_message(user_lat, user_lon)
                st.text_area("SOS Message (copy and share):", sos_message, height=150)

                location_link = EmergencyContactsService.generate_share_location_link(user_lat, user_lon, "EMERGENCY")
                st.markdown(f"[📍 View Location on Map]({location_link})")
            else:
                st.warning("Please enable location tracking first to generate SOS message.")

    @staticmethod
    def render_floating_sos_button() -> None:
        """Render floating SOS button (for mobile)"""
        st.markdown("""
        <div style="position: fixed; bottom: 20px; right: 20px; z-index: 1000;">
            <a href="tel:911" style="background: #ff6b6b; color: white;
               padding: 1rem 1.5rem; border-radius: 50px; text-decoration: none;
               font-weight: bold; box-shadow: 0 4px 8px rgba(0,0,0,0.3);
               display: block; text-align: center;">
                🚨 SOS
            </a>
        </div>
        """, unsafe_allow_html=True)

