from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_generate_ok():
    r = client.post(
        "/generate",
        json={"brand": "Nike", "event": "Launch", "context": "Hello"},
    )
    assert r.status_code == 200
    body = r.json()
    assert "summary" in body
    assert "risks" in body and isinstance(body["risks"], list)
    assert "recommendation" in body


def test_generate_validation_error():
    r = client.post(
        "/generate",
        json={"brand": "Nike", "event": "Launch"},
    )  # missing context
    assert r.status_code == 400
    body = r.json()
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert "request_id" in body["error"]
