from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_signup_validation():
    response = client.post(
        "/auth/signup",
        json={
            "name": "A",
            "email": "invalid-email",
            "password": "123"
        }
    )

    assert response.status_code == 422


def test_login_with_wrong_password():
    response = client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401