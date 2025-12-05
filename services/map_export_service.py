"""
Map Export Service - Microservice for exporting and printing maps
"""
import streamlit as st
import folium
from datetime import datetime
import os
from typing import Optional

class MapExportService:
    """Service for exporting and printing maps"""

    @staticmethod
    def export_map_to_html(map_obj: folium.Map, filename: Optional[str] = None) -> str:
        """
        Export folium map to HTML file

        Args:
            map_obj: Folium map object
            filename: Optional custom filename

        Returns:
            Path to exported HTML file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"nashville_safety_map_{timestamp}.html"

        # Ensure filename has .html extension
        if not filename.endswith('.html'):
            filename += '.html'

        # Save map
        export_path = f"exports/{filename}"
        os.makedirs("exports", exist_ok=True)
        map_obj.save(export_path)

        return export_path

    @staticmethod
    def create_printable_map(map_obj: folium.Map) -> folium.Map:
        """
        Create a print-optimized version of the map

        Args:
            map_obj: Original folium map

        Returns:
            Print-optimized folium map
        """
        # Create a copy with print-optimized settings
        print_map = folium.Map(
            location=map_obj.location,
            zoom_start=map_obj.options.get('zoom', 11),
            tiles='OpenStreetMap'
        )

        # Copy all layers from original map
        for layer in map_obj._children.values():
            print_map.add_child(layer)

        return print_map

    @staticmethod
    def get_map_as_base64(map_obj: folium.Map) -> str:
        """
        Convert map to base64 string for embedding

        Args:
            map_obj: Folium map object

        Returns:
            Base64 encoded HTML string
        """
        import base64

        html_string = map_obj._repr_html_()
        encoded = base64.b64encode(html_string.encode()).decode()
        return encoded

    @staticmethod
    def render_export_buttons(map_obj: folium.Map) -> None:
        """Render export buttons in UI"""
        if map_obj is None:
            st.warning("Map not available for export")
            return

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📥 Download Map (HTML)", use_container_width=True, key="download_map"):
                file_path = MapExportService.export_map_to_html(map_obj)
                try:
                    with open(file_path, 'rb') as f:
                        st.download_button(
                            label="⬇️ Click to Download",
                            data=f.read(),
                            file_name=os.path.basename(file_path),
                            mime="text/html",
                            use_container_width=True,
                            key="download_btn"
                        )
                    st.success(f"✅ Map saved as {os.path.basename(file_path)}")
                except Exception as e:
                    st.error(f"Error creating download: {str(e)}")

        with col2:
            if st.button("🖨️ Print Map", use_container_width=True, key="print_map"):
                st.info("💡 Use your browser's Print function (Ctrl+P / Cmd+P) to print the map")
                st.markdown(f"[Open Map in New Tab for Printing](data:text/html;base64,{MapExportService.get_map_as_base64(map_obj)})", unsafe_allow_html=True)

        with col3:
            st.markdown("**📤 Share Options:**")
            st.info("💡 Right-click on the map and 'Inspect' to access map controls")
            if st.button("📋 Get Share Link", use_container_width=True, key="share_link"):
                st.code(f"Map exported to: exports/", language="text")

    @staticmethod
    def create_map_with_legend(map_obj: folium.Map, legend_html: str) -> folium.Map:
        """
        Add custom legend to map for export

        Args:
            map_obj: Folium map object
            legend_html: HTML content for legend

        Returns:
            Map with legend added
        """
        from folium import Element

        map_obj.get_root().html.add_child(Element(legend_html))
        return map_obj

    @staticmethod
    def export_with_metadata(map_obj: folium.Map, metadata: dict) -> str:
        """
        Export map with metadata embedded

        Args:
            map_obj: Folium map object
            metadata: Dictionary of metadata (title, description, etc.)

        Returns:
            Path to exported file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"nashville_map_{timestamp}.html"

        # Add metadata as HTML comments
        metadata_html = f"""
        <!--
        Nashville Safe Tourist Guide - Map Export
        Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        Title: {metadata.get('title', 'Nashville Safety Map')}
        Description: {metadata.get('description', 'Crime hotspot safety map')}
        -->
        """

        export_path = f"exports/{filename}"
        os.makedirs("exports", exist_ok=True)

        # Add metadata to map HTML
        html_content = map_obj._repr_html_()
        html_with_metadata = metadata_html + html_content

        with open(export_path, 'w', encoding='utf-8') as f:
            f.write(html_with_metadata)

        return export_path

