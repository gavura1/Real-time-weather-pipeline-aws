import redis
import json
import logging

from clients.weather_api import fetch_current_weather
from clients.redis_client import RedisClient
from core.config import WEATHER_TTL_SECONDS

logger = logging.getLogger(__name__)

def run_weather_job(city: str, redis_client: RedisClient) -> None:
    logger.info("Fetching weather from API for city=%s", city)
    result = fetch_current_weather(city)

    if result is None:
        logger.warning("weather API returned no usable result for city=%s", city)
        return
    else:
        dict_data = result.model_dump()
        json_value = json.dumps(dict_data)
        redis_client.set_current_weather(city, json_value, WEATHER_TTL_SECONDS)
        logger.info("current weather stored in Redis for city-%s ttl-%s", city, WEATHER_TTL_SECONDS)

        redis_client.set_last_good_weather(city, json_value)
        logger.info("Last good weather stored in Redis for city=%s", city)

