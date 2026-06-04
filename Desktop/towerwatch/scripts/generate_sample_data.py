import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Indian telecom circles
CIRCLES = [
    'Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata',
    'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow'
]

# Operators
OPERATORS = ['jio', 'airtel', 'vi']

# Technologies
TECHS = ['4G', '5G']

# Generate 50,000 sample records
n_records = 50000

data = []

for i in range(n_records):
    circle = random.choice(CIRCLES)
    operator = random.choice(OPERATORS)
    tech = random.choice(TECHS)
    
    # Base speeds by operator and tech (realistic India ranges)
    if operator == 'jio':
        base_download = 25 if tech == '4G' else 85
        base_upload = 8 if tech == '4G' else 25
    elif operator == 'airtel':
        base_download = 22 if tech == '4G' else 75
        base_upload = 7 if tech == '4G' else 22
    else:  # vi
        base_download = 18 if tech == '4G' else 60
        base_upload = 6 if tech == '4G' else 18
    
    # Add noise and location variation
    download = max(1, base_download + np.random.normal(0, base_download * 0.3))
    upload = max(1, base_upload + np.random.normal(0, base_upload * 0.3))
    
    # Signal strength (RSRP in dBm, negative)
    signal = -85 + np.random.normal(0, 12)
    signal = min(-60, max(-120, signal))  # Clamp to realistic range
    
    # Latency
    latency = 35 + np.random.exponential(15)
    
    # Random date in last 90 days
    date = datetime(2026, 3, 1) + timedelta(days=random.randint(0, 90))
    
    # Random coordinates within India rough bounds
    lat = 8 + random.random() * 28  # 8°N to 36°N
    lon = 68 + random.random() * 28  # 68°E to 96°E
    
    data.append({
        'test_id': f'TEST_{i:06d}',
        'operator': operator,
        'technology': tech,
        'circle': circle,
        'download_speed': round(download, 2),
        'upload_speed': round(upload, 2),
        'signal_strength': round(signal, 2),
        'latency_ms': round(latency, 2),
        'test_date': date.strftime('%Y-%m-%d'),
        'latitude': round(lat, 6),
        'longitude': round(lon, 6)
    })

df = pd.DataFrame(data)

# Save as our "TRAI" data
df.to_csv('data/trai_myspeed_2026_05.csv', index=False)

print(f"Generated {len(df)} sample records")
print(f"\nOperators:\n{df['operator'].value_counts()}")
print(f"\nTechnologies:\n{df['technology'].value_counts()}")
print(f"\nCircles:\n{df['circle'].value_counts().head()}")
print(f"\nSample download speeds:")
print(df.groupby(['operator', 'technology'])['download_speed'].mean().round(2))
