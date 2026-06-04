from fastapi import FastAPI
from sqlalchemy import create_engine, text
from typing import Optional

app = FastAPI(title="NetMap API", version="0.1.0")
engine = create_engine('postgresql://tw_user:your_password@localhost:5432/towerwatch')

@app.get("/")
def root():
    return {"message": "NetMap API", "status": "live", "version": "0.1.0"}

@app.get("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.get("/cities")
def get_cities():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DISTINCT circle FROM measurements ORDER BY circle"))
        return {"cities": [row.circle for row in result]}

@app.get("/compare/{city}")
def compare_city(city: str, technology: Optional[str] = None):
    query = """
        SELECT operator, 
               COUNT(*) as tests,
               ROUND(AVG(download_speed)::numeric, 2) as avg_download,
               ROUND(AVG(upload_speed)::numeric, 2) as avg_upload,
               ROUND(AVG(latency_ms)::numeric, 2) as avg_latency,
               ROUND(AVG(quality_score)::numeric, 2) as avg_quality
        FROM measurements 
        WHERE circle = :city
    """
    params = {"city": city}
    if technology:
        query += " AND technology = :tech"
        params["tech"] = technology
    
    query += " GROUP BY operator ORDER BY avg_quality DESC"
    
    with engine.connect() as conn:
        result = conn.execute(text(query), params)
        rows = [dict(row._mapping) for row in result]
        return {"city": city, "technology": technology or "all", "operators": rows}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
