import pytest
from Destination.destination_service import app, destinations
import sys
import os

# Add the project root to the Python path

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# Helper function to generate a valid token
def generate_valid_token():
    # In practice, you'd generate or fetch a valid token here
    return "valid_jwt_token_here"  # Replace with your actual JWT

# Helper function to generate a valid admin token
def generate_valid_admin_token():
    # In practice, you'd generate or fetch a valid admin token here
    return "valid_admin_jwt_token_here"  # Replace with your actual Admin JWT

def test_get_destinations(client):
    valid_token = generate_valid_token()  # Replace with a valid JWT
    response = client.get('/destinations/', headers={"Authorization": f"Bearer {valid_token}"})
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_add_destination(client):
    valid_token = generate_valid_admin_token()  # Replace with a valid Admin JWT
    response = client.post('/destinations/', headers={"Authorization": f"Bearer {valid_token}"}, json={
        "name": "Paris",
        "description": "City of Light",
        "location": "France"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Destination added"
    assert "id" in data
    return data["id"]  # Return the destination ID for later use

def test_delete_destination(client):
    valid_token = generate_valid_admin_token()  # Replace with a valid Admin JWT
    
    # Add a destination first
    destination_id = test_add_destination(client)  # Create a destination and get the ID
    
    # Delete the destination using the ID returned by the add test
    response = client.delete(f'/destinations/{destination_id}', headers={"Authorization": f"Bearer {valid_token}"})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Destination deleted successfully"
