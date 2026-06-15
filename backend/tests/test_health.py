from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_healt_endpoint_returns_200():
    response = client.get("/health")
    assert response.status_code == 200

def test_health_endpoint_returns_correct_body():
    response = client.get("/health")
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data

def test_ready_endpoint_returns_valid_status():
    response = client.get("/ready")
    assert response.status_code in [200, 503]

def test_ready_endpoint_returns_valid_body():
    response = client.get("/ready")
    data = response.json()
    assert "status" in data