from fastapi import FastAPI
from app.api.routes_weather import router as weather_router
from app.api.routes_health import router as health_router
from app.api.routes_metrics import router as metric_router

app = FastAPI()

app.include_router(weather_router)
app.include_router(health_router)
app.include_router(metric_router)

@app.get("/")
def root():
    return {"message": "Weather API running"}

