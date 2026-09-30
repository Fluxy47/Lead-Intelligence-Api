from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

VALID_LEAD = {
    "name": "Ali",
    "email": "ali@example.com",
    "message": "Interested in your services",
}


def test_valid_lead_returns_201():
    response = client.post("/lead", json=VALID_LEAD)
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Ali"
    assert "lead_id" in body
    assert "received_at" in body


def test_invalid_email_returns_422():
    payload = {**VALID_LEAD, "email": "not-an-email"}
    response = client.post("/lead", json=payload)
    assert response.status_code == 422
    body = response.json()
    assert body["error_code"] == "VALIDATION_ERROR"
    fields = [d["field"] for d in body["details"]]
    assert "email" in fields


def test_missing_name_returns_422():
    payload = {k: v for k, v in VALID_LEAD.items() if k != "name"}
    response = client.post("/lead", json=payload)
    assert response.status_code == 422
    fields = [d["field"] for d in response.json()["details"]]
    assert "name" in fields


def test_disposable_email_returns_400():
    payload = {**VALID_LEAD, "email": "test@mailinator.com"}
    response = client.post("/lead", json=payload)
    assert response.status_code == 400
    assert response.json()["error_code"] == "DISPOSABLE_EMAIL"


def test_low_effort_message_returns_400():
    payload = {**VALID_LEAD, "message": "aaaaaaaaaa"}
    response = client.post("/lead", json=payload)
    assert response.status_code == 400
    assert response.json()["error_code"] == "LOW_EFFORT_MESSAGE"

def test_multiple_field_errors_returns_both():
    payload = {**VALID_LEAD, "name": "A", "message": "hi"}
    response = client.post("/lead", json=payload)
    assert response.status_code == 422
    fields = [d["field"] for d in response.json()["details"]]
    assert len(fields) == 2