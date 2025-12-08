from pydantic import BaseModel

class WeatherData(BaseModel):
    location: str
    temperature: float
    condition: str
    feels_like: float
    wind: str
    temp_unit: str
    wind_unit: str
    time_stamp: str
    is_stale: bool