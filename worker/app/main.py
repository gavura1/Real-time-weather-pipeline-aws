from clients.redis_client import RedisClient
from jobs.weather_job import run_weather_job
import time

def main():
    redis_client = RedisClient("localhost", 6379, 0)

    city = "Banska Bystrica"
    run_weather_job(city, redis_client)
    print("done")

if __name__ == "__main__":
    main()
