from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_token():
    response = client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "password123"
        }
    )

    return response.json()["access_token"]


def test_booking_without_token():
    response = client.post(
        "/bookings/",
        json={
            "centre_id": 1,
            "test_id": 1,
            "appointment_at": "2026-10-05T10:30:00"
        }
    )

    assert response.status_code == 401


def test_get_my_bookings():
    token = get_token()

    response = client.get(
        "/bookings/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)