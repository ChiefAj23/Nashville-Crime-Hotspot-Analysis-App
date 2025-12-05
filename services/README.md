# 🔧 Services Architecture - Microservice Pattern

This directory contains modular microservices following the microservice architecture pattern. Each service is self-contained, independently testable, and can be used across different parts of the application.

## 📁 Services Overview

### 1. **DarkModeService** (`dark_mode_service.py`)
**Purpose:** Manages dark/light theme switching

**Features:**
- Toggle between dark and light modes
- Persistent theme state
- Dynamic CSS injection
- Theme color scheme retrieval

**Usage:**
```python
from services.dark_mode_service import DarkModeService

# Apply theme
DarkModeService.apply_theme()

# Render toggle button
DarkModeService.render_toggle()

# Get current theme
is_dark = DarkModeService.get_theme_state()
```

---

### 2. **MapExportService** (`map_export_service.py`)
**Purpose:** Handles map export and printing functionality

**Features:**
- Export maps to HTML
- Print-optimized map generation
- Base64 encoding for embedding
- Metadata embedding

**Usage:**
```python
from services.map_export_service import MapExportService

# Export map
file_path = MapExportService.export_map_to_html(map_obj)

# Render export buttons
MapExportService.render_export_buttons(map_obj)
```

---

### 3. **CrimeFilterService** (`crime_filter_service.py`)
**Purpose:** Filters hotspots by crime type and category

**Features:**
- Filter by crime type
- Filter by category (Violent, Property, Traffic, etc.)
- Crime type categorization
- Filter statistics

**Usage:**
```python
from services.crime_filter_service import CrimeFilterService

# Filter hotspots
filtered = CrimeFilterService.filter_by_crime_type(hotspots, ['THEFT', 'BURGLARY'])

# Render filter UI
selected_types = CrimeFilterService.render_filter_ui(hotspots)
```

---

### 4. **ShareService** (`share_service.py`)
**Purpose:** Generates shareable links and text for hotspots

**Features:**
- Google Maps links
- Apple Maps links
- Shareable text generation
- Social media sharing links
- Bulk sharing

**Usage:**
```python
from services.share_service import ShareService

# Generate Google Maps link
link = ShareService.generate_google_maps_link(lat, lon, "Label")

# Render share buttons
ShareService.render_share_buttons(hotspot)
```

---

### 5. **SafetyScoreService** (`safety_score_service.py`)
**Purpose:** Calculates safety scores for locations

**Features:**
- Location safety scoring (0-100)
- Hotspot risk scoring
- Safety level determination
- Safety recommendations
- Nearby hotspot analysis

**Usage:**
```python
from services.safety_score_service import SafetyScoreService

# Calculate location score
score, details = SafetyScoreService.calculate_location_score(lat, lon, hotspots)

# Render calculator UI
SafetyScoreService.render_score_calculator(hotspots)
```

---

### 6. **DistanceService** (`distance_service.py`)
**Purpose:** Utility service for distance calculations

**Features:**
- Haversine distance calculation
- Meters-based distance

**Usage:**
```python
from services.distance_service import DistanceService

distance = DistanceService.haversine_distance(lat1, lon1, lat2, lon2)
```

---

## 🏗️ Architecture Benefits

### ✅ **Modularity**
Each service is independent and can be modified without affecting others

### ✅ **Testability**
Services can be unit tested individually

### ✅ **Reusability**
Services can be used across different parts of the app

### ✅ **Maintainability**
Clear separation of concerns makes code easier to maintain

### ✅ **Scalability**
Easy to add new services or extend existing ones

---

## 🔄 Service Dependencies

```
SafetyScoreService → DistanceService
All Services → None (except above)
Main App → All Services
```

---

## 📝 Adding New Services

To add a new service:

1. Create a new file: `services/your_service.py`
2. Create a class: `class YourService:`
3. Add static methods for functionality
4. Update `services/__init__.py` to export it
5. Import and use in `app.py`

Example:
```python
# services/your_service.py
class YourService:
    @staticmethod
    def do_something():
        pass
```

---

## 🧪 Testing Services

Each service can be tested independently:

```python
# test_services.py
from services.dark_mode_service import DarkModeService

def test_dark_mode_toggle():
    DarkModeService.set_theme(False)
    assert DarkModeService.get_theme_state() == False
    DarkModeService.toggle_theme()
    assert DarkModeService.get_theme_state() == True
```

---

## 📚 Service Documentation

Each service file contains:
- Comprehensive docstrings
- Type hints for parameters
- Usage examples in comments
- Clear method descriptions

---

**Services follow SOLID principles and are designed for easy extension and maintenance.**

