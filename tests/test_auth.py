import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from app.main import app
from app.settings import settings
from app.database import get_db
from app.auth2.models import User

client = TestClient(app)

# Set debug to True to bypass token validation in tests if needed
settings.debug = True


@pytest.fixture(autouse=True)
def clear_users():
    db: Session = next(get_db())
    db.query(User).delete()
    db.commit()


@pytest.fixture
def test_user():
    username = "testuser"
    password = "testpass123"
    client.post("/v1/auth/register", json={"username": username, "password": password})
    return {"username": username, "password": password}


def test_register_user():
    response = client.post(
        "/v1/auth/register", json={"username": "newuser", "password": "newpass123"}
    )
    print(response)
    print(response.json())
    assert response.status_code == 200
    assert response.json()["username"] == "newuser"


def test_login_success(test_user):
    response = client.post("/v1/auth/login", json=test_user)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_failure():
    response = client.post(
        "/v1/auth/login", json={"username": "fakeuser", "password": "wrongpass"}
    )
    assert response.status_code == 401


def test_refresh_token(test_user):
    login_response = client.post("/v1/auth/login", json=test_user)
    refresh_token = login_response.json()["refresh_token"]

    response = client.post("/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_change_password(test_user):
    response = client.post(
        "/v1/auth/change-password",
        json={
            "username": test_user["username"],
            "old_password": test_user["password"],
            "new_password": "newpassword123",
        },
    )
    assert response.status_code == 200
    assert response.json()["username"] == test_user["username"]

    # Login with new password should work
    response = client.post(
        "/v1/auth/login",
        json={"username": test_user["username"], "password": "newpassword123"},
    )
    assert response.status_code == 200


def test_delete_user():
    username = "tobedeleted"
    password = "deletepass"
    client.post("/v1/auth/register", json={"username": username, "password": password})

    response = client.post(
        "/v1/auth/delete", json={"username": username, "password": password}
    )
    assert response.status_code == 200

    # Try login after delete
    login_response = client.post(
        "/v1/auth/login", json={"username": username, "password": password}
    )
    assert login_response.status_code == 401
