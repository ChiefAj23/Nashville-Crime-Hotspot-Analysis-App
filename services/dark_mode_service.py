"""
Dark Mode Service - Microservice for dark/light theme management
"""
import streamlit as st
from typing import Dict, Tuple

class DarkModeService:
    """Service for managing dark/light mode theme"""

    DARK_MODE_CSS = """
    <style>
        /* Dark Mode Styles */
        .stApp {
            background-color: #0e1117;
        }
        .main {
            background-color: #0e1117;
        }
        .element-container p, .element-container h1, .element-container h2,
        .element-container h3, .element-container h4, .element-container h5,
        .element-container h6 {
            color: #fafafa !important;
        }
        .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #fafafa !important;
        }
        .hotspot-card {
            background: #1e1e1e !important;
            color: #fafafa !important;
            border: 1px solid #333333;
        }
        .hotspot-card h3 {
            color: #ffffff !important;
        }
        .hotspot-card p {
            color: #d3d3d3 !important;
        }
        section[data-testid="stSidebar"] {
            background-color: #1e1e1e;
        }
        .css-1d391kg {
            color: #fafafa;
        }
        .metric-card {
            background: #1e1e1e !important;
            color: #fafafa !important;
        }
    </style>
    """

    LIGHT_MODE_CSS = """
    <style>
        /* Light Mode Styles */
        .stApp {
            background-color: #ffffff;
        }
        .main {
            background-color: #ffffff;
        }
        .element-container p, .element-container h1, .element-container h2,
        .element-container h3, .element-container h4, .element-container h5,
        .element-container h6 {
            color: #333333 !important;
        }
        .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #333333 !important;
        }
        .hotspot-card {
            background: white !important;
            color: #333333 !important;
        }
        .hotspot-card h3 {
            color: #222222 !important;
        }
        .hotspot-card p {
            color: #555555 !important;
        }
        section[data-testid="stSidebar"] {
            background-color: #ffffff;
        }
        .css-1d391kg {
            color: #262730;
        }
        .metric-card {
            background: white !important;
            color: #333333 !important;
        }
    </style>
    """

    @staticmethod
    def get_theme_state() -> bool:
        """Get current dark mode state from session"""
        if 'dark_mode' not in st.session_state:
            st.session_state.dark_mode = False
        return st.session_state.dark_mode

    @staticmethod
    def set_theme(dark_mode: bool) -> None:
        """Set dark mode state"""
        st.session_state.dark_mode = dark_mode

    @staticmethod
    def toggle_theme() -> bool:
        """Toggle between dark and light mode"""
        current = DarkModeService.get_theme_state()
        DarkModeService.set_theme(not current)
        return not current

    @staticmethod
    def render_toggle() -> bool:
        """Render dark mode toggle button in sidebar"""
        current_theme = DarkModeService.get_theme_state()

        # Toggle button
        if st.sidebar.button(
            f"{'🌙' if not current_theme else '☀️'} {'Dark Mode' if not current_theme else 'Light Mode'}",
            key="dark_mode_toggle",
            use_container_width=True
        ):
            DarkModeService.toggle_theme()
            st.rerun()

        return DarkModeService.get_theme_state()

    @staticmethod
    def apply_theme() -> None:
        """Apply the current theme CSS"""
        is_dark = DarkModeService.get_theme_state()
        css = DarkModeService.DARK_MODE_CSS if is_dark else DarkModeService.LIGHT_MODE_CSS
        st.markdown(css, unsafe_allow_html=True)

    @staticmethod
    def get_theme_colors() -> Dict[str, str]:
        """Get color scheme based on current theme"""
        is_dark = DarkModeService.get_theme_state()

        if is_dark:
            return {
                'background': '#0e1117',
                'text': '#fafafa',
                'card_background': '#1e1e1e',
                'border': '#333333',
                'text_secondary': '#d3d3d3'
            }
        else:
            return {
                'background': '#ffffff',
                'text': '#333333',
                'card_background': '#ffffff',
                'border': '#e0e0e0',
                'text_secondary': '#555555'
            }

