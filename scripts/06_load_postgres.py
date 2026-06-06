import pandas as pd
from sqlalchemy import create_engine, text

# Connection
engine = create_engine('postgresql://tw_user:your_password@localhost:5432/towerwatch')

df = pd.read_csv('data/cleaned.csv')

# Load to PostgreSQL
df.to_sql('measurements', engine, if_exists='replace', index=False, chunksize=1000)

# Verify
with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT operator, COUNT(*) as tests, 
               ROUND(AVG(download_speed)::numeric, 2) as avg_down,
               ROUND(AVG(quality_score)::numeric, 2) as avg_quality
        FROM measurements 
        GROUP BY operator 
        ORDER BY avg_quality DESC
    """))
    print("=== DATABASE VERIFICATION ===")
    for row in result:
        print(f"{row.operator:10s} {row.tests:6d} tests  {row.avg_down:6.2f} Mbps  {row.avg_quality:.2f} quality")

    # Count total
    total = conn.execute(text("SELECT COUNT(*) FROM measurements"))
    print(f"\nTotal rows loaded: {total.scalar()}")
