import pandas as pd

df = pd.read_csv('data/cleaned.csv')

# Analysis for all 10 circles
all_cities = df.groupby(['circle', 'operator']).agg({
    'download_speed': ['mean', 'median', 'count'],
    'upload_speed': 'mean',
    'latency_ms': 'mean',
    'quality_score': 'mean'
}).round(2)

print("=== ALL CITIES: OPERATOR COMPARISON ===")
print(all_cities)

# City rankings by best operator
city_best = df.groupby(['circle', 'operator'])['quality_score'].mean().unstack()
print("\n=== CITY QUALITY SCORES BY OPERATOR ===")
print(city_best.round(2))

# Best operator per city
best_per_city = city_best.idxmax(axis=1)
print("\n=== BEST OPERATOR PER CITY ===")
for city, op in best_per_city.items():
    score = city_best.loc[city, op]
    print(f"{city:15s} {op:10s} {score:.2f}")

# Save
all_cities.to_csv('output/all_cities_analysis.csv')
city_best.to_csv('output/city_quality_matrix.csv')
print("\nSaved: output/all_cities_analysis.csv, output/city_quality_matrix.csv")