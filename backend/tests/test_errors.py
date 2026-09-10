from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


def test_validation_uses_error_envelope():
    app = create_app(Settings())
    response = TestClient(app).post("/api/rca", json={})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
    assert response.json()["error"]["request_id"]
    assert "Traceback" not in response.text
