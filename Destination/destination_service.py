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

# Authentication Service URL
AUTH_SERVICE_URL = "http://127.0.0.1:5002"

# Flask-Smorest API configuration
app.config['API_TITLE'] = 'Destination Service API'
app.config['API_VERSION'] = '1.0.0'
app.config['OPENAPI_VERSION'] = '3.0.3'
app.config['OPENAPI_URL_PREFIX'] = '/openapi.json'  # Ensure OpenAPI spec is available at `/openapi.json`

# Initialize Flask-Smorest API
api = Api(app)

# Blueprint for destination endpoints
blp = Blueprint("destinations", "destinations", url_prefix="/destinations", description="Destination management APIs")

# Swagger UI setup
SWAGGER_URL = '/swagger'
API_URL = '/openapi.json'  # This should match the OpenAPI URL prefix
swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Destination Service API"})
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Helper function to check admin role via Authentication Service
def is_admin(token):
    if not token:
        return False
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = request.post(f"{AUTH_SERVICE_URL}/check-role", json={"role": "Admin"}, headers=headers)
        return response.status_code == 200
    except request.exceptions.RequestException as e:
        # Log the error and return False
        print(f"Error connecting to Authentication Service: {e}")
        return False

# Route: Get all destinations
@blp.route("/", methods=["GET"])
@blp.response(200, {"destinations": "List of destinations"})
def get_destinations():
    """
    Get all destinations.
    """
    return jsonify(list(destinations.values())), 200

# Route: Add a new destination (Admin-only)
@blp.route("/", methods=["POST"])
@blp.arguments(DestinationSchema)  # Validate input with DestinationSchema
@blp.response(201, {"message": "Destination added successfully", "id": "string"})
@blp.response(403, {"error": "Access denied"})
@blp.response(400, {"error": "Invalid data"})
def add_destination(request_data):
    """
    Add a new destination (Admin-only).
    """
    token = request.headers.get('Authorization', '').split(" ")[1] if 'Authorization' in request.headers else None
    if not token or not is_admin(token):
        return jsonify({"error": "Access denied"}), 403

    destination_id = str(uuid.uuid4())
    destinations[destination_id] = {**request_data, "id": destination_id}
    return jsonify({"message": "Destination added successfully", "id": destination_id}), 201

# Route: Delete a destination (Admin-only)
@blp.route("/<destination_id>", methods=["DELETE"])
@blp.response(200, {"message": "Destination deleted successfully"})
@blp.response(403, {"error": "Access denied"})
@blp.response(404, {"error": "Destination not found"})
def delete_destination(destination_id):
    """
    Delete a destination (Admin-only).
    """
    token = request.headers.get('Authorization', '').split(" ")[1] if 'Authorization' in request.headers else None
    if not token or not is_admin(token):
        return jsonify({"error": "Access denied"}), 403

    if destination_id not in destinations:
        return jsonify({"error": "Destination not found"}), 404

    del destinations[destination_id]
    return jsonify({"message": "Destination deleted successfully"}), 200

# Register Blueprint
api.register_blueprint(blp)

# Enable OpenAPI specification to be served at `/openapi.json`
@app.route('/openapi.json')
def openapi_spec():
    return jsonify(api.spec.to_dict())

if __name__ == '__main__':
    app.run(debug=True, port=5001)