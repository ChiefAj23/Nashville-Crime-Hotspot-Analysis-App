# 🗺️ Nashville Crime Hotspot Analysis App

Hey there! 👋 I'm from Nashville, Tennessee - the home of country music. As country music has been getting more popular worldwide, Nashville has become a major tourist destination. With more visitors coming to explore Music City, I wanted to build something that would help keep them safe.

This application helps tourists (and locals too!) avoid high-crime areas and get real-time alerts when they're near potentially dangerous locations. It's my way of making sure everyone can enjoy everything Nashville has to offer while staying safe.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![React](https://img.shields.io/badge/React-18.2+-blue.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5.2+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📊 How It Works: The Science Behind the App

I've always been fascinated by data and how we can use it to solve real-world problems. For this project, I dove deep into Nashville's crime data to figure out where the hotspots are and how to warn people about them.

### The Approach

Instead of just looking at raw numbers, I used machine learning to find patterns in the data. The app analyzes thousands of 911 calls from the Metro Nashville Police Department and identifies areas where crime tends to cluster together.

### The Algorithm: DBSCAN Clustering

I chose **DBSCAN (Density-Based Spatial Clustering)** because it's perfect for this kind of problem. Unlike some other methods, it doesn't need me to tell it how many crime hotspots to find - it figures that out on its own by looking at where incidents naturally cluster together.

Here's how it works:
- It looks at all the crime locations and finds areas where incidents are densely packed
- I set it to look within a 400-meter radius (about a quarter mile)
- It only creates a hotspot if there are at least 30 incidents in that area
- This helps filter out random one-off incidents and focus on real problem areas

```python
# This is the core clustering code
dbscan = DBSCAN(eps=eps_degrees, min_samples=min_incidents)
coords['Cluster'] = dbscan.fit_predict(coords[['Latitude', 'Longitude']].values)
```

### Risk Scoring: Not All Crimes Are Equal

A stolen bike is different from a shooting, right? So I created a weighted scoring system:

- **High Risk** (Weight: 3): Things like shots fired, weapons, robberies, assaults, and burglaries
- **Medium Risk** (Weight: 2): Theft, disorderly conduct, suspicious activity
- **Low Risk** (Weight: 1): Everything else

This way, an area with 10 shootings gets flagged as more dangerous than an area with 30 noise complaints.

### How We Classify Hotspots

After analyzing the data, each hotspot gets labeled as High, Medium, or Low risk:

- **High Risk**: Either more than 30% of incidents are high-risk, or there are more than 10 serious incidents
- **Medium Risk**: Either more than 15% are medium/high risk, or there are more than 20 medium-risk incidents
- **Low Risk**: Everything else

I wanted to be conservative here - if there's any doubt, I'd rather flag something as risky than miss it.

### The Math Behind It

I use the Haversine formula to calculate distances accurately (because the Earth is round, not flat!). The app calculates:
- Where the center of each hotspot is
- How big the hotspot area is (the radius)
- How far you are from any hotspot

### The Data Pipeline

Here's what happens behind the scenes:

```
Raw 911 Data from Metro Nashville Police
    ↓
Clean it up (remove bad coordinates, filter outliers)
    ↓
Calculate risk scores for each incident
    ↓
Use DBSCAN to find clusters
    ↓
Calculate statistics for each hotspot
    ↓
Save everything to a JSON file
```

### What Makes This Special

- **Smart Categorization**: Automatically sorts incidents by severity
- **Time Analysis**: Looks at when crimes happen (some areas are safer during the day)
- **Spatial Intelligence**: Uses real geography to find clusters
- **Multi-Factor Scoring**: Doesn't just count crimes, it weighs them
- **Trend Detection**: Can spot if an area is getting better or worse over time

All of this is based on real data from the **Metro Nashville Police Department's 911 Calls for Service** - it's all publicly available, which is pretty cool!

---

## 🔧 The Backend: Making It All Work

I built the backend using **FastAPI** because it's fast, modern, and makes it easy to build APIs. Plus, it automatically generates documentation, which is super helpful.

### What Powers It

- **FastAPI**: The web framework (it's really fast!)
- **Uvicorn**: The server that runs everything
- **Pydantic**: Makes sure all the data is valid
- **Python 3.8+**: The programming language

### The Structure

```
backend/
├── main.py              # All the API endpoints
├── requirements.txt     # What needs to be installed
└── __init__.py
```

### What You Can Do With the API

I've set up endpoints for pretty much everything:

**Hotspots**
- Get all the hotspots
- Filter them by risk level, crime type, or time of day

**Route Planning**
- Calculate safe routes between two points
- Get alternative routes if the first one goes through a bad area

**Safety Analysis**
- Check how safe a specific location is
- See what hotspots are nearby

**Nearby Places**
- Find hospitals, police stations, and other safe places nearby

**Weather Integration**
- Get weather data (because bad weather can affect safety)

**Trends & Analysis**
- See crime trends over time (monthly, seasonal, daily, yearly)
- Understand when crimes are most likely to happen

**User Preferences**
- Save your favorite locations
- Customize alert settings
- Set your risk tolerance

**Emergency Contacts**
- Quick access to emergency numbers

### The Microservices

I organized the code into separate services so it's easier to maintain and understand:

- `route_planning_service.py` - Figures out safe routes
- `time_analysis_service.py` - Analyzes when crimes happen
- `safety_score_service.py` - Calculates safety scores
- `crime_filter_service.py` - Filters by crime type
- `distance_service.py` - Does all the distance math
- `nearby_places_service.py` - Finds safe places nearby
- `historical_trends_service.py` - Analyzes trends
- `weather_integration_service.py` - Gets weather data
- `user_preferences_service.py` - Manages user settings
- `emergency_contacts_service.py` - Emergency info

Each one does one thing well, which makes the code cleaner and easier to work with.

---

## 🎨 The Frontend: What You Actually See

I wanted the app to look good and be easy to use. So I built it with **React** and **TypeScript** - modern tools that let me create a really smooth experience.

### The Tech Stack

- **React 18**: The UI framework (it's what makes everything interactive)
- **TypeScript**: Adds type safety (catches bugs before they happen)
- **Vite**: Super fast build tool
- **Tailwind CSS**: Makes styling easier
- **React Router**: Handles navigation
- **Leaflet**: The map library (it's really good!)
- **Zustand**: Manages app state
- **Axios**: Handles API calls
- **Framer Motion**: Smooth animations
- **Recharts**: Makes pretty charts

### The Structure

```
frontend/
├── src/
│   ├── App.tsx              # The main app
│   ├── main.tsx             # Where it all starts
│   ├── components/          # Reusable pieces
│   │   ├── Layout.tsx       # The page layout
│   │   ├── FilterPanel.tsx # The filters
│   │   └── GPSTracker.tsx  # Location tracking
│   ├── pages/              # Different pages
│   │   ├── MapView.tsx     # The map
│   │   ├── RoutePlanner.tsx # Route planning
│   │   ├── Statistics.tsx  # Stats dashboard
│   │   ├── SafetyCalculator.tsx # Safety scores
│   │   ├── Trends.tsx      # Trend analysis
│   │   └── Settings.tsx    # Settings
│   ├── services/           # API calls
│   ├── store/              # State management
│   ├── types/              # TypeScript types
│   └── utils/              # Helper functions
```

### What You Can Do

- **Interactive Map**: See all the hotspots on a map, click them for details
- **Real-time Tracking**: Get alerts when you're near a risky area
- **Route Planning**: Find safe routes to where you want to go
- **Statistics**: See all the data in one place
- **Safety Calculator**: Check how safe any location is
- **Trends**: See how crime patterns change over time
- **Dark Mode**: Because sometimes you want a dark theme
- **Mobile Friendly**: Works on your phone too!
- **Filtering**: Filter by risk level, crime type, time of day
- **Favorites**: Save places you visit often

---

## 🚀 Getting Started: Let's Get This Running!

Alright, let's get you set up! It's not too complicated, I promise.

### What You'll Need

- **Python 3.8 or higher** (and pip)
- **Node.js 18 or higher** (and npm)
- **Git** (optional, but helpful)

### Step 1: Generate the Hotspot Data

First things first - we need to analyze the crime data and create the hotspot file.

```bash
# Install the Python packages we need
pip install -r requirements.txt

# Run the analyzer (this might take a minute)
python hotspot_analyzer.py
```

This will create a file called `data/processed/hotspots.json` with all the crime hotspots we found. Think of it as the brain of the app!

### Step 2: Start the Backend

The backend is what serves all the data to the frontend. You have a few options:

#### Option A: Use the Startup Script (Easiest!)

I made a script to make this easier:

```bash
# Make it executable (only needed once)
chmod +x start_backend.sh

# Run it!
./start_backend.sh
```

#### Option B: Do It Manually

If you prefer to do it yourself:

```bash
# Go to the backend folder
cd backend

# Install the dependencies
pip install -r requirements.txt

# Start the server
python main.py

# Or use uvicorn directly (same thing)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Option C: Use a Virtual Environment (Recommended for Clean Setup)

This keeps everything isolated:

```bash
cd backend

# Create a virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python main.py
```

Once it's running, you'll see:
- **API**: `http://localhost:8000`
- **API Docs**: `http://localhost:8000/docs` (this is really cool - check it out!)
- **Alternative Docs**: `http://localhost:8000/redoc`

Keep this terminal window open - the backend needs to keep running!

### Step 3: Start the Frontend

Open a **new terminal window** (keep the backend running in the first one!) and run:

```bash
# Go to the frontend folder
cd frontend

# Install dependencies (only needed the first time)
npm install

# Start the development server
npm run dev
```

This will start the frontend at `http://localhost:3000`

The frontend automatically connects to the backend on port 8000, so make sure that's running first!

### Step 4: Open It Up!

1. Open your browser and go to `http://localhost:3000`
2. You should see the app load up
3. Explore the map, check out the statistics, and try the different features!

### Alternative: Just Use the Streamlit App

If you don't want to deal with the backend and frontend setup, there's also a simpler Streamlit version:

```bash
# Install dependencies
pip install -r requirements.txt

# Generate hotspots (if you haven't already)
python hotspot_analyzer.py

# Run the Streamlit app
streamlit run app.py
```

Then just go to `http://localhost:8501` in your browser. It's simpler but has fewer features.

---

## 📖 How to Use It

Once you have it running, here's what you can do:

### The Map View

This is probably where you'll spend most of your time. You'll see:
- **Red circles**: High-risk areas (be careful here!)
- **Orange circles**: Medium-risk areas (stay alert)
- **Green circles**: Low-risk areas (generally safe)
- **Blue marker**: Your current location (if you enable tracking)

Click on any hotspot to see details about it - how many incidents, what types of crimes, and why it's flagged.

### Location Tracking

Turn on location tracking to get real-time alerts:
- The app will ask for your location (you can allow or deny)
- If you're near a high-risk area, you'll get a warning
- You can also manually enter your location if GPS isn't working

### Route Planning

Planning a trip? Use the route planner:
- Enter your starting point and destination
- The app will find a safe route that avoids high-risk areas
- You can see alternative routes too
- Each route shows a safety score

### Statistics Dashboard

Want to see the big picture? Check out the statistics:
- Total number of hotspots
- How many are high/medium/low risk
- Detailed information about each hotspot
- Top areas to avoid

### Safety Calculator

Curious about a specific location?
- Enter the address or coordinates
- Get a safety score
- See what hotspots are nearby
- Get recommendations

### Trends Analysis

See how things change over time:
- Monthly trends
- Seasonal patterns
- Day-of-week analysis
- Year-over-year comparisons

### Understanding the Risk Levels

- **🔴 High Risk**: Lots of serious crime here - I'd avoid these areas, especially at night
- **🟠 Medium Risk**: Some crime activity - be cautious and stay aware
- **🟢 Low Risk**: Generally safe, but always stay alert

---

## 🔧 Configuration: Making It Your Own

Want to tweak things? Here's how:

### Backend Settings

- **CORS**: Currently set to allow `http://localhost:3000` (the React frontend)
- **Hotspots File**: Looks for `data/processed/hotspots.json` in the project root
- **Port**: Default is 8000, but you can change it in `backend/main.py`

### Frontend Settings

- **API URL**: Set to `http://localhost:8000` by default
- **Change it**: Edit `frontend/src/services/api.ts` if your backend is somewhere else

### Hotspot Detection Settings

Want to adjust how hotspots are detected? Edit `hotspot_analyzer.py`:

```python
hotspots = identify_hotspots(
    'data/processed/cleaned_nashville_911_data.csv',
    min_incidents=30,      # Minimum incidents to form a hotspot
    radius_meters=400       # How big the area is (in meters)
)
```

Make `min_incidents` higher to get fewer, more serious hotspots. Make it lower to catch more areas.

### Risk Categories

Want to change what counts as high/medium/low risk? Edit the `categorize_incident()` function in `hotspot_analyzer.py`:

```python
high_risk = ["SHOTS FIRED", "PERSON WITH WEAPON", ...]
medium_risk = ["THEFT", "DISORDERLY PERSON", ...]
```

---

## 🛠️ Troubleshooting: When Things Go Wrong

Things not working? Let's fix it!

### Backend Problems

**Backend won't start:**
- Check Python version: `python --version` (needs 3.8+)
- Install dependencies: `pip install -r backend/requirements.txt`
- Make sure `data/processed/hotspots.json` exists
- Check if port 8000 is already in use:
  - macOS/Linux: `lsof -i :8000`
  - Windows: `netstat -ano | findstr :8000`

**Can't connect to the API:**
- Is the backend actually running? Check the terminal
- Look at the CORS settings in `backend/main.py`
- Make sure the frontend is pointing to the right URL

### Frontend Problems

**Frontend won't start:**
- Check Node version: `node --version` (needs 18+)
- Install dependencies: `cd frontend && npm install`
- Check if port 3000 is in use

**Can't connect to backend:**
- Is the backend running? (Check that terminal window!)
- Open browser console (F12) and look for errors
- Check the API URL in `frontend/src/services/api.ts`

### Data Problems

**No hotspots showing:**
- Did you run `python hotspot_analyzer.py`?
- Check that `data/processed/hotspots.json` exists
- Make sure file paths in the code are correct

**Location tracking not working:**
- Did you allow location access in your browser?
- Try the manual entry option instead
- Check the browser console for errors (F12)

**Map not loading:**
- Do you have internet? (Map tiles need internet)
- Are all dependencies installed?
- Try refreshing the page

---

## 📁 Project Structure: Where Everything Lives

Here's how I organized everything:

```
Nashville-Crime-Hotspot-Analysis_V2/
│
├── README.md                    # You're reading this!
├── requirements.txt             # Python packages
├── environment.yml              # Conda environment (optional)
├── start_backend.sh            # Backend startup script
│
├── app.py                       # Streamlit version (simpler)
├── hotspot_analyzer.py          # The brain - finds hotspots
├── components.py                # Custom components
│
├── backend/                     # The API server
│   ├── main.py                  # All the endpoints
│   ├── requirements.txt         # Backend dependencies
│   └── __init__.py
│
├── frontend/                    # The web app
│   ├── src/                     # All the React code
│   ├── package.json            # Node dependencies
│   └── ...
│
├── services/                    # The microservices
│   └── *.py                     # Each service in its own file
│
├── tests/                       # Tests (because testing is important!)
│   └── *.py
│
├── data/
│   ├── raw/                     # Original data files
│   └── processed/              # Cleaned data and hotspots
│       ├── cleaned_nashville_911_data.csv
│       └── hotspots.json
│
├── notebooks/                   # Jupyter notebooks (for analysis)
│   └── *.ipynb
│
├── models/                      # Machine learning models
│   └── *.joblib
│
├── exports/                     # Generated files (maps, etc.)
│   ├── *.html
│   └── *.png
│
└── Asset/                       # Images for documentation
    └── *.png
```

---

## 🔒 Privacy & Security: Your Data Stays Yours

I care about privacy, so here's what happens with your data:

- **Your Location**: Processed in your browser, never sent anywhere
- **No Tracking**: I don't store or track your location
- **Local Processing**: All the hotspot detection runs on your machine
- **Open Source**: You can see exactly what the code does

---

## ⚠️ Important Safety Disclaimer

This app is a tool to help you make informed decisions, but it's not perfect. Always:

- Use your own judgment
- Follow local safety guidelines
- Stay aware of your surroundings
- Trust your instincts
- Call 911 in emergencies

The data is historical - it shows patterns from the past, but things can change. An area that was safe yesterday might not be safe today, and vice versa.

---

## 📝 License

This is open source under the MIT License. Feel free to use it, modify it, and share it!

---

## 👨‍💻 About Me

Hi! I'm **Abhijeet Solanki**, and I built this because I wanted to help keep people safe in my city. Nashville is an amazing place, and I want everyone to be able to enjoy it without worry.

This project uses:
- Machine learning to find crime patterns
- A modern React frontend
- A FastAPI backend
- Real data from Metro Nashville Police

If you have questions, suggestions, or just want to say hi, feel free to reach out!

---

## 🙏 Acknowledgments

Big thanks to:
- **Metro Nashville Police Department** for making their data publicly available
- **FastAPI** team for the awesome framework
- **React and TypeScript** communities for the great tools
- **Leaflet** for the mapping library
- Everyone in the open-source community who makes projects like this possible

---

**Made with ❤️ in Nashville, Tennessee**

*Stay Safe, Stay Informed, Stay Smart*

*And remember - Music City is a great place, but like any city, it pays to be aware of your surroundings!*


---

## Author

**Abhijeet Solanki** - AI Engineer (Edge AI + GenAI), 11 peer-reviewed IEEE publications on robust perception and edge AI.

[Portfolio](https://www.abhijeetsolanki.com/) | [LinkedIn](https://www.linkedin.com/in/abhijeet-solanki) | [GitHub](https://github.com/ChiefAj23)
