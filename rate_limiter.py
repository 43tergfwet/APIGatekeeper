from flask import request, Flask, jsonify
from functools import wraps
from time import time
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

request_timestamps = {}

REQUEST_LIMIT = int(os.getenv('REQUEST_LIMIT', 100))
TIME_PERIOD = int(os.getenv('TIME_PERIOD', 3600))

def rate_limiter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        client_identifier = request.remote_addr or "user_id_if_authenticated"
        current_time = time()
        if client_identifier not in request_timestamps:
            request_timestamps[client_identifier] = []
        request_timestamps[client_identifier] = [timestamp for timestamp in request_timestamps[client_identifier] if current_time - timestamp < TIME_PERIOD]
        if len(request_timestamps[client_identifier]) < REQUEST_LIMIT:
            request_timestamps[client_identifier].append(current_time)
            return func(*args, **kwargs)
        else:
            return jsonify({'error': 'Too many requests'}), 429
    return wrapper

@app.route('/protected')
@rate_limiter
def protected():
    return jsonify({'message': 'This is a rate limited route'})

if __name__ == '__main__':
    app.run(debug=True)