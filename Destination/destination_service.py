import bcrypt
from flask import Flask, jsonify, request, send_from_directory
from flask_smorest import Api, Blueprint
from flask_swagger_ui import get_swaggerui_blueprint
import uuid
import jwt
import datetime
import os
from functools import wraps
from schemas.destination_schema import DestinationSchema

app = Flask(__name__)

# In-memory destination data storage
destinations = {}

# Secret key for encoding JWT token
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure key

# Set the API title and OpenAPI version in your app configuration
app.config['API_TITLE'] = 'Destination Service API'
app.config['API_VERSION'] = '1.0.0'
app.config['OPENAPI_VERSION'] = '3.0.2'  # OpenAPI version

# Initialize Flask-Smorest for OpenAPI documentation
api = Api(app)

# Register DestinationSchema for OpenAPI
api.spec.components.schema("DestinationSchema", schema=DestinationSchema)

# Set up Swagger UI at the /swagger path
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'  # Swagger JSON file path
swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Destination Service API"})
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Create Blueprint for Destination operations
blp = Blueprint('destinations', 'destinations', url_prefix='/destinations', description="Destination related operations")

# Function to hash passwords securely using bcrypt (for user service, here for consistency)
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

# Token required decorator to validate JWT
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({"error": "Token is missing!"}), 403

        try:
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = decoded_token['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401

        return f(current_user_id, *args, **kwargs)
    return decorator

# Route: Get all destinations
@blp.route("/", methods=["GET"])
@blp.response(200, {'type': 'array', 'items': {'$ref': '#/components/schemas/DestinationSchema'}})
def get_destinations():
    return jsonify(list(destinations.values())), 200

# Route: Add a new destination (Admin-only)
@blp.route("/", methods=["POST"])
@blp.arguments(DestinationSchema)
@blp.response(201, {'message': 'Destination added successfully', 'id': 'string'})
@token_required
def add_destination(current_user_id, request_data):
    """Add a new destination (Admin-only)"""
    # Assuming only Admin can add destinations (role check)
    if current_user_id != "Admin":  # Example check
        return jsonify({"error": "Access Denied"}), 403

    destination_id = str(uuid.uuid4())
    destinations[destination_id] = {**request_data, "id": destination_id}

    return jsonify({"message": "Destination added successfully", "id": destination_id}), 201

# Route: Delete a destination (Admin-only)
@blp.route("/<destination_id>", methods=["DELETE"])
@blp.response(200, {'message': 'Destination deleted successfully'})
@token_required
def delete_destination(current_user_id, destination_id):
    """Delete a destination (Admin-only)"""
    if current_user_id != "Admin":  # Example check
        return jsonify({"error": "Access Denied"}), 403

    if destination_id not in destinations:
        return jsonify({"error": "Destination not found"}), 404

    del destinations[destination_id]
    return jsonify({"message": "Destination deleted successfully."}), 200

# Route: Update a destination (Admin-only)
@blp.route("/<destination_id>", methods=["PUT"])
@blp.arguments(DestinationSchema)
@blp.response(200, {'message': 'Destination updated successfully', 'destination': {'$ref': '#/components/schemas/DestinationSchema'}})
@token_required
def update_destination(current_user_id, destination_id, request_data):
    """Update a destination (Admin-only)"""
    if current_user_id != "Admin":  # Example check
        return jsonify({"error": "Access Denied"}), 403

    if destination_id not in destinations:
        return jsonify({"error": "Destination not found"}), 404

    destinations[destination_id].update(request_data)
    return jsonify({"message": "Destination updated successfully.", "destination": destinations[destination_id]}), 200

# Create Swagger Documentation (swagger.json)
@app.route('/static/swagger.json')
def create_swagger():
    return jsonify({
        "openapi": "3.0.0",
        "info": {
            "title": "Destination Service API",
            "version": "1.0.0",
            "description": "An API for managing destinations in a travel app"
        },
        "paths": {
            "/destinations": {
                "get": {
                    "summary": "Get all destinations",
                    "operationId": "getDestinations",
                    "responses": {
                        "200": {
                            "description": "A list of destinations",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/DestinationSchema"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "summary": "Add a new destination",
                    "operationId": "addDestination",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/DestinationSchema"
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "Destination added successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "message": {"type": "string"},
                                            "id": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/destinations/{destination_id}": {
                "delete": {
                    "summary": "Delete a destination",
                    "operationId": "deleteDestination",
                    "responses": {
                        "200": {
                            "description": "Destination deleted successfully"
                        }
                    }
                },
                "put": {
                    "summary": "Update a destination",
                    "operationId": "updateDestination",
                    "responses": {
                        "200": {
                            "description": "Destination updated successfully"
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "DestinationSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                        "location": {"type": "string"}
                    },
                    "required": ["name", "description", "location"]
                }
            }
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
