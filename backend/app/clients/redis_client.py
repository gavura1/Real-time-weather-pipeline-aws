from app.core.models import WeatherData
import json
import redis 

class RedisClient:
    def __init__(self, host, port, db):
        self.client = redis.Redis(host=host, port=port, db=db)

    def get_current_weather(self, city: str) -> WeatherData | None:
        key = f"weather:{city}:current"

        raw = self.client.get(key)

        if raw is None:
            return None
        else:
            decoded = raw.decode("utf-8")
            data = json.loads(decoded)
            model = WeatherData(**data)

        return model

        