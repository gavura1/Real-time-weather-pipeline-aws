import os

REDIS_HOST = os.getenv("REDIS_HOST")

if not REDIS_HOST:
    raise RuntimeError("REDIS_HOST is not set")

REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

STALE_AFTER_SECONDS= int(os.getenv("STALE_AFTER_SECONDS", 300))
MAX_AGE_SECONDS= int(os.getenv("MAX_AGE_SECONDS", 10800))
