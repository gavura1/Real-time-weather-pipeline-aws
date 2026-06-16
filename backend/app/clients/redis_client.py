from app.core.models import WeatherData
import json
import redis
import os

class RedisClient:
    def __init__(self, host, port, db):
        ssl = os.getenv("REDIS_SSL", "false").lower() == "true"
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            ssl=ssl,
            ssl_cert_reqs=None
        )

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

    def get_last_good_weather(self, city: str) -> WeatherData | None:
        key = f"weather:{city}:last_good"
        raw = self.client.get(key)
        if raw is None:
            return None
        else:
            decoded = raw.decode("utf-8")
            data = json.loads(decoded)
            model = WeatherData(**data)
        return model

    def ping(self) -> bool:
        return bool(self.client.ping())

    def exists(self, key: str) -> bool:
        return self.client.exists(key) == 1