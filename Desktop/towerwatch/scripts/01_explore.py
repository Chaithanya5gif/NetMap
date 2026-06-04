import pandas as pd

df = pd.read_csv('data/trai_myspeed_2026_05.csv')

print("=== DATA EXPLORATION ===")
print(f"Shape: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nFirst 3 rows:")
print(df.head(3))
print(f"\nData types:")
print(df.dtypes)
print(f"\nNull counts:")
print(df.isnull().sum())
print(f"\nBasic stats:")
print(df.describe())
