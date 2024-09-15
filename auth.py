import os
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, request, jsonify, make_response
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)

users_db = {
    "user1": {"password": "password123", "roles": ["admin"]},
    "user2": {"password": "pass456", "roles": ["user"]}
}

def check_user(username, password):
    user = users_db.get(username)
    if not user:
        return False
    return user["password"] == password

def register_user(username, password):
    if username in users_db:
        return False, "User already exists."
    users_db[username] = {"password": password, "roles": ["user"]}
    return True, "User created successfully."

def encode_auth_token(user_id):
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1, seconds=5),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    except Exception as e:
        return e

def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            current_user = decode_auth_token(token)
            if not isinstance(current_user, str):
                request.current_user = current_user
            else:
                return jsonify({'message': current_user}), 401
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated

def check_permission(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization', None)
            if token:
                token = token.split(" ")[1]
                user_id = decode_auth_token(token)
                user_roles = users_db.get(user_id, {}).get("roles", [])
                if required_role not in user_roles:
                    return jsonify({'message': 'You do not have permission to perform this action'}), 403
            else:
                return jsonify({'message': 'Token is missing!'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if check_user(username, password):
        token = encode_auth_token(username)
        return jsonify({'token': token})
    else:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    success, message = register_user(username, password)
    if success:
        return jsonify({'message': message})
    else:
        return jsonify({'message': message}), 400

@app.route('/protected', methods=['GET'])
@token_required
@check_permission('admin')
def protected():
    return jsonify({'message': 'This is only available for admins'})

if __name__ == '__main__':
    app.run(debug=True)