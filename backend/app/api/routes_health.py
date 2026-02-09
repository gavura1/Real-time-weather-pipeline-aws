from fastapi.responses import JSONResponse
from fastapi import APIRouter
from app.core.config import REDIS_HOST, REDIS_PORT, REDIS_DB
from app.clients.redis_client import RedisClient


router = APIRouter()

redis_client = RedisClient(REDIS_HOST, REDIS_PORT, REDIS_DB)

@router.get("/health")
def health():
    return {"status": "OK"}

@router.get("/ready")
def ready():
    try:
        redis_client.ping()
        last_good_exists = redis_client.exists("weather:Banska Bystrica:last_good")
        if last_good_exists is False:
            return JSONResponse(
                status_code=503,
                content={"status":"not_ready","redis":"ok","last_good":"missing"}
            )
        return {"status":"ready","redis":"ok","last_good":"ok"}
    except Exception:
        return JSONResponse(
                status_code=503,
                content={"status":"not_ready","redis":"error"}
        )