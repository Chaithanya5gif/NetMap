import pandas as pd

# Load
df = pd.read_csv('data/trai_myspeed_2026_05.csv')

# Convert date
df['test_date'] = pd.to_datetime(df['test_date'])

# Ensure numeric types
df['download_speed'] = pd.to_numeric(df['download_speed'])
df['upload_speed'] = pd.to_numeric(df['upload_speed'])
df['signal_strength'] = pd.to_numeric(df['signal_strength'])
df['latency_ms'] = pd.to_numeric(df['latency_ms'])

# Standardize operator names (already clean, but enforce)
df['operator'] = df['operator'].str.lower().str.strip()

# Standardize technology
df['technology'] = df['technology'].str.upper().str.strip()

# Add quality score (composite metric)
# Higher download, lower latency, stronger signal (less negative) = better
df['quality_score'] = (
    (df['download_speed'] / df['download_speed'].max() * 40) +
    (df['upload_speed'] / df['upload_speed'].max() * 20) +
    ((120 + df['signal_strength']) / 60 * 20) +  # Normalize -120 to -60 → 0 to 20
    (100 / (df['latency_ms'] + 1) * 20)  # Inverse latency
).round(2)

# Save
df.to_csv('data/cleaned.csv', index=False)

print(f"Cleaned: {len(df)} rows")
print(f"Date range: {df['test_date'].min()} to {df['test_date'].max()}")
print(f"\nQuality score stats:")
print(df['quality_score'].describe())
print(f"\nOperator quality ranking:")
print(df.groupby('operator')['quality_score'].mean().sort_values(ascending=False).round(2))
