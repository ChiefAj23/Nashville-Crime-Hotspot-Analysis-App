"""
Custom Streamlit components for location tracking
"""
import streamlit as st
import streamlit.components.v1 as components

def location_tracker():
    """HTML component for browser-based location tracking"""
    location_html = """
    <div id="location-status"></div>
    <script>
        function updateLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    function(position) {
                        // Send location to Streamlit
                        window.parent.postMessage({
                            type: 'streamlit:setComponentValue',
                            value: {
                                lat: position.coords.latitude,
                                lon: position.coords.longitude,
                                accuracy: position.coords.accuracy
                            }
                        }, '*');

                        document.getElementById('location-status').innerHTML =
                            '📍 Location updated: ' + position.coords.latitude.toFixed(6) +
                            ', ' + position.coords.longitude.toFixed(6);
                    },
                    function(error) {
                        document.getElementById('location-status').innerHTML =
                            '❌ Location error: ' + error.message;
                    },
                    {
                        enableHighAccuracy: true,
                        timeout: 10000,
                        maximumAge: 0
                    }
                );
            } else {
                document.getElementById('location-status').innerHTML =
                    '❌ Geolocation not supported by this browser.';
            }
        }

        // Update location every 5 seconds
        updateLocation();
        setInterval(updateLocation, 5000);
    </script>
    """

    return components.html(location_html, height=50)

