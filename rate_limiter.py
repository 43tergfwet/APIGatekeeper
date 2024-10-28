from flask import request, Flask, jsonify, g
from functools import wraps
from time import time
import os
from dotenv import load_dotenv
import logging

load_dotenv()

app = Flask(__name__)

# Set up basic logging
logging.basicConfig(level=logging.INFO)

request_timestamps = {}

# Default rate limits
REQUEST_LIMIT = int(os.getenv('REQUEST_LIMIT', 100))
TIME_PERIOD = int(os.getenv('TIME_PERIOD', 3600))

# Enhanced rate limits for demonstration (e.g., authenticated users)
AUTHENTICATED_REQUEST_LIMIT = int(os.getenv('AUTHENTICATED_REQUEST_LIMIT', 200))

def rate_limiter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Assuming a function `is_authenticated` to check authentication
        # For illustration; implement your authentication check logic
        is_authenticated = check_authentication_status(request)
        client_identifier = request.remote_addr
        current_time = time()
        
        if is_authenticated:
            client_identifier += "_authenticated"
            limit = AUTHENTICATED_REQUEST_LIMIT
        else:
            limit = REQUEST_LIMIT

        if client_identifier not in request_timestamps:
            request_timestamps[client_identifier] = []
        
        request_timestamps[client_identifier] = [
            timestamp for timestamp in request_timestamps[client_identifier] if current_time - timestamp < TIME_PERIOD
        ]
        
        if len(request_timestamps[client_identifier]) < limit:
            request_timestamps[client_identifier].append(current_time)
            logging.info(f"Request allowed for {client_identifier}.")
            return func(*args, **kwargs)
        else:
            logging.warning(f"Rate limit exceeded for {client_identifier}.")
            return jsonify({'error': 'Too many requests'}), 429
    return wrapper

def check_authentication_status(request):
    # Placeholder for actual authentication logic
    # Return True if the user is authenticated, False otherwise
    # This can be based on tokens, session IDs, etc.
    return False  # Example: Not authenticated by default

@app.route('/protected')
@rate_limiter
def protected():
    return jsonify({'message': 'This is a rate limited route'})

if __name__ == '__main__':
    app.run(debug=True)