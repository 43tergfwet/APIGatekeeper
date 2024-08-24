from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from flask import abort

load_dotenv()

app = Flask(__name__)

API_CONFIGS = {}
USERS = {}
LOGS = []

def validate_route_data(data):
    """
    Validate the required fields in API route configuration.
    """
    if not data or not isinstance(data, dict):
        return False
    required_fields = ['id']
    return all(field in data for field in required_fields)

def validate_user_data(data):
    """
    Validate the required fields in user data.
    """
    if not data or not isinstance(data, dict):
        return False
    required_fields = ['id']
    return all(field in data for field in required_fields)

@app.route('/api/routes', methods=['POST', 'GET', 'PUT', 'DELETE'])
def manage_routes():
    if request.method == 'POST':
        data = request.json
        if not validate_route_data(data):
            return jsonify({'message': 'Invalid route configuration'}), 400
        API_CONFIGS[data['id']] = data
        return jsonify({'message': 'Route created successfully'}), 201
    elif request.method == 'GET':
        return jsonify(API_CONFIGS), 200
    elif request.method == 'PUT':
        data = request.json
        if not validate_route_data(data):
            return jsonify({'message': 'Invalid route configuration'}), 400
        if data['id'] in API_CONFIGS:
            API_CONFIGS[data['id']].update(data)
            return jsonify(API_CONFIGS[data['id']]), 200
        else:
            return jsonify({'message': 'Route not found'}), 404
    elif request.method == 'DELETE':
        route_id = request.args.get('id')
        if route_id in API_CONFIGS:
            del API_CONFIGS[route_id]
            return jsonify({'message': 'Route deleted successfully'}), 200
        else:
            return jsonify({'message': 'Route not found'}), 404

@app.route('/api/users', methods=['POST', 'GET', 'PUT', 'DELETE'])
def manage_users():
    if request.method == 'POST':
        user = request.json
        if not validate_user_data(user):
            return jsonify({'message': 'Invalid user data'}), 400
        USERS[user['id']] = user
        return jsonify({'message': 'User created successfully'}), 201
    elif request.method == 'GET':
        return jsonify(USERS), 200
    elif request.method == 'PUT':
        user = request.json
        if not validate_user_data(user):
            return jsonify({'message': 'Invalid user data'}), 400
        if user['id'] in USERS:
            USERS[user['id']].update(user)
            return jsonify(USERS[user['id']]), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    elif request.method == 'DELETE':
        user_id = request.args.get('id')
        if user_id in USERS:
            del USERS[user_id]
            return jsonify({'message': 'User deleted successfully'}), 200
        else:
            return jsonify({'message': 'User not found'}), 404

@app.route('/api/logs', methods=['POST', 'GET'])
def manage_logs():
    if request.method == 'POST':
        log = request.json
        if not log or not isinstance(log, dict):
            return jsonify({'message': 'Invalid log data'}), 400
        LOGS.append(log)
        return jsonify({'message': 'Log added successfully'}), 201
    elif request.method == 'GET':
        return jsonify(LOGS), 200

if __name__ == '__main__':
    port = os.getenv("PORT", 5000)
    try:
        port = int(port)
    except ValueError:
        port = 5000
    app.run(debug=True, port=port)