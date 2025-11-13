# tests/test_endpoints.py
import pytest

def test_get_foods_with_valid_token(client, mock_token_verification):
    headers = {"Authorization": "Bearer fake_token"}
    response = client.get("/Foods/", headers=headers)
    assert response.status_code == 200
    assert "message" not in response.json()
def test_register_user_requires_token(client):
    data = {
        "name": "Test User",
        "surname": "Example",
        "weight": 70,
        "height": 175,
        "birthDate": "1990-01-01",
        "goals": [],
        "validation": "",
        "achievements": []
    }
    response = client.post("/RegisterUser/test_user", json=data)
    assert response.status_code == 401

def test_register_user_with_token(client, mock_token_verification):
    headers = {"Authorization": "Bearer fake_token"}
    data = {
        "name": "Test User",
        "surname": "Example",
        "weight": 70,
        "height": 175,
        "birthDate": "1990-01-01",
        "goals": [],
        "validation": "",
        "achievements": []
    }
    response = client.post("/RegisterUser/test_user", headers=headers, json=data)
    assert response.status_code in [200, 201]
