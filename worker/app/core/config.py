import os

REDIS_HOST = os.getenv("REDIS_HOST")

if not REDIS_HOST:
    raise RuntimeError("REDIS_HOST is not set")

REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not OPENWEATHER_API_KEY:
    raise RuntimeError("OPENWEATHER_API_KEY is not set")

OPENWEATHER_BASE_URL = os.getenv("OPENWEATHER_BASE_URL")

if not OPENWEATHER_BASE_URL:
    raise RuntimeError("OPENWEATHER_BASE_URL is not set")

OPENWEATHER_UNITS = os.getenv("OPENWEATHER_UNITS", "metric")
OPENWEATHER_LANG = os.getenv("OPENWEATHER_LANG", "en")
WEATHER_TTL_SECONDS = int(os.getenv("WEATHER_TTL_SECONDS", 300))
FETCH_INTERVAL_SECONDS = int(os.getenv("FETCH_INTERVAL_SECONDS", 60))