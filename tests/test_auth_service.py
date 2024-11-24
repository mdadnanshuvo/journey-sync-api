import pytest
from Auth.auth_service import app
import sys
import os


# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_authorize_valid_token(client):
    valid_token = "generate_a_valid_token_here"  # Replace with a valid JWT
    response = client.post('/authorize', headers={"Authorization": f"Bearer {valid_token}"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Token is valid"
    assert "user_info" in data

def test_authorize_invalid_token(client):
    invalid_token = "invalid.token.value"
    response = client.post('/authorize', headers={"Authorization": f"Bearer {invalid_token}"})
    assert response.status_code == 401
    assert "error" in response.get_json()

def test_role_checker(client):
    valid_token = "generate_a_valid_token_with_role_here"  # Replace with a valid JWT
    response = client.get('/role_checker', headers={"Authorization": f"Bearer {valid_token}"})
    assert response.status_code == 200
    data = response.get_json()
    assert "role" in data
