"""
Share Service - Microservice for sharing hotspot locations
"""
import streamlit as st
from typing import Dict, Optional
from datetime import datetime
import urllib.parse

class ShareService:
    """Service for sharing hotspot locations and maps"""

    @staticmethod
    def generate_google_maps_link(latitude: float, longitude: float, label: str = "") -> str:
        """
        Generate Google Maps link for a location

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            label: Optional label for the location

        Returns:
            Google Maps URL
        """
        base_url = "https://www.google.com/maps?q="
        coords = f"{latitude},{longitude}"

        if label:
            label_encoded = urllib.parse.quote(label)
            return f"{base_url}{coords}+({label_encoded})"

        return f"{base_url}{coords}"

    @staticmethod
    def generate_apple_maps_link(latitude: float, longitude: float, label: str = "") -> str:
        """
        Generate Apple Maps link for a location

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            label: Optional label for the location

        Returns:
            Apple Maps URL
        """
        return f"https://maps.apple.com/?ll={latitude},{longitude}&q={label if label else 'Location'}"

    @staticmethod
    def generate_what3words_link(latitude: float, longitude: float) -> str:
        """
        Generate what3words link (if needed)

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate

        Returns:
            what3words URL (requires API for actual conversion)
        """
        # Note: This requires what3words API for actual conversion
        return f"https://what3words.com/?coordinates={latitude},{longitude}"

    @staticmethod
    def create_shareable_text(hotspot: Dict) -> str:
        """
        Create shareable text for a hotspot

        Args:
            hotspot: Hotspot dictionary

        Returns:
            Formatted text string
        """
        text = f"""
🚨 Nashville Safety Alert

Hotspot #{hotspot['id']} - {hotspot['severity']} Risk Area

📍 Location: {hotspot['latitude']:.4f}, {hotspot['longitude']:.4f}
⚠️ Risk Level: {hotspot['severity']}
📊 Total Incidents: {hotspot['total_incidents']:,}

Why avoid?
{hotspot.get('explanation', 'High crime activity in this area')}

View on map: {ShareService.generate_google_maps_link(
    hotspot['latitude'],
    hotspot['longitude'],
    f"Hotspot #{hotspot['id']}"
)}
        """.strip()

        return text

    @staticmethod
    def render_share_buttons(hotspot: Dict) -> None:
        """
        Render share buttons for a hotspot

        Args:
            hotspot: Hotspot dictionary
        """
        st.markdown("### 📤 Share This Hotspot")

        col1, col2, col3 = st.columns(3)

        with col1:
            google_link = ShareService.generate_google_maps_link(
                hotspot['latitude'],
                hotspot['longitude'],
                f"Hotspot #{hotspot['id']}"
            )
            st.markdown(f"[🗺️ View on Google Maps]({google_link})")

        with col2:
            apple_link = ShareService.generate_apple_maps_link(
                hotspot['latitude'],
                hotspot['longitude'],
                f"Hotspot #{hotspot['id']}"
            )
            st.markdown(f"[🍎 View on Apple Maps]({apple_link})")

        with col3:
            share_text = ShareService.create_shareable_text(hotspot)
            st.download_button(
                "📋 Copy Details",
                data=share_text,
                file_name=f"hotspot_{hotspot['id']}_info.txt",
                mime="text/plain",
                use_container_width=True
            )

        # Share text area
        st.markdown("---")
        st.markdown("**Share Text:**")
        st.code(share_text, language="text")

        # Social sharing (for mobile/web)
        st.markdown("---")
        st.markdown("**Quick Share:**")

        share_url = ShareService.generate_google_maps_link(
            hotspot['latitude'],
            hotspot['longitude'],
            f"Hotspot {hotspot['id']}"
        )

        # Create share links
        twitter_text = urllib.parse.quote(
            f"🚨 {hotspot['severity']} Risk Area in Nashville - Hotspot #{hotspot['id']}"
        )
        twitter_link = f"https://twitter.com/intent/tweet?text={twitter_text}&url={urllib.parse.quote(share_url)}"

        whatsapp_text = urllib.parse.quote(ShareService.create_shareable_text(hotspot))
        whatsapp_link = f"https://wa.me/?text={whatsapp_text}"

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"[🐦 Share on Twitter]({twitter_link})")
        with col2:
            st.markdown(f"[💬 Share on WhatsApp]({whatsapp_link})")

    @staticmethod
    def create_shareable_map_link(latitude: float, longitude: float, zoom: int = 15) -> str:
        """
        Create shareable link to view location on map

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            zoom: Zoom level

        Returns:
            Shareable map URL
        """
        return f"https://www.google.com/maps/@?api=1&map_action=map&center={latitude},{longitude}&zoom={zoom}"

    @staticmethod
    def generate_qr_code_data(latitude: float, longitude: float) -> str:
        """
        Generate data for QR code (to be used with QR code generator)

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate

        Returns:
            URL string for QR code
        """
        return ShareService.generate_google_maps_link(latitude, longitude)

    @staticmethod
    def create_bulk_share(hotspots: list) -> str:
        """
        Create shareable text for multiple hotspots

        Args:
            hotspots: List of hotspot dictionaries

        Returns:
            Formatted text string
        """
        text = f"""
🗺️ Nashville Safety Map - {len(hotspots)} Hotspots

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

High-Risk Areas to Avoid:
"""
        for hotspot in hotspots[:10]:  # Limit to first 10
            text += f"""
• Hotspot #{hotspot['id']}: {hotspot['severity']} Risk
  Location: {hotspot['latitude']:.4f}, {hotspot['longitude']:.4f}
  {ShareService.generate_google_maps_link(
      hotspot['latitude'],
      hotspot['longitude'],
      f"Hotspot {hotspot['id']}"
  )}
"""

        if len(hotspots) > 10:
            text += f"\n... and {len(hotspots) - 10} more hotspots"

        return text.strip()

    @staticmethod
    def render_share_all_button(hotspots: list) -> None:
        """
        Render button to share all hotspots

        Args:
            hotspots: List of hotspot dictionaries
        """
        if st.button("📤 Share All Hotspots", use_container_width=True):
            share_text = ShareService.create_bulk_share(hotspots)

            st.download_button(
                "⬇️ Download Share Text",
                data=share_text,
                file_name=f"nashville_hotspots_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )

            st.code(share_text[:500] + "...", language="text")

