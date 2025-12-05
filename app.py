"""
Nashville Tourist Discovery App - Safe Travel Guide
A production-ready app for tourists to discover safe areas and avoid high-risk zones
"""
import streamlit as st
import json
import folium
# Removed unused imports that might cause serialization issues
from streamlit_folium import folium_static
import pandas as pd
import numpy as np

# Import microservices
from services.dark_mode_service import DarkModeService
from services.map_export_service import MapExportService
from services.crime_filter_service import CrimeFilterService
from services.share_service import ShareService
from services.safety_score_service import SafetyScoreService
from services.distance_service import DistanceService
from services.route_planning_service import RoutePlanningService
from services.time_analysis_service import TimeAnalysisService
from services.emergency_contacts_service import EmergencyContactsService
from services.nearby_places_service import NearbyPlacesService
from services.historical_trends_service import HistoricalTrendsService
from services.weather_integration_service import WeatherIntegrationService
from services.user_preferences_service import UserPreferencesService

# Page configuration
st.set_page_config(
    page_title="Nashville Safe Tourist Guide",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
    <style>
        /* Main styling */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .main-header h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
        }

        .main-header p {
            margin: 0.5rem 0 0 0;
            font-size: 1.1rem;
            opacity: 0.9;
        }

        .warning-box {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.9; }
        }

        .info-box {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .safe-box {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .hotspot-card {
            background: white !important;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            border-left: 5px solid #ff6b6b;
            color: #333333 !important;
        }

        .hotspot-card h3 {
            color: #333333 !important;
        }

        .hotspot-card p {
            color: #555555 !important;
        }

        .hotspot-card strong {
            color: #222222 !important;
        }

        .hotspot-card.medium {
            border-left-color: #ffa500;
        }

        .hotspot-card.low {
            border-left-color: #38ef7d;
        }

        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s;
        }

        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        /* Ensure text is visible - override Streamlit defaults */
        .main .block-container {
            color: #333333 !important;
            background-color: #ffffff;
        }

        /* Make sure all text in main area is dark */
        .element-container p, .element-container h1, .element-container h2,
        .element-container h3, .element-container h4, .element-container h5,
        .element-container h6 {
            color: #333333 !important;
        }

        /* Ensure Streamlit markdown text is dark */
        .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
        .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
            color: #333333 !important;
        }

        .stMarkdown strong {
            color: #222222 !important;
        }

        /* Force light theme background */
        .stApp {
            background-color: #ffffff;
        }

        .main {
            background-color: #ffffff;
        }

        /* Sidebar text should also be visible */
        section[data-testid="stSidebar"] {
            background-color: #ffffff;
        }

        /* Metric cards text */
        .metric-card {
            color: #333333 !important;
        }

        /* All paragraph and heading text in main content */
        div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stMarkdownContainer"] h1,
        div[data-testid="stMarkdownContainer"] h2,
        div[data-testid="stMarkdownContainer"] h3 {
            color: #333333 !important;
        }

        /* Hide Streamlit default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_hotspots():
    """Load hotspot data from JSON file"""
    try:
        with open("data/processed/hotspots.json", 'r') as f:
            hotspots = json.load(f)
        # Filter out hotspots with extremely large radius (likely noise)
        filtered_hotspots = [h for h in hotspots if h['radius_meters'] < 10000]
        return filtered_hotspots
    except FileNotFoundError:
        st.error("Hotspots file not found. Please run hotspot_analyzer.py first.")
        return []

# Use DistanceService instead of local function
def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in meters - delegates to DistanceService"""
    return DistanceService.haversine_distance(lat1, lon1, lat2, lon2)

def safe_html(text):
    """Safely escape HTML for popup content"""
    if text is None:
        return ""
    # Convert to string and escape HTML entities
    text = str(text)
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&#39;')
    return text

def check_location_in_hotspot(user_lat, user_lon, hotspots):
    """Check if user location is within any hotspot - uses DistanceService"""
    nearby_hotspots = []

    for hotspot in hotspots:
        distance_m = DistanceService.haversine_distance(
            user_lat, user_lon,
            hotspot['latitude'], hotspot['longitude']
        )

        # Check if within hotspot radius (with 50m buffer)
        if distance_m <= (hotspot['radius_meters'] + 50):
            nearby_hotspots.append({
                'hotspot': hotspot,
                'distance': distance_m
            })

    return nearby_hotspots

def create_map(hotspots, user_lat=None, user_lon=None):
    """Create interactive map with hotspots"""
    # Center map on Nashville
    map_center = [36.1627, -86.7816] if user_lat is None else [user_lat, user_lon]

    m = folium.Map(
        location=map_center,
        zoom_start=11,
        tiles='CartoDB positron'
    )

    # Add different tile layers
    folium.TileLayer('OpenStreetMap').add_to(m)
    folium.TileLayer('CartoDB dark_matter').add_to(m)

    # Color mapping for severity
    severity_colors = {
        'High': '#ff6b6b',
        'Medium': '#ffa500',
        'Low': '#38ef7d'
    }

    # Add hotspots as circles
    for hotspot in hotspots:
        color = severity_colors.get(hotspot['severity'], '#808080')
        opacity = 0.6 if hotspot['severity'] == 'High' else 0.4

        # Safely escape HTML in explanation
        explanation_html = safe_html(hotspot.get('explanation', 'No explanation available'))
        severity_html = safe_html(hotspot['severity'])

        popup_html_circle = f"""<div style="width: 300px; max-height: 400px; overflow-y: auto;">
            <h3 style="color: {color};">{severity_html} Risk Area</h3>
            <p><strong>Total Incidents:</strong> {hotspot['total_incidents']:,}</p>
            <p><strong>High Risk:</strong> {hotspot['high_risk_count']:,}</p>
            <p><strong>Medium Risk:</strong> {hotspot['medium_risk_count']:,}</p>
            <p><strong>Radius:</strong> {hotspot['radius_meters']:.0f}m</p>
            <hr>
            <p style="font-size: 0.9em;">{explanation_html}</p>
        </div>"""

        # Create circle for hotspot
        folium.Circle(
            location=[hotspot['latitude'], hotspot['longitude']],
            radius=hotspot['radius_meters'],
            popup=folium.Popup(popup_html_circle, max_width=300, max_height=400),
            tooltip=f"{hotspot['severity']} Risk - {hotspot['total_incidents']:,} incidents",
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=opacity,
            weight=2
        ).add_to(m)

        # Add marker at center (simplified icon to avoid serialization issues)
        icon_color = 'red' if hotspot['severity'] == 'High' else ('orange' if hotspot['severity'] == 'Medium' else 'green')
        # Safely escape HTML in explanation
        explanation_html = safe_html(hotspot.get('explanation', 'No explanation available'))
        severity_html = safe_html(hotspot['severity'])

        popup_html = f"""<div style="width: 300px; max-height: 400px; overflow-y: auto;">
            <h3 style="color: {icon_color};">{severity_html} Risk Area #{hotspot['id']}</h3>
            <p><strong>Total Incidents:</strong> {hotspot['total_incidents']:,}</p>
            <p><strong>High Risk:</strong> {hotspot['high_risk_count']:,}</p>
            <p><strong>Medium Risk:</strong> {hotspot['medium_risk_count']:,}</p>
            <p><strong>Radius:</strong> {hotspot['radius_meters']:.0f}m</p>
            <hr>
            <p><strong>Why avoid?</strong></p>
            <p style="font-size: 0.9em;">{explanation_html}</p>
        </div>"""

        folium.Marker(
            location=[hotspot['latitude'], hotspot['longitude']],
            icon=folium.Icon(color=icon_color, icon='info-sign'),
            popup=folium.Popup(popup_html, max_width=300, max_height=400),
            tooltip=f"{hotspot['severity']} Risk - Click for details"
        ).add_to(m)

    # Add user location if provided
    if user_lat and user_lon:
        folium.Marker(
            location=[user_lat, user_lon],
            icon=folium.Icon(color='blue', icon='user'),
            tooltip='Your Location',
            popup='Your Current Location'
        ).add_to(m)

        # Check if in hotspot
        nearby = check_location_in_hotspot(user_lat, user_lon, hotspots)
        if nearby:
            for item in nearby:
                hotspot = item['hotspot']
                # Draw line from user to hotspot center
                folium.PolyLine(
                    locations=[[user_lat, user_lon],
                             [hotspot['latitude'], hotspot['longitude']]],
                    color='red',
                    weight=3,
                    opacity=0.5,
                    tooltip=f"Distance: {item['distance']:.0f}m"
                ).add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)

    return m

def main():
    # Initialize Dark Mode Service
    DarkModeService.apply_theme()

    # Header
    st.markdown("""
        <div class="main-header">
            <h1>🗺️ Nashville Safe Tourist Guide</h1>
            <p>Discover safe areas and get real-time alerts for high-risk zones</p>
        </div>
    """, unsafe_allow_html=True)

    # Load hotspots
    hotspots = load_hotspots()

    if not hotspots:
        st.error("No hotspot data available. Please run hotspot_analyzer.py first.")
        return

    # Sidebar
    with st.sidebar:
        # Dark Mode Toggle at top
        DarkModeService.render_toggle()
        st.markdown("---")

        st.markdown("### 🎯 Navigation")

        # Set Map View as default (index 0)
        page = st.radio(
            "Choose a view:",
            [
                "📍 Map View",
                "🗺️ Route Planner",
                "📊 Statistics",
                "🛡️ Safety Calculator",
                "📈 Trends",
                "⚙️ Settings"
            ],
            index=0,  # Default to Map View
            label_visibility="collapsed"
        )

        st.markdown("---")
        st.markdown("### 📍 Location Tracking")

        # Location tracking toggle
        track_location = st.checkbox("Enable Location Tracking", value=False)

        if track_location:
            st.info("""
            **Location tracking enabled!**

            Allow browser location access when prompted.
            You'll receive alerts when entering high-risk areas.
            """)

            # Get location from user
            location_method = st.radio(
                "Location input method:",
                ["📍 Browser GPS", "✏️ Manual Entry"]
            )

            user_lat = None
            user_lon = None

            if location_method == "📍 Browser GPS":
                st.info("💡 **Browser GPS Feature:** Click the button below and allow location access when prompted.")

                # Initialize session state for location
                if 'user_lat' not in st.session_state:
                    st.session_state.user_lat = None
                if 'user_lon' not in st.session_state:
                    st.session_state.user_lon = None

                # JavaScript component to get location
                location_component = st.components.v1.html("""
                    <div style="padding: 1rem; background: #f0f2f6; border-radius: 10px;">
                        <button id="get-loc-btn" onclick="getLocation()"
                                style="background: #667eea; color: white; border: none; padding: 0.75rem 1.5rem;
                                       border-radius: 5px; cursor: pointer; font-weight: 600; width: 100%;">
                            📍 Get My Location
                        </button>
                        <div id="location-status" style="margin-top: 1rem; font-size: 0.9rem; color: #333;"></div>
                    </div>
                    <script>
                        function getLocation() {
                            const statusDiv = document.getElementById('location-status');
                            if (navigator.geolocation) {
                                statusDiv.innerHTML = '⏳ Getting location... Please allow location access.';
                                navigator.geolocation.getCurrentPosition(
                                    function(position) {
                                        const lat = position.coords.latitude;
                                        const lon = position.coords.longitude;
                                        statusDiv.innerHTML = '✅ Location received: ' + lat.toFixed(6) + ', ' + lon.toFixed(6);

                                        // Show coordinates in a format that can be copied
                                        statusDiv.innerHTML += '<br><small>Copy these coordinates to use in manual entry mode</small>';

                                        // Store in a way Streamlit can access (through URL params)
                                        const url = new URL(window.location);
                                        url.searchParams.set('lat', lat);
                                        url.searchParams.set('lon', lon);
                                        window.history.pushState({}, '', url);
                                    },
                                    function(error) {
                                        statusDiv.innerHTML = '❌ Error: ' + error.message + '<br><small>Please use Manual Entry mode instead</small>';
                                    },
                                    {
                                        enableHighAccuracy: true,
                                        timeout: 15000,
                                        maximumAge: 0
                                    }
                                );
                            } else {
                                statusDiv.innerHTML = '❌ Geolocation not supported by your browser. Please use Manual Entry mode.';
                            }
                        }
                    </script>
                """, height=150)

                # Try to get location from URL parameters (set by JavaScript)
                query_params = st.query_params
                if 'lat' in query_params and 'lon' in query_params:
                    try:
                        user_lat = float(query_params['lat'])
                        user_lon = float(query_params['lon'])
                        st.session_state.user_lat = user_lat
                        st.session_state.user_lon = user_lon
                    except:
                        user_lat = st.session_state.user_lat
                        user_lon = st.session_state.user_lon
                else:
                    user_lat = st.session_state.user_lat
                    user_lon = st.session_state.user_lon

                if user_lat and user_lon:
                    st.success(f"📍 Current location: {user_lat:.6f}, {user_lon:.6f}")
                    if st.button("Clear Location"):
                        st.session_state.user_lat = None
                        st.session_state.user_lon = None
                        st.rerun()
            else:
                user_lat = st.number_input("Latitude", value=36.1627, format="%.6f")
                user_lon = st.number_input("Longitude", value=-86.7816, format="%.6f")

            if user_lat and user_lon:
                # Check if in hotspot
                nearby_hotspots = check_location_in_hotspot(user_lat, user_lon, hotspots)

                if nearby_hotspots:
                    st.markdown("---")
                    st.markdown("### ⚠️ Alert Status")
                    for item in nearby_hotspots:
                        hotspot = item['hotspot']
                        distance_m = item['distance']

                        if hotspot['severity'] == 'High':
                            st.markdown(f"""
                                <div class="warning-box">
                                    <h3>🚨 HIGH RISK AREA DETECTED!</h3>
                                    <p><strong>Distance:</strong> {distance_m:.0f}m away</p>
                                    <p><strong>Risk Level:</strong> {hotspot['severity']}</p>
                                    <p><strong>Total Incidents:</strong> {hotspot['total_incidents']:,}</p>
                                </div>
                            """, unsafe_allow_html=True)
                        elif hotspot['severity'] == 'Medium':
                            st.markdown(f"""
                                <div class="info-box">
                                    <h3>⚠️ MEDIUM RISK AREA</h3>
                                    <p><strong>Distance:</strong> {distance_m:.0f}m away</p>
                                    <p><strong>Risk Level:</strong> {hotspot['severity']}</p>
                                </div>
                            """, unsafe_allow_html=True)
        else:
            user_lat = None
            user_lon = None

        st.markdown("---")
        st.markdown("### 🔍 Filter Hotspots")

        # Filter by severity (existing)
        severity_filter = st.multiselect(
            "Show only (Risk Level):",
            ["High", "Medium", "Low"],
            default=["High", "Medium"]
        )

        # Filter hotspots by severity
        filtered_by_severity = [h for h in hotspots if h['severity'] in severity_filter]

        # Crime type filter (new service)
        st.markdown("---")
        selected_crime_types = CrimeFilterService.render_filter_ui(filtered_by_severity)

        # Apply crime type filter
        if selected_crime_types:
            filtered_hotspots = CrimeFilterService.filter_by_crime_type(filtered_by_severity, selected_crime_types)
        else:
            filtered_hotspots = filtered_by_severity

        st.markdown(f"**Showing {len(filtered_hotspots)} of {len(hotspots)} hotspots**")

    # Main content based on page
    if page == "📍 Map View":
        # Map header with legend
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### 🗺️ Interactive Safety Map")
            st.markdown("""
            <p>Explore Nashville with our interactive safety map. High-risk areas are marked in <span style="color: #ff6b6b; font-weight: bold;">red</span>,
            medium-risk in <span style="color: #ffa500; font-weight: bold;">orange</span>, and low-risk in <span style="color: #38ef7d; font-weight: bold;">green</span>.</p>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("### 🎨 Legend")
            st.markdown("""
            <div style="padding: 1rem; background: #f0f2f6; border-radius: 10px;">
                <p><span style="color: #ff6b6b; font-weight: bold;">●</span> High Risk</p>
                <p><span style="color: #ffa500; font-weight: bold;">●</span> Medium Risk</p>
                <p><span style="color: #38ef7d; font-weight: bold;">●</span> Low Risk</p>
                <p><span style="color: #4facfe; font-weight: bold;">●</span> Your Location</p>
            </div>
            """, unsafe_allow_html=True)

        # Time-based filter integration
        st.markdown("---")
        time_filter = TimeAnalysisService.render_time_filter_ui()
        if time_filter['type'] != "All Day":
            filtered_hotspots = TimeAnalysisService.filter_hotspots_by_time(filtered_hotspots, time_filter)
            st.info(f"⏰ Time filter applied: {time_filter['type']}")

        # Create and display map
        st.markdown("---")
        m = create_map(filtered_hotspots, user_lat, user_lon)

        # Display map using folium_static (more reliable than st_folium)
        # Use full width and good height for better visibility
        try:
            folium_static(m, width=None, height=700)

            # Map Export Buttons (new service) - after map is displayed
            st.markdown("---")
            st.markdown("### 📥 Export Map")
            MapExportService.render_export_buttons(m)

            # Weather integration on map page
            if user_lat and user_lon:
                st.markdown("---")
                weather = WeatherIntegrationService.render_weather_panel(user_lat, user_lon)
                if weather:
                    # Adjust risk based on weather
                    st.info("💡 Weather conditions may affect safety. Check recommendations above.")

        except Exception as e:
            st.error(f"Error displaying map: {str(e)}")
            st.info("Please try refreshing the page. If the issue persists, check that all hotspots data is valid.")
            # Fallback: show map in an iframe
            m.save('temp_map.html')
            st.components.v1.html(open('temp_map.html', 'r').read(), height=700)

        # Show warning if user is in hotspot
        if user_lat and user_lon:
            nearby = check_location_in_hotspot(user_lat, user_lon, filtered_hotspots)
            if nearby:
                st.markdown("---")
                for item in nearby:
                    hotspot = item['hotspot']
                    if hotspot['severity'] == 'High':
                        st.markdown(f"""
                            <div class="warning-box">
                                <h2>🚨 WARNING: You are in a HIGH RISK AREA!</h2>
                                <h3>Hotspot #{hotspot['id']} - {hotspot['severity']} Risk</h3>
                                <p><strong>Your distance from center:</strong> {item['distance']:.0f} meters</p>
                                <p><strong>Total incidents recorded:</strong> {hotspot['total_incidents']:,}</p>
                                <p><strong>High-risk incidents:</strong> {hotspot['high_risk_count']:,}</p>
                                <hr>
                                <p><strong>Why avoid this area?</strong></p>
                                <p>{hotspot['explanation']}</p>
                                <p><strong>Recommendation:</strong> Leave this area as soon as possible. Use well-lit, populated routes.</p>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div class="info-box">
                                <h3>⚠️ You are near a {hotspot['severity']} risk area</h3>
                                <p>{hotspot['explanation']}</p>
                            </div>
                        """, unsafe_allow_html=True)

    elif page == "📊 Statistics":
        # Prominent call-to-action to view map
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem; text-align: center;">
            <h2 style="color: white; margin: 0;">🗺️ Want to see the Interactive Map?</h2>
            <p style="color: white; margin: 0.5rem 0 0 0;">Click <strong>'📍 Map View'</strong> in the sidebar to explore all hotspots on an interactive map!</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📊 Crime Hotspot Statistics")

        # Calculate statistics
        total_incidents = sum(h['total_incidents'] for h in hotspots)
        high_risk_count = len([h for h in hotspots if h['severity'] == 'High'])
        medium_risk_count = len([h for h in hotspots if h['severity'] == 'Medium'])
        low_risk_count = len([h for h in hotspots if h['severity'] == 'Low'])

        # Display metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Hotspots", len(hotspots))

        with col2:
            st.metric("High Risk Areas", high_risk_count, delta=f"{high_risk_count/len(hotspots)*100:.1f}%")

        with col3:
            st.metric("Total Incidents", f"{total_incidents:,}")

        with col4:
            st.metric("Medium Risk", medium_risk_count)

        st.markdown("---")

        # Hotspot list
        st.markdown("### 🎯 High-Risk Areas to Avoid")

        # Sort by risk score
        sorted_hotspots = sorted(filtered_hotspots, key=lambda x: x['total_risk_score'], reverse=True)

        for hotspot in sorted_hotspots[:20]:  # Show top 20
            severity_class = hotspot['severity'].lower()

            st.markdown(f"""
                <div class="hotspot-card {severity_class}" style="background: white; color: #333333;">
                    <h3 style="color: #222222; margin-top: 0;">🚨 Hotspot #{hotspot['id']} - {hotspot['severity']} Risk</h3>
                    <p style="color: #555555;"><strong style="color: #222222;">Location:</strong> ({hotspot['latitude']:.4f}, {hotspot['longitude']:.4f})</p>
                    <p style="color: #555555;"><strong style="color: #222222;">Total Incidents:</strong> {hotspot['total_incidents']:,} |
                       <strong style="color: #222222;">High Risk:</strong> {hotspot['high_risk_count']:,} |
                       <strong style="color: #222222;">Radius:</strong> {hotspot['radius_meters']:.0f}m</p>
                    <p style="color: #555555;"><strong style="color: #222222;">Why avoid?</strong> <span style="color: #444444;">{safe_html(hotspot.get('explanation', 'No explanation available'))}</span></p>
                </div>
            """, unsafe_allow_html=True)

            # Add share button for each hotspot
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button(f"📤 Share", key=f"share_{hotspot['id']}", use_container_width=True):
                    st.session_state[f"show_share_{hotspot['id']}"] = True

            if st.session_state.get(f"show_share_{hotspot['id']}", False):
                ShareService.render_share_buttons(hotspot)

    elif page == "🗺️ Route Planner":
        RoutePlanningService.render_route_planner(hotspots)

        # Add nearby places and emergency contacts
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            EmergencyContactsService.render_emergency_panel()
        with col2:
            user_lat = st.session_state.get('user_lat')
            user_lon = st.session_state.get('user_lon')
            NearbyPlacesService.render_nearby_places_ui(user_lat, user_lon)

    elif page == "🛡️ Safety Calculator":
        SafetyScoreService.render_score_calculator(hotspots)

        # Share all hotspots button
        st.markdown("---")
        ShareService.render_share_all_button(hotspots)

        # Add nearby places
        st.markdown("---")
        user_lat = st.session_state.get('user_lat')
        user_lon = st.session_state.get('user_lon')
        NearbyPlacesService.render_nearby_places_ui(user_lat, user_lon)

    elif page == "📈 Trends":
        HistoricalTrendsService.render_trends_dashboard()

        # Add time analysis
        st.markdown("---")
        st.markdown("### ⏰ Time-of-Day Analysis")
        time_filter = TimeAnalysisService.render_time_filter_ui()

        # Show time-based filtered hotspots
        if time_filter['type'] != "All Day":
            time_filtered = TimeAnalysisService.filter_hotspots_by_time(hotspots, time_filter)
            st.info(f"📊 Showing {len(time_filtered)} hotspots with time-based risk analysis")

            # Show peak hours
            if time_filtered:
                sample_hotspot = time_filtered[0]
                peak_hours = TimeAnalysisService.get_peak_crime_hours(sample_hotspot)
                safe_hours = TimeAnalysisService.get_safe_hours(sample_hotspot)

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**⚠️ Peak Crime Hours:** {', '.join([f'{h}:00' for h in peak_hours[:5]])}")
                with col2:
                    st.markdown(f"**✅ Safe Hours:** {', '.join([f'{h}:00' for h in safe_hours[:5]])}")

    elif page == "⚙️ Settings":
        st.markdown("### ⚙️ App Settings")

        # Tabs for different settings
        tab1, tab2, tab3, tab4 = st.tabs(["📋 About", "🚨 Emergency", "⭐ Favorites", "⚙️ Preferences"])

        with tab1:
            st.info("""
            ### About This App

            This app helps tourists safely explore Nashville by identifying high-risk areas
            based on 911 call data analysis. It uses machine learning clustering algorithms
            (DBSCAN) to identify crime hotspots and provides real-time warnings when you
            enter these areas.

            ### Features:
            - 🗺️ Interactive map with hotspot visualization
            - 📍 Real-time location tracking
            - 🚨 Geofencing alerts
            - 📊 Detailed statistics and explanations
            - 🗺️ Safe route planning
            - ⏰ Time-of-day risk analysis
            - 🏥 Nearby safe places
            - 📈 Historical trends

            ### Data Source:
            Metro Nashville Police Department 911 Calls for Service

            ### Safety Disclaimer:
            This app is a tool to help inform your decisions. Always use your best judgment
            and follow local safety guidelines when traveling.
            """)

            st.markdown("---")
            st.markdown("### 🔄 Refresh Data")

            if st.button("Regenerate Hotspots"):
                st.info("Run `python hotspot_analyzer.py` in the terminal to regenerate hotspot data.")

        with tab2:
            EmergencyContactsService.render_emergency_panel()

        with tab3:
            UserPreferencesService.render_favorites_ui()

        with tab4:
            UserPreferencesService.render_preferences_ui()

            # Weather integration
            st.markdown("---")
            user_lat = st.session_state.get('user_lat', 36.1627)
            user_lon = st.session_state.get('user_lon', -86.7816)
            WeatherIntegrationService.render_weather_panel(user_lat, user_lon)

if __name__ == "__main__":
    main()

