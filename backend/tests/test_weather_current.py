import time

from fastapi.testclient import TestClient

from app.main import app
from app.api import routes_weather

client = TestClient(app)


class FakeWeather:
    def __init__(self, stored_at: int):
        self.stored_at = stored_at
        self.is_stale = False


def test_weather_current_returns_200_when_current_exists(monkeypatch):
    def fake_get_current_weather(city, redis_client):
        return FakeWeather(stored_at=int(time.time()))

    def fake_get_last_good_weather(city, redis_client):
        return None

    monkeypatch.setattr(routes_weather, "get_current_weather", fake_get_current_weather)
    monkeypatch.setattr(routes_weather, "get_last_good_weather", fake_get_last_good_weather)

    response = client.get("/weather/current?city=Test")
    assert response.status_code == 200


def test_weather_current_returns_503_when_no_data_available(monkeypatch):
    def fake_get_current_weather(city, redis_client):
        return None

    def fake_get_last_good_weather(city, redis_client):
        return None

    monkeypatch.setattr(routes_weather, "get_current_weather", fake_get_current_weather)
    monkeypatch.setattr(routes_weather, "get_last_good_weather", fake_get_last_good_weather)

    response = client.get("/weather/current?city=Test")
    assert response.status_code == 503
