from clients.redis_client import RedisClient 
from jobs.weather_job import run_weather_job 
from core.config import FETCH_INTERVAL_SECONDS, REDIS_HOST, REDIS_PORT, REDIS_DB
import time 

def main(): 
    redis_client = RedisClient(REDIS_HOST, REDIS_PORT, REDIS_DB)
    
    while True: 
        try: 
            city = "Banska Bystrica" 
            run_weather_job(city, redis_client) 
        except Exception as e: 
            print(e) 
        
        time.sleep(FETCH_INTERVAL_SECONDS)
    
if __name__ == "__main__": 
    main()
