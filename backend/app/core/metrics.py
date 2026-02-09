from prometheus_client import Counter, Histogram

# How many times the endpoint is called
HTTP_REQUEST_TOTAL = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["endpoint"]
)

# Where the weather data came from (cache hit/miss)
WEATHER_CACHE_SOURCE_TOTAL = Counter(
    "weather_cache_source_total",
    "Weather response source",
    ["source"] # current, last_good, none
)

# Request latency in seconds
HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["endpoint"]
)



