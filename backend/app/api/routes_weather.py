from fastapi import APIRouter, HTTPException
from app.clients.redis_client import RedisClient
from app.core.models import WeatherData
from app.services.weather_service import get_current_weather

router = APIRouter()

redis_client = RedisClient("localhost", 6379, 0)

@router.get("/weather/current")
def weather_current(city: str):
    result = get_current_weather(city, redis_client)
    if result is None:
        raise HTTPException(status_code=503, detail="Weather data unavailable")
    else:
        return result