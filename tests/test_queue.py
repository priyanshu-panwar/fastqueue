import random
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.settings import settings

settings.debug = True

client = TestClient(app)
random_name = random.randint(10000, 99999)


@pytest.fixture
def auth_header():
    return {"Authorization": f"Bearer random-token"}


def test_create_queue(auth_header):
    response = client.post(
        "/v1/queues",
        headers=auth_header,
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


def test_create_duplicate_queue(auth_header):
    response = client.post(
        "/v1/queues",
        headers=auth_header,
        json={
            "name": f"test-queue-{random_name}",
            "visibility_timeout_seconds": 30,
            "max_queue_length": 100,
        },
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "Queue with the given name already exists."


def test_list_queues(auth_header):
    response = client.get("/v1/queues", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json()["queues"], list)
    assert any(
        q["name"] == f"test-queue-{random_name}" for q in response.json()["queues"]
    )


def test_update_queue(auth_header):
    response = client.patch(
        f"/v1/queues/test-queue-{random_name}",
        headers=auth_header,
        json={"max_queue_length": 500},
    )
    assert response.status_code == 200
    assert response.json()["max_queue_length"] == 500


def test_delete_queue(auth_header):
    response = client.delete(
        f"/v1/queues/test-queue-{random_name}", headers=auth_header
    )
    assert response.status_code == 204


def test_delete_nonexistent_queue(auth_header):
    response = client.delete("/v1/queues/nonexistent", headers=auth_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Queue not found."
