import pandas as pd
from sqlalchemy import create_engine, text
import json

engine = create_engine('postgresql://tw_user:your_password@localhost:5432/towerwatch')

# Mumbai bounding box: roughly 18.8-19.4 N, 72.7-73.0 E
query = """
SELECT 
    operator,
    technology,
    ROUND(latitude::numeric, 2) as lat,
    ROUND(longitude::numeric, 2) as lon,
    COUNT(*) as tests,
    ROUND(AVG(download_speed)::numeric, 2) as avg_download,
    ROUND(AVG(quality_score)::numeric, 2) as avg_quality
FROM measurements
WHERE circle = 'Mumbai'
GROUP BY operator, technology, ROUND(latitude::numeric, 2), ROUND(longitude::numeric, 2)
"""

with engine.connect() as conn:
    df = pd.read_sql(text(query), conn)

print(f"Mumbai query returned {len(df)} rows")

features = []
for _, row in df.iterrows():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [float(row['lon']), float(row['lat'])]
        },
        "properties": {
            "operator": row['operator'],
            "technology": row['technology'],
            "tests": int(row['tests']),
            "avg_download": float(row['avg_download']),
            "avg_quality": float(row['avg_quality'])
        }
    }
    features.append(feature)

geojson = {
    "type": "FeatureCollection",
    "features": features
}

with open('output/mumbai_points.geojson', 'w') as f:
    json.dump(geojson, f)

print(f"Generated Mumbai GeoJSON with {len(features)} points")
