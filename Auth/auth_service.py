from flask import Flask, jsonify, request
import jwt
from functools import wraps
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Secret key for encoding JWT tokens (same as in user_service.py)
app.config['SECRET_KEY'] = 'random_secret_key_for_assignment'

# Swagger UI Setup
SWAGGER_URL = '/swagger'  # Swagger UI will be accessible at this route
API_URL = '/swagger.json'  # The Swagger spec will be available here

# Setup Swagger UI Blueprint
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI will be accessible at '/swagger'
    API_URL,  # Swagger specification URL
    config={
        'app_name': "Auth Service API"
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Function to decode and validate the JWT token
def decode_token(token):
    try:
        # Decode the token using the same secret key
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return decoded_token  # Returns decoded token with user info (user_id, name, role)
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")

# Decorator to require JWT token
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')  # Expecting "Bearer <token>"

        if not token:
            return jsonify({"error": "Token is missing!"}), 403

        token = token.split(" ")[1]  # Remove 'Bearer' from the header value

        try:
            # Decode the JWT token
            decoded_token = decode_token(token)
            current_user_id = decoded_token['user_id']
        except Exception as e:
            return jsonify({"error": str(e)}), 401

        # Pass the user information to the route function
        return f(current_user_id, *args, **kwargs)

    return decorator

# POST /authorize: Check if the token is valid and return user info
@app.route('/authorize', methods=['POST'])
@token_required
def authorize(current_user_id):
    try:
        # Retrieve the token from the Authorization header
        token = request.headers.get('Authorization')
        token = token.split(" ")[1]  # Extract the token

        # Decode the token to get user information
        decoded_token = decode_token(token)
        user_info = {
            "user_id": decoded_token['user_id'],
            "name": decoded_token['name'],
            "role": decoded_token['role']
        }
        return jsonify({"message": "Token is valid", "user_info": user_info}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

# GET /role_checker: Check user role (User or Admin)
@app.route('/role_checker', methods=['GET'])
@token_required
def role_checker(current_user_id):
    try:
        # Retrieve the token from the Authorization header
        token = request.headers.get('Authorization')
        token = token.split(" ")[1]  # Extract the token

        # Decode the token to extract the role
        decoded_token = decode_token(token)
        role = decoded_token.get('role', None)
        
        if role is None:
            return jsonify({"error": "Role not found in token"}), 400
        
        return jsonify({"message": "Role found", "role": role}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 401

# Swagger Spec
@app.route('/swagger.json')
def swagger_spec():
    return jsonify({
        "openapi": "3.0.0",
        "info": {
            "title": "Auth Service API",
            "version": "1.0.0",
            "description": "API for JWT Authentication and Role Checking"
        },
        "paths": {
            "/authorize": {
                "post": {
                    "summary": "Check if the token is valid and return user info",
                    "operationId": "authorize",
                    "security": [
                        {
                            "bearerAuth": []
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Token is valid",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "message": { "type": "string" },
                                            "user_info": {
                                                "type": "object",
                                                "properties": {
                                                    "user_id": { "type": "string" },
                                                    "name": { "type": "string" },
                                                    "role": { "type": "string" }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "401": {
                            "description": "Invalid or expired token"
                        }
                    }
                }
            },
            "/role_checker": {
                "get": {
                    "summary": "Check user role",
                    "operationId": "roleChecker",
                    "security": [
                        {
                            "bearerAuth": []
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Role found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "message": { "type": "string" },
                                            "role": { "type": "string" }
                                        }
                                    }
                                }
                            }
                        },
                        "401": {
                            "description": "Invalid or expired token"
                        }
                    }
                }
            }
        },
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Running on a different port for the auth_service
