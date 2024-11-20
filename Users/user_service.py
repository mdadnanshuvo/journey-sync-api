from flask import Flask, jsonify, request
import hashlib
import uuid
import json
import os

app = Flask(__name__)

# Path to store user data in a JSON file
USER_DATA_FILE = './data/users_data.json'

# Function to load users from the JSON file
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

# Function to save users to the JSON file
def save_users(users):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file, indent=4)

# Function to hash passwords securely
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to validate user login
def validate_login(email, password, users):
    for user_id, user in users.items():
        if user['email'] == email and user['password'] == hash_password(password):
            return user_id
    return None

# Register user
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    users = load_users()  # Load users from file

    # Validate input data
    if not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing required fields"}), 400

    role = data.get('role', 'User')  # Default role is 'User', if not specified
    if role not in ['Admin', 'User']:
        return jsonify({"error": "Role must be either 'Admin' or 'User'"}), 400
    
    # Hash password and create user
    user_id = str(uuid.uuid4())  # Generate a unique user ID
    users[user_id] = {
        "name": data['name'],
        "email": data['email'],
        "password": hash_password(data['password']),
        "role": role  # Store the user role
    }
    save_users(users)  # Save the updated users data to file
    return jsonify({"message": "User registered successfully", "user_id": user_id}), 201

# Login user
@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Validate input data
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    users = load_users()  # Load users from file
    # Authenticate user
    user_id = validate_login(email, password, users)
    if user_id:
        user = users[user_id]
        return jsonify({"message": "Login successful", "user_id": user_id, "role": user["role"]}), 200
    return jsonify({"error": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(debug=True)
