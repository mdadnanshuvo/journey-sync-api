import pytest
from Users.user_service import app,users

import sys
import os





# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_register_user(client):
    response = client.post('/register', json={
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "role": "User"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "User registered successfully"
    assert "user_id" in data

def test_register_user_duplicate_email(client):
    client.post('/register', json={
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "role": "User"
    })
    response = client.post('/register', json={
        "name": "Jane Doe",
        "email": "john.doe@example.com",
        "password": "password456",
        "role": "User"
    })
    assert response.status_code == 400
    assert response.get_json()["error"] == "Email already exists"

def test_login_user(client):
    client.post('/register', json={
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "role": "User"
    })
    response = client.post('/login', json={
        "email": "john.doe@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data

def test_login_user_invalid_credentials(client):
    response = client.post('/login', json={
        "email": "invalid@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid email or password"

def test_get_users(client):
    response = client.get('/users')
    assert response.status_code == 200
