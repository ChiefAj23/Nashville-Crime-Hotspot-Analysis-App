import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
from sklearn.cluster import KMeans, DBSCAN
import matplotlib.pyplot as plt
from collections import defaultdict

# ========== PAGE SETUP ==========
st.set_page_config(page_title="Nashville 911 Analysis Dashboard", layout="wide")

# ========== CUSTOM CSS ==========
st.markdown("""
    <style>
        .title {
            font-size: 2.5em;
            font-weight: 700;
            text-align: center;
            color: #ff4b4b;
        }
        .subtitle {
            text-align: center;
            color: gray;
        }
        .section-header {
            font-size: 2.5em;
            margin-top: 30px;
            color: #990aff;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🚨 Nashville 911 Hotspot and Cluster Analysis</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Developed By Abhijeet Solanki</div>", unsafe_allow_html=True)

# ========== INTRO ==========
st.markdown("""
---
### 🧠 What’s This All About?

This dashboard turns thousands of real 911 calls into an **interactive visual story** using clustering and heatmaps to:
- Highlight **hot zones** of emergency calls
- Understand what types of incidents happen and where
- Help city leaders **act smarter, faster, safer**

Whether you're just curious, a policymaker, or analyzing risk, this dashboard helps make Nashville safer — together.
---
""")

# ========== LOAD DATA ==========
data_path = '/Users/chiefaj/Abhijeet-Carrer/Projects/Nashville-Crime-Hotspot-Analysis/cleaned_nashville_911_data.csv'
data = pd.read_csv(data_path)

# Categorize incidents
def categorize_incident(desc):
    desc = str(desc).upper()
    if desc in ["FIGHT / ASSAULT", "VEHICLE ACCIDENT - PERSONAL INJURY"]:
        return "Medical/Accident-related"
    elif desc in ["SHOTS FIRED", "PERSON WITH WEAPON", "HOLDUP / ROBBERY"]:
        return "Violent/Criminal Activity"
    elif desc in ["TRAFFIC VIOLATION", "VEHICLE ACCIDENT - PROPERTY DAMAGE", "VEHICLE BLOCKING RIGHT OF WAY"]:
        return "Traffic & Vehicle-Related"
    elif desc in ["BURGLARY - RESIDENCE", "BURGLARY - NON-RESIDENCE", "THEFT"]:
        return "Burglary/Theft"
    elif desc in ["WANT OFFICER FOR INVESTIGATION / ASSISTA", "INVESTIGATE 911 HANG-UP CALL", "SUSPICIOUS PERSON", "MISSING PERSON"]:
        return "Police Engagement"
    elif desc in ["SAFETY HAZARD", "DISORDERLY PERSON", "DANGEROUS / INJURED ANIMAL"]:
        return "Public Safety / Community"
    elif desc in ["COMMUNITY POLICING ACTIVITY", "BUSINESS CHECK"]:
        return "Community Policing"
    else:
        return "Other"

data['Incident Category'] = data['Tencode Description'].apply(categorize_incident)

# ========== CATEGORY TABLE ==========
st.markdown("<div class='section-header'>📂 Incident Categorization</div>", unsafe_allow_html=True)
st.markdown("Grouped each 911 call into simplified categories to enable better clustering and insights.")
if st.button("🔍 Show Categorization Table"):
    category_table = data[['Tencode Description', 'Incident Category']].drop_duplicates().sort_values('Incident Category')
    st.dataframe(category_table, use_container_width=True)

# ========== HEATMAP ==========
st.markdown("<div class='section-header'>🌍 Heatmap of All 911 Calls</div>", unsafe_allow_html=True)
st.markdown("""
### 🚨 Problem Statement:
Where are 911 emergency calls concentrated in Nashville?

### 📊 Purpose:
This heatmap shows where calls are **densest** to identify hotspots.

- 🟦 Blue = Low activity
- 🟩 Green = Moderate to high activity

**Analysis**: Central Nashville has the most frequent calls. This helps agencies focus efforts in busy zones.
""")

heatmap_data = data[['Latitude', 'Longitude']].dropna()
heatmap_map = folium.Map(location=[heatmap_data['Latitude'].mean(), heatmap_data['Longitude'].mean()], zoom_start=11)
HeatMap(heatmap_data.values, radius=10).add_to(heatmap_map)
folium_static(heatmap_map)

# ========== CLUSTERING ==========
st.markdown("<div class='section-header'>🧠 Category-Wise Clustering Maps</div>", unsafe_allow_html=True)
st.markdown("""
### 🚨 Problem Statement:
Do different types of incidents form distinct spatial patterns?

### 📊 Purpose:
- **KMeans**: Finds dense clusters (centroids)
- **DBSCAN**: Captures less obvious patterns & outliers

**Analysis**: Each category’s clustering can help allocate emergency units to high-risk or spread-out areas.
""")

category_colors = {
    "Medical/Accident-related": 'red',
    "Violent/Criminal Activity": 'blue',
    "Traffic & Vehicle-Related": 'green',
    "Burglary/Theft": 'purple',
    "Police Engagement": 'orange',
    "Public Safety / Community": 'pink',
    "Community Policing": 'brown'
}

cluster_counts = defaultdict(int)

for category, color in category_colors.items():
    if st.button(f"🗺️ Show Map for {category}"):
        coords = data[data['Incident Category'] == category][['Latitude', 'Longitude']].dropna()
        if len(coords) >= 200:
            coords_sampled = coords.sample(frac=0.3, random_state=42)
            kmeans = KMeans(n_clusters=9, random_state=42, n_init=10)
            coords_sampled['kmeans_cluster'] = kmeans.fit_predict(coords_sampled)

            eps_meters = 260 / 111034.61  # ~260 meters
            dbscan = DBSCAN(eps=eps_meters, min_samples=15)
            coords_sampled['dbscan_cluster'] = dbscan.fit_predict(coords_sampled)

            dbscan_clusters = coords_sampled['dbscan_cluster'].nunique() - (1 if -1 in coords_sampled['dbscan_cluster'].values else 0)
            cluster_counts[category] = dbscan_clusters

            category_map = folium.Map(location=[coords_sampled['Latitude'].mean(), coords_sampled['Longitude'].mean()], zoom_start=12)
            for _, row in coords_sampled.iterrows():
                dbscan_color = 'yellow' if row['dbscan_cluster'] == -1 else 'blue'
                folium.CircleMarker(
                    location=[row['Latitude'], row['Longitude']],
                    radius=1,
                    color=dbscan_color,
                    fill=True,
                    fill_opacity=0.4
                ).add_to(category_map)
            for center in kmeans.cluster_centers_:
                folium.CircleMarker(
                    location=[center[0], center[1]],
                    radius=5,
                    color='black',
                    fill=True,
                    fill_opacity=1
                ).add_to(category_map)

            st.markdown(f"### 🔍 Insights for {category}")
            st.markdown("""
            - 📍 Each dot = emergency call
            - ⚫ KMeans centroid (black)
            - 🟦 DBSCAN cluster
            - 🟨 DBSCAN noise/outlier

            These maps reveal where incidents **concentrate** and where they are **dispersed**.
            """)
            folium_static(category_map)
        else:
            st.warning(f"Not enough data to generate map for {category}.")

# ========== CLUSTER COUNT BAR ==========
if cluster_counts:
    st.markdown("<div class='section-header'>📊 DBSCAN Cluster Count per Category</div>", unsafe_allow_html=True)
    st.markdown("""
### 🚨 Problem Statement:
Which types of incidents are highly clustered vs. spread out?

### 📊 Purpose:
Understand **how many clusters** DBSCAN found for each category.

**Analysis**: Higher counts = more widespread activity. Lower = concentrated zones.
""")

    cluster_df = pd.DataFrame.from_dict(cluster_counts, orient='index', columns=['Clusters']).sort_values('Clusters')
    fig, ax = plt.subplots(figsize=(10, 4))
    cluster_df.plot(kind='barh', ax=ax, color='skyblue', legend=False)
    ax.set_xlabel("Number of DBSCAN Clusters")
    ax.set_title("911 Clusters Detected by Category")
    st.pyplot(fig)

st.success("✅ Dashboard loaded successfully. Explore insights above!")
