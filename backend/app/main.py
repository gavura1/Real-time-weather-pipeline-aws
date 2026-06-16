import logging
from fastapi import FastAPI
from app.api.routes_weather import router as weather_router
from app.api.routes_health import router as health_router
from app.api.routes_metrics import router as metric_router
from app.core.logging_config import setup_logging
from fastapi.middleware.cors import CORSMiddleware

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(weather_router)
app.include_router(health_router)
app.include_router(metric_router)

logger.info("Backend application started")

@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {"message": "Weather API running"}

