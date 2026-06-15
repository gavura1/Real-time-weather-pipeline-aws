import time
from fastapi.testclient import TestClient
from app.main import app
from app.api import routes_weather

client = TestClient(app)


class FakeWeather:
    def __init__(self, stored_at: int):
        self.stored_at = stored_at
        self.is_stale = False


def test_weather_status_returns_200_when_data_exists(monkeypatch):
    def fake_get_current_weather(city, redis_client):
        return FakeWeather(stored_at=int(time.time()))

    def fake_get_last_good_weather(city, redis_client):
        return None

    monkeypatch.setattr(routes_weather, "get_current_weather", fake_get_current_weather)
    monkeypatch.setattr(routes_weather, "get_last_good_weather", fake_get_last_good_weather)

    response = client.get("/weather/status?city=Test")
    assert response.status_code == 200


def test_weather_status_returns_correct_fields(monkeypatch):
    def fake_get_current_weather(city, redis_client):
        return FakeWeather(stored_at=int(time.time()))

    def fake_get_last_good_weather(city, redis_client):
        return None

    monkeypatch.setattr(routes_weather, "get_current_weather", fake_get_current_weather)
    monkeypatch.setattr(routes_weather, "get_last_good_weather", fake_get_last_good_weather)

    response = client.get("/weather/status?city=Test")
    data = response.json()
    assert "city" in data
    assert "source" in data
    assert "redis" in data
    assert "current_exists" in data
    assert "last_good_exists" in data


def test_weather_status_returns_503_when_no_data(monkeypatch):
    def fake_get_current_weather(city, redis_client):
        return None

    def fake_get_last_good_weather(city, redis_client):
        return None

    monkeypatch.setattr(routes_weather, "get_current_weather", fake_get_current_weather)
    monkeypatch.setattr(routes_weather, "get_last_good_weather", fake_get_last_good_weather)

    response = client.get("/weather/status?city=Test")
    data = response.json()
    assert data["source"] == "none"
    assert data["current_exists"] is False
    assert data["last_good_exists"] is False