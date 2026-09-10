from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


def test_health_works_without_external_configuration():
    app = create_app(Settings(google_api_key=None, github_token=None, github_repo=None))
    response = TestClient(app).get("/api/health")
    assert response.status_code == 200
    assert response.json()["issues_configured"] is False
    assert response.headers["x-request-id"]
