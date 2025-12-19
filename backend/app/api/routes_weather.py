from fastapi import APIRouter, HTTPException
from app.clients.redis_client import RedisClient
from app.core.models import WeatherData
from app.services.weather_service import get_current_weather
from app.core.config import REDIS_HOST, REDIS_PORT, REDIS_DB

router = APIRouter()

redis_client = RedisClient(REDIS_HOST, REDIS_PORT, REDIS_DB)

@router.get("/weather/current")
def weather_current(city: str):
    result = get_current_weather(city, redis_client)
    if result is None:
        raise HTTPException(status_code=503, detail="Weather data unavailable")
    else:
        return result