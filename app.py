from flask import Flask, jsonify
from Users.user_service import app  # Import the 'app' from user_service.py in the Users folder
from flask_smorest import Api



# Set the API title and OpenAPI version in your app configuration
app.config['API_TITLE'] = 'My API Title'
app.config['API_VERSION'] = '1.0.0'
app.config['OPENAPI_VERSION'] = '3.0.2'  # Set the OpenAPI version



@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API!"})

@app.route('/api/example', methods=['GET'])
def example():
    return jsonify({"data": "This is an example endpoint"})

# You don't need to create the app again; it's imported from user_service.py
if __name__ == '__main__':
    app.run(debug=True)
