from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_scenarios_endpoint():
    response = client.get("/api/scenarios")
    assert response.status_code == 200
    assert "scenarios" in response.json()


def test_evaluate_nominal_endpoint():
    response = client.get("/api/evaluate/nominal")
    assert response.status_code == 200
    payload = response.json()
    assert payload["scenario"] == "nominal"


def test_playback_endpoint():
    response = client.post("/api/playback")
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["sequence"]) == 5
