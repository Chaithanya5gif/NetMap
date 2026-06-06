import pandas as pd
import json

df = pd.read_csv('data/mumbai_realistic.csv')

# Round to 2 decimals for clustering
grouped = df.groupby(['operator', 'technology', 
                        df['latitude'].round(2), 
                        df['longitude'].round(2)]).agg({
    'download_speed': 'mean',
    'quality_score': 'mean'
}).reset_index()

features = []
for _, row in grouped.iterrows():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [float(row['longitude']), float(row['latitude'])]
        },
        "properties": {
            "operator": row['operator'],
            "technology": row['technology'],
            "avg_download": round(float(row['download_speed']), 2),
            "avg_quality": round(float(row['quality_score']), 2)
        }
    }
    features.append(feature)

geojson = {"type": "FeatureCollection", "features": features}
with open('map/mumbai_realistic.geojson', 'w') as f:
    json.dump(geojson, f)

print(f"Generated {len(features)} points for Mumbai map")
