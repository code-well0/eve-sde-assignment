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


def test_payment_without_token():
    response = client.post(
        "/payments/",
        json={
            "booking_id": 1
        }
    )

    assert response.status_code == 401


def test_webhook_wrong_amount():
    response = client.post(
        "/payments/webhook/",
        json={
            "event_id": "pytest-wrong-amount",
            "booking_id": 1,
            "status": "SUCCESS",
            "amount": 100
        }
    )

    assert response.status_code == 400


def test_webhook_invalid_status():
    response = client.post(
        "/payments/webhook/",
        json={
            "event_id": "pytest-invalid-status",
            "booking_id": 1,
            "status": "PENDING",
            "amount": 500
        }
    )

    assert response.status_code == 400