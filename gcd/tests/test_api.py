from fastapi.testclient import TestClient

from gcd.api.app import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.json()["status"] == "ok"


def test_metrics():
    resp = client.get("/metrics")
    assert "requests" in resp.json()
