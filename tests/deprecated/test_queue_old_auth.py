import random
from fastapi.testclient import TestClient
from unittest.mock import patch

import pytest

from app.main import app
from app.settings import settings

client = TestClient(app)

API_KEY_HEADER = {"Authorization": f"Bearer {settings.api_key}"}
random_name = random.randint(10000, 99999)


@pytest.mark.skip(reason="Deprecated - uses old API key auth")
def test_create_queue():
    response = client.post(
        "/v1/queues",
        headers=API_KEY_HEADER,
        json={
            "name": f"test-queue-{random_name}",
            "visibility_timeout_seconds": 30,
            "max_queue_length": 100,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == f"test-queue-{random_name}"
    assert data["visibility_timeout_seconds"] == 30
    assert data["max_queue_length"] == 100


@pytest.mark.skip(reason="Deprecated - uses old API key auth")
def test_create_duplicate_queue():
    # Attempt to create the same queue again
    response = client.post(
        "/v1/queues",
        headers=API_KEY_HEADER,
        json={
            "name": f"test-queue-{random_name}",
            "visibility_timeout_seconds": 30,
            "max_queue_length": 100,
        },
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "Queue with the given name already exists."


@pytest.mark.skip(reason="Deprecated - uses old API key auth")
def test_list_queues():
    response = client.get("/v1/queues", headers=API_KEY_HEADER)
    assert response.status_code == 200
    assert isinstance(response.json()["queues"], list)
    assert any(
        q["name"] == f"test-queue-{random_name}" for q in response.json()["queues"]
    )


@pytest.mark.skip(reason="Deprecated - uses old API key auth")
def test_update_queue():
    response = client.patch(
        f"/v1/queues/test-queue-{random_name}",
        headers=API_KEY_HEADER,
        json={"max_queue_length": 500},
    )
    assert response.status_code == 200
    assert response.json()["max_queue_length"] == 500


@pytest.mark.skip(reason="Deprecated - uses old API key auth")
def test_delete_queue():
    response = client.delete(
        f"/v1/queues/test-queue-{random_name}", headers=API_KEY_HEADER
    )
    assert response.status_code == 204  # No content


@pytest.mark.skip(reason="Deprecated - uses old API key auth")
def test_delete_nonexistent_queue():
    response = client.delete("/v1/queues/nonexistent", headers=API_KEY_HEADER)
    assert response.status_code == 404
    assert response.json()["detail"] == "Queue not found."
