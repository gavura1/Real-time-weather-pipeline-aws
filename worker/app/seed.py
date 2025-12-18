import redis 
import json 
from core.models import WeatherData

host = "localhost" 
port = 6379 
db = 0 

weather = WeatherData( 
location="Banska Bystrica", 
temperature=10.0, 
condition="Rain", 
feels_like=8.5, 
wind="11 - 30", 
temp_unit="°C", 
wind_unit="km/h", 
time_stamp="2025-12-04T14:00:00Z", 
is_stale=False 
)

redis_client = redis.Redis(host="localhost", port=6379, db=0)

data = weather.model_dump() 
json_value = json.dumps(data) 
key = "weather:BanskaBystrica:current" 
redis_client.set(key, json_value)