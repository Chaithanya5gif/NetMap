import pandas as pd
from sqlalchemy import create_engine, text
import json

engine = create_engine('postgresql://tw_user:your_password@localhost:5432/towerwatch')

# Round to 1 decimal for broader clustering
query = """
SELECT 
    operator,
    technology,
    ROUND(latitude::numeric, 1) as lat,
    ROUND(longitude::numeric, 1) as lon,
    COUNT(*) as tests,
    ROUND(AVG(download_speed)::numeric, 2) as avg_download,
    ROUND(AVG(quality_score)::numeric, 2) as avg_quality
FROM measurements
GROUP BY operator, technology, ROUND(latitude::numeric, 1), ROUND(longitude::numeric, 1)
"""

with engine.connect() as conn:
    df = pd.read_sql(text(query), conn)

print(f"Query returned {len(df)} rows")

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

with open('output/netmap_points.geojson', 'w') as f:
    json.dump(geojson, f)

print(f"Generated GeoJSON with {len(features)} points")
print(f"Operators: {df['operator'].unique().tolist()}")
print(f"Technologies: {df['technology'].unique().tolist()}")
