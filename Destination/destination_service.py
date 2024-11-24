from flask import Flask, jsonify, request
from flask_smorest import Api, Blueprint
from flask_swagger_ui import get_swaggerui_blueprint
import jwt
import uuid
from functools import wraps
from Destination.schemas.destination_schema import DestinationSchema  # Adjust path if needed





# Flask app setup
app = Flask(__name__)
app.config['API_TITLE'] = 'Destination Service API'
app.config['API_VERSION'] = '1.0.0'
app.config['OPENAPI_VERSION'] = '3.0.3'
app.config['OPENAPI_JSON_PATH'] = 'openapi.json'
app.config['OPENAPI_URL_PREFIX'] = '/api'
app.config['API_SPEC_OPTIONS'] = {
    "components": {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Enter 'Bearer <JWT>' to authorize."
            }
        }
    },
    "security": [{"bearerAuth": []}]
}

# Initialize Flask-Smorest API
api = Api(app)

# Swagger UI setup
SWAGGER_URL = '/swagger'
swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, '/api/openapi.json')
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Secret Key
SECRET_KEY = 'random_secret_key_for_assignment'

# In-memory destination data storage
destinations = {}

# Helper function for JWT authentication
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header must be in format 'Bearer <JWT>'"}), 401

        token = auth_header.split("Bearer ")[-1]
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user = decoded  # Attach user info to request
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 403
        return func(*args, **kwargs)
    return decorated

# Blueprint for destination APIs
blp = Blueprint("destinations", __name__, description="APIs for managing destinations", url_prefix="/destinations")

@blp.route("/", methods=["GET"])
@token_required
@blp.response(200, description="List of all destinations")
def get_destinations():
    """Fetch all destinations."""
    return jsonify(list(destinations.values()))

@blp.route("/", methods=["POST"])
@blp.arguments(DestinationSchema)
@token_required
@blp.response(201, description="Destination added successfully")
def add_destination(data):
    """Add a new destination (Admin-only)."""
    if request.user.get("role") != "Admin":
        return jsonify({"error": "Admin privileges required"}), 403
    destination_id = str(uuid.uuid4())
    destinations[destination_id] = {**data, "id": destination_id}
    return jsonify({"message": "Destination added", "id": destination_id}), 201

@blp.route("/<destination_id>", methods=["DELETE"])
@token_required
@blp.response(200, description="Destination deleted successfully")
def delete_destination(destination_id):
    """Delete a destination by ID."""
    if request.user.get("role") != "Admin":
        return jsonify({"error": "Admin privileges required"}), 403
    if destination_id not in destinations:
        return jsonify({"error": "Destination not found"}), 404
    del destinations[destination_id]
    return jsonify({"message": "Destination deleted"}), 200

# Register Blueprint
api.register_blueprint(blp)

@app.route("/")
def home():
    return "Destination Service is running!"

if __name__ == "__main__":
    app.run(debug=True, port=5002)