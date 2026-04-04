#v2 deployment

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import scoring
from app.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs on startup
    init_db()
    print("Database initialized.")
    yield
    # Runs on shutdown (nothing needed here)

app = FastAPI(
    title="SentinelScore API",
    description="Real-time transaction fraud scoring API",
    version="1.0.0",
    lifespan=lifespan
)

# Register routers
app.include_router(scoring.router, prefix="/api/v1", tags=["Scoring"])

@app.get("/health")
def health_check():
    return {"status": "healthy", "model": "xgboost_best"}