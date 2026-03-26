import logging
import time
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException
from app.clients.redis_client import RedisClient
from app.services.weather_service import get_current_weather, get_last_good_weather
from app.core.config import REDIS_HOST, REDIS_PORT, REDIS_DB, STALE_AFTER_SECONDS, MAX_AGE_SECONDS
from app.core.metrics import HTTP_REQUEST_TOTAL, WEATHER_CACHE_SOURCE_TOTAL, HTTP_REQUEST_DURATION_SECONDS 

logger = logging.getLogger(__name__)
router = APIRouter()

redis_client = RedisClient(REDIS_HOST, REDIS_PORT, REDIS_DB)

@router.get("/weather/current")
def weather_current(city: str):
    
    start = time.perf_counter()
    endpoint_label = "weather_current"

    HTTP_REQUEST_TOTAL.labels(endpoint=endpoint_label).inc()
    logger.info("Weather current requested for city=%s", city)

    source = "none"
    try:
        result = get_current_weather(city, redis_client)
        if result is not None:
            source = "current"
            logger.info("using current weather cache for city=%s", city)
        else:
            result = get_last_good_weather(city, redis_client)
            if result is not None:
                source = "last_good"
                logger.warning("using last_good fallback for city=%s", city)
    
        if result is None:
            WEATHER_CACHE_SOURCE_TOTAL.labels(source=source).inc()
            logger.error("Weather data unavailable for city=%s", city)
            raise HTTPException(status_code=503, detail="Weather data unavailable")

        now = int(time.time())
        age = now - result.stored_at

        result.is_stale = age > STALE_AFTER_SECONDS

        logger.info(
            "Weather data age checked for city=%s source=%s, age=%s, stale=%s", city, source, age, result.is_stale)

        if age > MAX_AGE_SECONDS:
            WEATHER_CACHE_SOURCE_TOTAL.labels(source=source).inc()
            logger.error("weather data too old for city=%s source=%s age=%s", city, source, age)
            raise HTTPException(status_code=503, detail="Weather data too old")
    
        WEATHER_CACHE_SOURCE_TOTAL.labels(source=source).inc()
        return result
    finally:
        duration = time.perf_counter() - start
        HTTP_REQUEST_DURATION_SECONDS.labels(endpoint=endpoint_label).observe(duration)
        logger.info("Weather current finished for city=%s in %.4f seconds", city, duration)

@router.get("/weather/status")
def weather_status(city: str):

    start = time.perf_counter()
    endpoint_label = "weather_status"

    HTTP_REQUEST_TOTAL.labels(endpoint=endpoint_label).inc()
    logger.info("Weather status requested for city=%s", city)

    try:
        try:
            redis_client.ping()

            current = redis_client.get_current_weather(city)
            last_good = redis_client.get_last_good_weather(city)

        except Exception:
            logger.exception("Redis error during weather status check for city=%s", city)
            return JSONResponse(status_code=503, content={"redis": "error"})

        current_exists = current is not None
        last_good_exists = last_good is not None

        selected = None

        if current_exists:
            source = "current"
            selected = current
        elif last_good_exists:
            source = "last_good"
            selected = last_good
        else:
            source = "none"
            selected = None

        if selected is not None:
            now = int(time.time())
            age_seconds = now - selected.stored_at
        else:
            age_seconds = None
            is_stale = None

        if age_seconds is None:
            is_stale = None
        else:
            is_stale = age_seconds > STALE_AFTER_SECONDS

        logger.info("Weather status result city=%s source=%s current_exists=%s last_good_exists=%s age_seconds=%s", city, source, current_exists, last_good_exists, age_seconds)

        return {
            "city": city,
            "redis": "ok",
            "source": source,
            "current_exists": current_exists,
            "last_good_exists": last_good_exists,
            "age_seconds": age_seconds,
            "is_stale": is_stale,
            "stale_after_seconds": STALE_AFTER_SECONDS,
            "max_age_seconds": MAX_AGE_SECONDS
        }
    finally:
        duration = time.perf_counter() - start
        HTTP_REQUEST_DURATION_SECONDS.labels(endpoint=endpoint_label).observe(duration)
        logger.info("Weather status finished for city=%s in %.4f seconds", city, duration)

    
    