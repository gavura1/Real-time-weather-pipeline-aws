import requests
import time
from core.models import WeatherData
from core.config import OPENWEATHER_API_KEY, OPENWEATHER_BASE_URL, OPENWEATHER_LANG, OPENWEATHER_UNITS
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

def fetch_current_weather(city: str) -> WeatherData | None:
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": OPENWEATHER_UNITS,
        "lang": OPENWEATHER_LANG
    }

    try:
        response = requests.get(OPENWEATHER_BASE_URL, params=params)
    except requests.RequestException:
        logger.exception("OpenWeather request failed for city=%s", city)
        return None

    if response.status_code != 200:
        logger.warning("OpenWeather returned non-200 response for city=%s status=%s body=%s", city, response.status_code, response.text)
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
        stored_at = int(time.time()),
        is_stale = False
    )

    logger.info("OpenWeather fetch succeeded for city=%s location=%s", city, weather.location)
    return weather
        