from functools import wraps
from flask import request, jsonify
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key-change-this"

def generate_token(user_id):
    """Generate a JWT token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    """Verify and decode a JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator to require valid token in Authorization header"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({"error": "Invalid authorization header"}), 401

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        # Verify token
        payload = verify_token(token)
        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401

        # Pass user_id to the route function
        return f(payload['user_id'], *args, **kwargs)

    return decorated_function

# Example usage:
# @app.route('/protected', methods=['GET'])
# @token_required
# def protected_route(user_id):
#     return jsonify({"message": f"Hello user {user_id}"})
