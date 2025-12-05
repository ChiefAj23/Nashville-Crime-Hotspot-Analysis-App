"""
FastAPI Backend Server for Nashville Safe Tourist Guide
Serves hotspot data and all microservices as API endpoints
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

# Import microservices
import sys
sys.path.append(str(Path(__file__).parent.parent))

from services.route_planning_service import RoutePlanningService
from services.time_analysis_service import TimeAnalysisService
from services.emergency_contacts_service import EmergencyContactsService
from services.nearby_places_service import NearbyPlacesService
from services.historical_trends_service import HistoricalTrendsService
from services.weather_integration_service import WeatherIntegrationService
from services.user_preferences_service import UserPreferencesService
from services.safety_score_service import SafetyScoreService
from services.crime_filter_service import CrimeFilterService

# Initialize FastAPI app
app = FastAPI(
    title="Nashville Safe Tourist Guide API",
    description="API for Nashville Safe Tourist Guide - Crime hotspot analysis and safety features",
    version="1.0.0"
)

# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base directory
BASE_DIR = Path(__file__).parent.parent
HOTSPOTS_FILE = BASE_DIR / "data" / "processed" / "hotspots.json"

# Load hotspots data
def load_hotspots() -> List[Dict]:
    """Load hotspots from JSON file"""
    try:
        if HOTSPOTS_FILE.exists():
            with open(HOTSPOTS_FILE, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading hotspots: {e}")
        return []

# Pydantic models for request/response
class FilterRequest(BaseModel):
    severity: Optional[List[str]] = None
    crimeTypes: Optional[List[str]] = None
    timeFilter: Optional[str] = None

class RouteRequest(BaseModel):
    start_lat: float
    start_lon: float
    end_lat: float
    end_lon: float
    avoid_hotspots: bool = True

class SafetyScoreRequest(BaseModel):
    latitude: float
    longitude: float
    radius_meters: int = 1000

class FavoriteLocation(BaseModel):
    name: str
    latitude: float
    longitude: float

# API Routes

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Nashville Safe Tourist Guide API",
        "version": "1.0.0",
        "endpoints": {
            "hotspots": "/api/hotspots",
            "route": "/api/route/calculate",
            "safety": "/api/safety/calculate",
            "nearby": "/api/nearby-places",
            "weather": "/api/weather",
            "trends": "/api/trends",
            "time-analysis": "/api/time-analysis"
        }
    }

@app.get("/api/hotspots")
async def get_hotspots():
    """Get all hotspots"""
    hotspots = load_hotspots()
    return hotspots

@app.post("/api/hotspots/filter")
async def filter_hotspots(filter_request: FilterRequest):
    """Filter hotspots by severity, crime types, etc."""
    hotspots = load_hotspots()

    # Filter by severity
    if filter_request.severity:
        hotspots = [h for h in hotspots if h.get('severity') in filter_request.severity]

    # Filter by crime types
    if filter_request.crimeTypes:
        filtered_hotspots = []
        for hotspot in hotspots:
            # Check if hotspot matches any crime type
            explanation = hotspot.get('explanation', '').lower()
            for crime_type in filter_request.crimeTypes:
                if crime_type.lower() in explanation:
                    filtered_hotspots.append(hotspot)
                    break
        hotspots = filtered_hotspots

    return hotspots

@app.post("/api/route/calculate")
async def calculate_route(route_request: RouteRequest):
    """Calculate safe route between two points"""
    try:
        hotspots = load_hotspots()
        route = RoutePlanningService.calculate_route(
            route_request.start_lat,
            route_request.start_lon,
            route_request.end_lat,
            route_request.end_lon,
            hotspots,
            route_request.avoid_hotspots
        )
        return route
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/route/alternatives")
async def get_alternative_routes(route_request: RouteRequest, num_alternatives: int = 3):
    """Get alternative routes"""
    try:
        hotspots = load_hotspots()
        alternatives = RoutePlanningService.get_alternative_routes(
            route_request.start_lat,
            route_request.start_lon,
            route_request.end_lat,
            route_request.end_lon,
            hotspots,
            num_alternatives
        )
        return alternatives
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/safety/calculate")
async def calculate_safety_score(request: SafetyScoreRequest):
    """Calculate safety score for a location"""
    try:
        hotspots = load_hotspots()
        score, details = SafetyScoreService.calculate_location_score(
            request.latitude,
            request.longitude,
            hotspots,
            request.radius_meters
        )
        return {
            "score": score,
            "details": details
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/nearby-places")
async def get_nearby_places(latitude: float, longitude: float, radius_meters: int = 2000):
    """Get nearby safe places"""
    try:
        places = NearbyPlacesService.find_all_nearby_safe_places(
            latitude,
            longitude,
            radius_meters
        )
        return places
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/weather")
async def get_weather(latitude: float, longitude: float):
    """Get weather data for location"""
    try:
        weather = WeatherIntegrationService.get_weather(latitude, longitude)
        return weather
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/time-analysis")
async def get_time_analysis(hotspot_id: Optional[int] = None):
    """Get time-based analysis"""
    try:
        hourly_patterns = TimeAnalysisService.analyze_hourly_patterns(hotspot_id)

        # Create sample hotspot for demo
        sample_hotspot = {"severity": "High", "total_incidents": 100}
        safe_hours = TimeAnalysisService.get_safe_hours(sample_hotspot)
        peak_hours = TimeAnalysisService.get_peak_crime_hours(sample_hotspot)

        return {
            "hourly_patterns": hourly_patterns,
            "safe_hours": safe_hours,
            "peak_hours": peak_hours
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/trends")
async def get_trends(type: str = "monthly"):
    """Get historical trends"""
    try:
        hotspots = load_hotspots()

        if type == "monthly":
            trends = HistoricalTrendsService.analyze_monthly_trends(hotspots)
            return {
                "type": "monthly",
                "data": trends,
                "labels": list(trends.keys()),
                "values": list(trends.values())
            }
        elif type == "seasonal":
            trends = HistoricalTrendsService.analyze_seasonal_patterns(hotspots)
            return {
                "type": "seasonal",
                "data": trends,
                "labels": list(trends.keys()),
                "values": list(trends.values())
            }
        elif type == "daily":
            trends = HistoricalTrendsService.analyze_day_of_week_patterns(hotspots)
            return {
                "type": "daily",
                "data": trends,
                "labels": list(trends.keys()),
                "values": list(trends.values())
            }
        elif type == "yearly":
            trends = HistoricalTrendsService.analyze_yearly_trends()
            return {
                "type": "yearly",
                "data": trends,
                "labels": [str(k) for k in sorted(trends.keys())],
                "values": [trends[k] for k in sorted(trends.keys())]
            }
        else:
            raise HTTPException(status_code=400, detail="Invalid trend type")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/emergency-contacts")
async def get_emergency_contacts():
    """Get emergency contacts"""
    return EmergencyContactsService.get_emergency_contacts()

@app.get("/api/user/preferences")
async def get_user_preferences():
    """Get user preferences"""
    try:
        preferences = UserPreferencesService.get_risk_settings()
        alerts = UserPreferencesService.get_alert_preferences()
        return {**preferences, **alerts}
    except Exception as e:
        # Return defaults if error
        return {
            "risk_tolerance": "medium",
            "alert_distance": 500,
            "high_risk_alerts": True,
            "medium_risk_alerts": True,
            "low_risk_alerts": False
        }

@app.post("/api/user/preferences")
async def save_user_preferences(preferences: Dict[str, Any]):
    """Save user preferences"""
    try:
        UserPreferencesService.save_risk_settings({
            "risk_tolerance": preferences.get("risk_tolerance", "medium"),
            "alert_distance": preferences.get("alert_distance", 500)
        })
        UserPreferencesService.save_alert_preferences({
            "high_risk_alerts": preferences.get("high_risk_alerts", True),
            "medium_risk_alerts": preferences.get("medium_risk_alerts", True),
            "low_risk_alerts": preferences.get("low_risk_alerts", False)
        })
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/user/favorites")
async def get_favorites():
    """Get favorite locations"""
    try:
        favorites = UserPreferencesService.get_favorites()
        return favorites
    except Exception as e:
        return []

@app.post("/api/user/favorites")
async def save_favorite(location: FavoriteLocation):
    """Save favorite location"""
    try:
        UserPreferencesService.save_favorite_location(location.dict())
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/user/favorites/{location_name}")
async def delete_favorite(location_name: str):
    """Delete favorite location"""
    try:
        UserPreferencesService.remove_favorite(location_name)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

