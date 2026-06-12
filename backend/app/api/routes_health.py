import logging

from fastapi.responses import JSONResponse
from fastapi import APIRouter
from app.core.config import REDIS_HOST, REDIS_PORT, REDIS_DB, WEATHER_CITY
from app.clients.redis_client import RedisClient

logger = logging.getLogger(__name__)
router = APIRouter()

redis_client = RedisClient(REDIS_HOST, REDIS_PORT, REDIS_DB)

@router.get("/health")
def health():
    logger.info("Health check requested")
    return {"status": "OK", "version": "1.0.0"}

@router.get("/ready")
def ready():
    try:
        logger.info("Readiness check started")
        redis_client.ping()
        last_good_exists = redis_client.exists(f"weather:{WEATHER_CITY}:last_good")
        if last_good_exists is False:
            logger.warning("Readiness check failed: last_good missing")
            return JSONResponse(
                status_code=503,
                content={"status":"not_ready","redis":"ok","last_good":"missing"}
            )
        
        logger.info("Readiness check passed")
        return {"status":"ready","redis":"ok","last_good":"ok"}
    except Exception:
        logger.exception("Readiness check failed because Redis is unavailable")
        return JSONResponse(
                status_code=503,
                content={"status":"not_ready","redis":"error"}
        )