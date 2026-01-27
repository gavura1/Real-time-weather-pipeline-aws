from app.clients.redis_client import RedisClient
from app.core.models import WeatherData 

def get_current_weather(city: str, redis_client: RedisClient) -> WeatherData | None:
    result = redis_client.get_current_weather(city)
    if result is None:
        return None
    else:
        return result
    
def get_last_good_weather(city: str, redis_client: RedisClient) -> WeatherData | None:
    result = redis_client.get_last_good_weather(city)
    if result is None:
        return None
    else:
        return result
