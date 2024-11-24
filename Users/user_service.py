from flask import Flask, jsonify, request
import bcrypt
import uuid
import jwt
import datetime
from flask_smorest import Api, Blueprint
from flask_swagger_ui import get_swaggerui_blueprint
from functools import wraps
from Users.schemas.user_schema import UserRegisterSchema  # Import the schema
from flask import Flask, jsonify



app = Flask(__name__)

# In-memory user data storage
users = {}

# Secret key for encoding JWT token
app.config['SECRET_KEY'] = 'random_secret_key_for_assignment'  # Change this to a secure key

# Set the API title and OpenAPI version in your app configuration
app.config['API_TITLE'] = 'random_secret_key_for_assignment'
app.config['API_VERSION'] = '1.0.0'
app.config['OPENAPI_VERSION'] = '3.0.2'  # OpenAPI version



# Initialize Flask-Smorest for OpenAPI documentation
api = Api(app)

# Register UserRegisterSchema for OpenAPI
api.spec.components.schema("UserRegisterSchema", schema=UserRegisterSchema)

# Set up Swagger UI at the /swagger path
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "User Registration API"})
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Create Blueprint for User operations
blp = Blueprint('users', 'users', url_prefix='', description="User related operations")

# Function to hash passwords securely using bcrypt
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

# Function to validate user login (check email and password)
def validate_login(email, password):
    for user_id, user in users.items():
        if user['email'] == email and bcrypt.checkpw(password.encode(), user['password'].encode()):
            return user_id
    return None

# Register user with OpenAPI documentation
@blp.route('/register', methods=['POST'])  # Change to '/register' (no '/users' prefix)
@blp.arguments(UserRegisterSchema)  # Use Marshmallow schema
@blp.response(201, {'message': 'User registered successfully', 'user_id': 'string'})
def register_user(request_data):
    name = request_data['name']
    email = request_data['email']
    password = request_data['password']
    role = request_data['role']

    # Validate role
    if role not in ['Admin', 'User']:
        return jsonify({"error": "Role must be either 'Admin' or 'User'"}), 400

    # Check if the email already exists
    if any(user['email'] == email for user in users.values()):
        return jsonify({"error": "Email already exists"}), 400

    # Hash password and create user
    user_id = str(uuid.uuid4())
    users[user_id] = {
        "name": name,
        "email": email,
        "password": hash_password(password),
        "role": role
    }

    return jsonify({"message": "User registered successfully", "user_id": user_id}), 201

# Get all users with OpenAPI documentation
@blp.route('/users', methods=['GET'])  # Endpoint to get users
@blp.response(200, {
    'type': 'object',
    'additionalProperties': {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'email': {'type': 'string'},
            'role': {'type': 'string'}
        }
    }
})
def get_users():
    # Exclude password when returning user details
    sanitized_users = {
        user_id: {key: value for key, value in user.items() if key != 'password'}
        for user_id, user in users.items()
    }
    return jsonify(sanitized_users)

# POST /login: Authenticate a user and provide an access token
@blp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validate user credentials
    user_id = validate_login(email, password)
    if not user_id:
        return jsonify({"error": "Invalid email or password"}), 401

    # Create JWT token with user name, email, and role
    user = users[user_id]
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # 1 hour expiration
    token = jwt.encode({
        'user_id': user_id,
        'name': user['name'],  # Include name in the JWT
        'role': user['role'],  # Include role in the JWT
        'exp': expiration_time
    }, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'message': 'Login successful', 'access_token': token}), 200


# Token required decorator to validate JWT
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        # Check if the token is provided in the Authorization header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Extract token from "Bearer <token>"

        if not token:
            return jsonify({"error": "Token is missing!"}), 403

        try:
            # Decode the JWT token
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = decoded_token['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401

        # Pass current_user_id to the route function
        return f(current_user_id, *args, **kwargs)

    return decorator

# Profile endpoint to get the current user's profile
@blp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user_id):
    # Fetch the user data from the in-memory storage
    user = users.get(current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Return user profile excluding password
    user_profile = {key: value for key, value in user.items() if key != 'password'}
    return jsonify(user_profile)

# Register Blueprint to the API
api.register_blueprint(blp)

# Create Swagger Documentation (swagger.json)
@app.route('/static/swagger.json')
def create_swagger():
    return jsonify({
        "openapi": "3.0.0",
        "info": {
            "title": "User Registration API",
            "version": "1.0.0",
            "description": "An API for registering and managing users"
        },
        "paths": {
            "/register": {
                "post": {
                    "summary": "Register a new user",
                    "operationId": "registerUser",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/UserRegisterSchema"
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "User registered successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "message": {"type": "string"},
                                            "user_id": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/login": {
                "post": {
                    "summary": "Authenticate a user and provide an access token",
                    "operationId": "loginUser",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "email": {"type": "string", "format": "email"},
                                        "password": {"type": "string"}
                                    },
                                    "required": ["email", "password"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Login successful",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "message": {"type": "string"},
                                            "access_token": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/profile": {
                "get": {
                    "summary": "Get current user's profile",
                    "operationId": "getProfile",
                    "security": [
                        {
                            "bearerAuth": []
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "User profile data",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string"},
                                            "email": {"type": "string"},
                                            "role": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "UserRegisterSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "email": {"type": "string", "format": "email"},
                        "password": {"type": "string"},
                        "role": {"type": "string", "enum": ["Admin", "User"], "default": "User"}
                    },
                    "required": ["name", "email", "password"]
                }
            },
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        }
    })



def home():
    return "User Service is running!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)