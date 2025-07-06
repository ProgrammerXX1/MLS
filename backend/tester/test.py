import pytest
import requests

BASE_URL = "http://localhost:8000"

@pytest.fixture
def token():
    resp = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": "tester", "password": "123456"}  # Здесь форма, а не json
    )
    resp.raise_for_status()
    return resp.json()['access_token']


def test_jwt_protected(token):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{BASE_URL}/jwt-protected", headers=headers)
    assert resp.status_code == 200
    assert "username" in resp.json()

def test_api_key_protected():
    api_key = "3eab2b66cca82fce7de6997d4d097817937f8c51ba8f71f11ab02581b9b1e96b"
    headers = {"X-API-Key": api_key}
    resp = requests.get(f"{BASE_URL}/api-key-protected", headers=headers)
    assert resp.status_code == 200
    assert "username" in resp.json()
