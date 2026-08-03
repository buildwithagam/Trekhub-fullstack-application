from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from models.user import User

def role_required(*roles):
    def wrapper(f):
        @wraps(f)
        @jwt_required()
        def decorated_view(*args, **kwargs):
            # Check user status in database to immediately reflect block/deactivation
            user_id = get_jwt_identity()
            user = User.query.get(int(user_id)) if user_id else None
            if not user or not user.is_active or user.is_blacklisted:
                return jsonify({'error': 'Unauthorized: Account is inactive or blacklisted'}), 401

            claims = get_jwt()
            user_role = claims.get('role')
            
            # Allow case-insensitive comparison or force upper
            roles_upper = [r.upper() for r in roles]
            if not user_role or user_role.upper() not in roles_upper:
                return jsonify({'error': f"Forbidden: Access denied. Required role: {', '.join(roles_upper)}"}), 403
                
            return f(*args, **kwargs)
        return decorated_view
    return wrapper

