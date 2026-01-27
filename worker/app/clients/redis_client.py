import redis 

class RedisClient:
    def __init__(self, host, port, db):
        self.client = redis.Redis(host=host, port=port, db=db)

    def set_current_weather(self, city: str, json_value: str, ttl_seconds: int):
        key = f"weather:{city}:current"
        self.client.setex(key, ttl_seconds, json_value)

    def set_last_good_weather(self, city: str, json_value: str):
        key = f"weather:{city}:last_good"
        self.client.set(key, json_value) 