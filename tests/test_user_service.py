import pytest
import uuid
import json
from ..app import app, users  # Import the Flask app and users storage

# Set up the test client for Flask
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test User Registration
def test_register_user(client):
    user_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "role": "User"
    }
    
    response = client.post('/register', json=user_data)
    
    # Check if user is registered successfully
    assert response.status_code == 201
    assert b'User registered successfully' in response.data

def test_register_user_email_exists(client):
    # First, register a user
    user_data = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "password": "password123",
        "role": "User"
    }
    client.post('/register', json=user_data)
    
    # Try to register with the same email
    duplicate_user_data = {
        "name": "Jane Duplicate",
        "email": "jane.doe@example.com",
        "password": "password456",
        "role": "User"
    }
    response = client.post('/register', json=duplicate_user_data)
    
    # Check if the email exists error is returned
    assert response.status_code == 400
    assert b'Email already exists' in response.data

# Test User Login
def test_login_user(client):
    # First, register a user
    user_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "role": "User"
    }
    client.post('/register', json=user_data)

    # Now, login with the correct credentials
    login_data = {
        "email": "john.doe@example.com",
        "password": "password123"
    }
    response = client.post('/login', json=login_data)
    
    # Check if login is successful and access token is returned
    assert response.status_code == 200
    assert b'Login successful' in response.data
    assert b'access_token' in response.data

def test_login_user_invalid_credentials(client):
    # Try to login with invalid credentials
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    response = client.post('/login', json=login_data)
    
    # Check if the invalid credentials error is returned
    assert response.status_code == 401
    assert b'Invalid email or password' in response.data

# Test Profile Access with JWT
def test_get_profile(client):
    # First, register and login to get a token
    user_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "role": "User"
    }
    client.post('/register', json=user_data)

    login_data = {
        "email": "john.doe@example.com",
        "password": "password123"
    }
    login_response = client.post('/login', json=login_data)
    token = login_response.get_json()['access_token']

    # Now, access the profile using the token
    response = client.get('/profile', headers={'Authorization': f'Bearer {token}'})
    
    # Check if profile data is returned (without password)
    assert response.status_code == 200
    assert b'name' in response.data
    assert b'email' in response.data
    assert b'role' in response.data
    assert b'password' not in response.data  # Ensure password is excluded

def test_get_profile_no_token(client):
    # Try to access the profile without a token
    response = client.get('/profile')
    
    # Check if error message for missing token is returned
    assert response.status_code == 403
    assert b'Token is missing' in response.data

def test_get_profile_invalid_token(client):
    # Try to access the profile with an invalid token
    response = client.get('/profile', headers={'Authorization': 'Bearer invalid_token'})
    
    # Check if error message for invalid token is returned
    assert response.status_code == 401
    assert b'Invalid token' in response.data

# Test Swagger UI
def test_swagger_ui(client):
    # Check if the Swagger UI page loads successfully
    response = client.get('/swagger')
    assert response.status_code == 200
    assert b'Swagger UI' in response.data
