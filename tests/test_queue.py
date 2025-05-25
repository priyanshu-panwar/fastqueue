from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app
from app.settings import settings

client = TestClient(app)

API_KEY_HEADER = {"Authorization": f"Bearer {settings.api_key}"}


def test_create_queue():
    response = client.post(
        "/v1/queues",
        headers=API_KEY_HEADER,
        json={
            "name": "test-queue",
            "visibility_timeout_seconds": 30,
            "max_queue_length": 100,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "test-queue"
    assert data["visibility_timeout_seconds"] == 30
    assert data["max_queue_length"] == 100


def test_create_duplicate_queue():
    # Attempt to create the same queue again
    response = client.post(
        "/v1/queues",
        headers=API_KEY_HEADER,
        json={
            "name": "test-queue",
            "visibility_timeout_seconds": 30,
            "max_queue_length": 100,
        },
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "Queue with the given name already exists."


def test_list_queues():
    response = client.get("/v1/queues", headers=API_KEY_HEADER)
    assert response.status_code == 200
    assert isinstance(response.json()["queues"], list)
    assert any(q["name"] == "test-queue" for q in response.json()["queues"])


def test_update_queue():
    response = client.patch(
        "/v1/queues/test-queue",
        headers=API_KEY_HEADER,
        json={"max_queue_length": 500},
    )
    assert response.status_code == 200
    assert response.json()["max_queue_length"] == 500


def test_delete_queue():
    response = client.delete("/v1/queues/test-queue", headers=API_KEY_HEADER)
    assert response.status_code == 204  # No content


def test_delete_nonexistent_queue():
    response = client.delete("/v1/queues/nonexistent", headers=API_KEY_HEADER)
    assert response.status_code == 404
    assert response.json()["detail"] == "Queue not found."
