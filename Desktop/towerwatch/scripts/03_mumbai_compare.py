import pandas as pd
import os

df = pd.read_csv('data/cleaned.csv')

# Filter Mumbai
mumbai = df[df['circle'] == 'Mumbai']

print(f"Mumbai records: {len(mumbai)}")

# Compare operators
comparison = mumbai.groupby('operator').agg({
    'download_speed': ['mean', 'median', 'std', 'count'],
    'upload_speed': ['mean', 'median'],
    'latency_ms': ['mean', 'median'],
    'signal_strength': 'mean',
    'quality_score': 'mean'
}).round(2)

print("\n=== MUMBAI OPERATOR COMPARISON ===")
print(comparison)

# 4G vs 5G breakdown
tech_breakdown = mumbai.groupby(['operator', 'technology']).agg({
    'download_speed': 'mean',
    'quality_score': 'mean'
}).round(2)

print("\n=== 4G vs 5G AVG DOWNLOAD & QUALITY ===")
print(tech_breakdown)

# Save for viz
os.makedirs('output', exist_ok=True)
mumbai.to_csv('output/mumbai_data.csv', index=False)
tech_breakdown.to_csv('output/mumbai_tech_breakdown.csv')
print("\nSaved: output/mumbai_data.csv, output/mumbai_tech_breakdown.csv")
