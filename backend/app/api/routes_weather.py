import time
from fastapi import APIRouter, HTTPException
from app.clients.redis_client import RedisClient
from app.core.models import WeatherData
from app.services.weather_service import get_current_weather, get_last_good_weather
from app.core.config import REDIS_HOST, REDIS_PORT, REDIS_DB, STALE_AFTER_SECONDS, MAX_AGE_SECONDS

router = APIRouter()

redis_client = RedisClient(REDIS_HOST, REDIS_PORT, REDIS_DB)

@router.get("/weather/current")
def weather_current(city: str):
    print(f"city param = '{city}'")

    result = get_current_weather(city, redis_client)
    if result is None:
        result = get_last_good_weather(city, redis_client)
    if result is None:
        raise HTTPException(status_code=503, detail="Weather data unavailable")

    now = int(time.time())
    age = now - result.stored_at

    result.is_stale = age > STALE_AFTER_SECONDS

    if age > MAX_AGE_SECONDS:
        raise HTTPException(status_code=503, detail="Weather data too old")
    
    return result