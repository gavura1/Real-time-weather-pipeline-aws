import redis
import json
from clients.weather_api import fetch_current_weather
from clients.redis_client import RedisClient
from core.config import WEATHER_TTL_SECONDS

def run_weather_job(city: str, redis_client: RedisClient) -> None:
    result = fetch_current_weather(city)

    if result is None:
        print("None result")
        return
    else:
        dict_data = result.model_dump()
        json_value = json.dumps(dict_data)
        redis_client.set_current_weather(city, json_value, WEATHER_TTL_SECONDS)

