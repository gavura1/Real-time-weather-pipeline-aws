import requests
from core.models import WeatherData
from core.config import OPENWEATHER_API_KEY, OPENWEATHER_BASE_URL, OPENWEATHER_LANG, OPENWEATHER_UNITS
from datetime import datetime, timezone

def fetch_current_weather(city: str) -> WeatherData | None:
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": OPENWEATHER_UNITS,
        "lang": OPENWEATHER_LANG
    }

    response = requests.get(OPENWEATHER_BASE_URL, params=params)

    if response.status_code != 200:
        return None
    
    data = response.json()

    speed_ms = data["wind"]["speed"]
    speed_kmh = speed_ms * 3.6

    weather = WeatherData(
        location = data["name"],
        temperature = data["main"]["temp"],
        condition = data["weather"][0]["description"],
        feels_like = data["main"]["feels_like"],                       
        wind = f'{speed_kmh} km/h',
        temp_unit = "°C",
        wind_unit = "km/h",
        time_stamp = datetime.fromtimestamp(data["dt"], tz=timezone.utc).isoformat(),
        is_stale = False
    )
    return weather
        