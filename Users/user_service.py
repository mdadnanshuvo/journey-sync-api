from flask import Flask, jsonify, request
import bcrypt
import uuid
from flask_smorest import Api, Blueprint
from flask_swagger_ui import get_swaggerui_blueprint
from Users.schemas.user_schema import UserRegisterSchema  # Import the schema

app = Flask(__name__)

# In-memory user data storage
users = {}

# Set the API title and OpenAPI version in your app configuration
app.config['API_TITLE'] = 'User Registration API'
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

# Function to validate user login
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
            "/register": {  # Change the path here to /register
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
                        },
                        "400": {
                            "description": "Bad Request",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "error": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/users": {
                "get": {
                    "summary": "Get all users",
                    "operationId": "getUsers",
                    "responses": {
                        "200": {
                            "description": "List of all users",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "additionalProperties": {
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
            }
        }
    })


if __name__ == '__main__':
    app.run(debug=True)
