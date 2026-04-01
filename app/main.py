from fastapi import FastAPI
from app.routers import scoring

app = FastAPI(
    title="SentinelScore API",
    description="Real-time transaction fraud scoring API",
    version="1.0.0"
)

# Register routers
app.include_router(scoring.router, prefix="/api/v1", tags=["Scoring"])

@app.get("/health")
def health_check():
    return {"status": "healthy", "model": "xgboost_best"}