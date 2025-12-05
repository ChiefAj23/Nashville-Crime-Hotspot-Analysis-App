"""
Hotspot Analyzer - Identifies high-risk areas from crime data
"""
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
import json

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula (in meters)"""
    R = 6371000  # Earth radius in meters
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)

    a = np.sin(delta_phi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

    return R * c

def categorize_incident(desc):
    """Categorize incidents into risk levels"""
    desc = str(desc).upper()

    # High-risk categories
    high_risk = ["SHOTS FIRED", "PERSON WITH WEAPON", "HOLDUP / ROBBERY",
                 "FIGHT / ASSAULT", "BURGLARY - RESIDENCE", "BURGLARY - NON-RESIDENCE"]

    # Medium-risk categories
    medium_risk = ["THEFT", "DISORDERLY PERSON", "SUSPICIOUS PERSON",
                   "INVESTIGATE 911 HANG-UP CALL", "INTOXICATED PERSON"]

    if desc in high_risk:
        return "high"
    elif desc in medium_risk:
        return "medium"
    else:
        return "low"

def calculate_risk_score(row, high_weight=3, medium_weight=2, low_weight=1):
    """Calculate risk score for an incident"""
    risk_level = categorize_incident(row['Tencode Description'])
    if risk_level == "high":
        return high_weight
    elif risk_level == "medium":
        return medium_weight
    else:
        return low_weight

def identify_hotspots(data_path, min_incidents=50, radius_meters=500):
    """
    Identify high-risk hotspots from crime data

    Parameters:
    -----------
    data_path : str
        Path to cleaned crime data CSV
    min_incidents : int
        Minimum number of incidents to form a hotspot
    radius_meters : float
        Radius in meters for DBSCAN clustering

    Returns:
    --------
    hotspots : list of dict
        List of hotspot information dictionaries
    """

    # Load data
    print("Loading crime data...")
    data = pd.read_csv(data_path)

    # Filter valid coordinates
    data = data.dropna(subset=['Latitude', 'Longitude'])
    data = data[(data['Latitude'].between(36.0, 36.4)) &
                (data['Longitude'].between(-87.0, -86.5))]

    # Calculate risk scores
    data['Risk Score'] = data.apply(calculate_risk_score, axis=1)

    # Prepare coordinates for clustering
    coords = data[['Latitude', 'Longitude', 'Risk Score', 'Tencode Description']].copy()

    # Convert radius from meters to degrees (approximate)
    # 1 degree latitude ≈ 111 km, so 1 meter ≈ 1/111000 degrees
    eps_degrees = radius_meters / 111000

    print(f"Clustering incidents with DBSCAN (eps={eps_degrees:.6f} degrees, min_samples={min_incidents})...")

    # DBSCAN clustering
    dbscan = DBSCAN(eps=eps_degrees, min_samples=min_incidents)
    coords['Cluster'] = dbscan.fit_predict(coords[['Latitude', 'Longitude']].values)

    # Filter out noise points (cluster -1)
    clustered_data = coords[coords['Cluster'] != -1].copy()

    if len(clustered_data) == 0:
        print("No hotspots found. Try reducing min_incidents or increasing radius_meters.")
        return []

    # Calculate hotspot statistics
    hotspots = []
    for cluster_id in sorted(clustered_data['Cluster'].unique()):
        cluster_points = clustered_data[clustered_data['Cluster'] == cluster_id]

        # Calculate centroid
        centroid_lat = cluster_points['Latitude'].mean()
        centroid_lon = cluster_points['Longitude'].mean()

        # Calculate total risk score
        total_risk = cluster_points['Risk Score'].sum()
        total_incidents = len(cluster_points)

        # Count incidents by category
        high_risk_count = len(cluster_points[cluster_points['Risk Score'] == 3])
        medium_risk_count = len(cluster_points[cluster_points['Risk Score'] == 2])
        low_risk_count = len(cluster_points[cluster_points['Risk Score'] == 1])

        # Get most common incident types
        top_incidents = cluster_points['Tencode Description'].value_counts().head(5).to_dict()

        # Calculate hotspot radius (distance from centroid to farthest point)
        distances = []
        for _, point in cluster_points.iterrows():
            dist = haversine_distance(centroid_lat, centroid_lon,
                                     point['Latitude'], point['Longitude'])
            distances.append(dist)
        hotspot_radius = max(distances) if distances else radius_meters

        # Determine risk level
        risk_ratio = (high_risk_count + medium_risk_count) / total_incidents if total_incidents > 0 else 0
        if risk_ratio > 0.3 or high_risk_count > 10:
            severity = "High"
        elif risk_ratio > 0.15 or medium_risk_count > 20:
            severity = "Medium"
        else:
            severity = "Low"

        # Generate explanation
        explanation = generate_explanation(
            total_incidents, high_risk_count, medium_risk_count,
            top_incidents, severity
        )

        hotspot = {
            'id': int(cluster_id),
            'latitude': float(centroid_lat),
            'longitude': float(centroid_lon),
            'radius_meters': float(hotspot_radius),
            'total_incidents': int(total_incidents),
            'high_risk_count': int(high_risk_count),
            'medium_risk_count': int(medium_risk_count),
            'low_risk_count': int(low_risk_count),
            'total_risk_score': float(total_risk),
            'severity': severity,
            'top_incidents': top_incidents,
            'explanation': explanation
        }

        hotspots.append(hotspot)

    # Sort by total risk score (highest first)
    hotspots.sort(key=lambda x: x['total_risk_score'], reverse=True)

    print(f"Identified {len(hotspots)} hotspots")
    return hotspots

def generate_explanation(total_incidents, high_risk, medium_risk, top_incidents, severity):
    """Generate human-readable explanation for why to avoid this area"""

    reasons = []

    if high_risk > 0:
        reasons.append(f"{high_risk} high-risk incidents")

    if medium_risk > 0:
        reasons.append(f"{medium_risk} medium-risk incidents")

    if len(reasons) == 0:
        reasons.append(f"{total_incidents} total incidents")

    explanation = f"This area has a {severity.lower()} crime risk with {', '.join(reasons)} recorded. "

    # Add specific incident types
    if top_incidents:
        top_types = list(top_incidents.keys())[:3]
        explanation += f"Most common incidents include: {', '.join([t.lower().replace(' - ', ' ') for t in top_types])}. "

    # Add safety advice
    if severity == "High":
        explanation += "It is strongly recommended to avoid this area, especially at night. If you must travel through, stay alert and consider using well-lit routes."
    elif severity == "Medium":
        explanation += "Exercise caution when visiting this area. Stay aware of your surroundings and avoid isolated locations."
    else:
        explanation += "While generally safe, be mindful of your surroundings and follow standard safety precautions."

    return explanation

def save_hotspots(hotspots, output_path='data/processed/hotspots.json'):
    """Save hotspots to JSON file"""
    with open(output_path, 'w') as f:
        json.dump(hotspots, f, indent=2)
    print(f"Hotspots saved to {output_path}")

if __name__ == "__main__":
    # Identify hotspots
    hotspots = identify_hotspots(
        'data/processed/cleaned_nashville_911_data.csv',
        min_incidents=30,  # Lower threshold to get more hotspots
        radius_meters=400  # 400 meter radius
    )

    # Save to JSON
    save_hotspots(hotspots, 'data/processed/hotspots.json')

    # Print summary
    print("\n" + "="*60)
    print("HOTSPOT SUMMARY")
    print("="*60)
    for hotspot in hotspots[:10]:  # Show top 10
        print(f"\nHotspot #{hotspot['id']} - {hotspot['severity']} Risk")
        print(f"  Location: ({hotspot['latitude']:.4f}, {hotspot['longitude']:.4f})")
        print(f"  Radius: {hotspot['radius_meters']:.0f} meters")
        print(f"  Total Incidents: {hotspot['total_incidents']}")
        print(f"  Risk Score: {hotspot['total_risk_score']:.0f}")
        print(f"  Explanation: {hotspot['explanation'][:150]}...")

