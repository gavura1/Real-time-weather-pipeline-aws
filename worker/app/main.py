from clients.redis_client import RedisClient 
from jobs.weather_job import run_weather_job 
from core.config import FETCH_INTERVAL_SECONDS, REDIS_HOST, REDIS_PORT, REDIS_DB
from core.logging_config import setup_logging
import time 
import logging

setup_logging()
logger = logging.getLogger(__name__)

def main(): 
    logger.info("Worker application started")
    redis_client = RedisClient(REDIS_HOST, REDIS_PORT, REDIS_DB)
    
    while True: 
        try: 
            city = "Banska Bystrica" 
            logger.info("Worker iteration started for city=%s", city)
            run_weather_job(city, redis_client) 
            logger.info("Worker iteration finished for city=%s", city)
        except Exception as e: 
            logger.exception("worker iteration failed")
        
        time.sleep(FETCH_INTERVAL_SECONDS)
    
if __name__ == "__main__": 
    main()
