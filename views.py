from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_CONFIGS = {}
USERS = {}
LOGS = []

@app.route('/api/routes', methods=['POST', 'GET', 'PUT', 'DELETE'])
def manage_routes():
    if request.method == 'POST':
        data = request.json
        API_CONFIGS[data['id']] = data
        return jsonify({'message': 'Route created successfully'}), 201
    elif request.method == 'GET':
        return jsonify(API_CONFIGS), 200
    elif request.method == 'PUT':
        data = request.json
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
        USERS[user['id']] = user
        return jsonify({'message': 'User created successfully'}), 201
    elif request.method == 'GET':
        return jsonify(USERS), 200
    elif request.method == 'PUT':
        user = request.json
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
        LOGS.append(log)
        return jsonify({'message': 'Log added successfully'}), 201
    elif request.method == 'GET':
        return jsonify(LOGS), 200

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", 5000))