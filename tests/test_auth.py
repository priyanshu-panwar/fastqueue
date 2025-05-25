from fastapi.testclient import TestClient
from app.main import app
from app.settings import settings

client = TestClient(app)

VALID_API_KEY = settings.api_key
INVALID_API_KEY = "invalid-key"


def test_auth_required_missing_token():
    response = client.get("/v1/queues")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or missing API key."


def test_auth_required_invalid_token():
    response = client.get(
        "/v1/queues",
        headers={"Authorization": f"Bearer {INVALID_API_KEY}"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or missing API key."


def test_auth_required_valid_token():
    response = client.get(
        "/v1/queues",
        headers={"Authorization": f"Bearer {VALID_API_KEY}"},
    )
    # The response may vary depending on test DB state
    assert response.status_code == 200 or response.status_code == 204
