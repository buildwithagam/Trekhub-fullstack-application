from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_required, 
    get_jwt_identity
)
from models.user import User
from extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    phone = data.get('phone')
    age_limit = data.get("age_limit")

    if not email or not password or not name:
        return jsonify({'error': 'Email, password, and name are required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'User with this email already exists'}), 400

    user = User(
        email=email,
        name=name,
        phone=phone,
        role='TREKKER',
        is_active=True,
        is_blacklisted=False
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    # Invalidate admin stats cache on new registration
    from extensions import cache
    cache.delete("admin_dashboard_stats")

    return jsonify({'message': 'Registration successful'}), 201

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401

    if not user.is_active:
        return jsonify({'error': 'Your account is deactivated'}), 403

    if user.is_blacklisted:
        return jsonify({'error': 'Your account is blacklisted'}), 403

    # Add role & email to access token claims
    additional_claims = {
        'role': user.role,
        'name': user.name,
        'email': user.email
    }
    access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=str(user.id), additional_claims=additional_claims)

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role,
            'phone': user.phone
        }
    }), 200

@auth_bp.route('/api/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    user = db.session.get(User, int(identity))
    if not user or not user.is_active or user.is_blacklisted:
        return jsonify({'error': 'Unauthorized or account suspended'}), 401

    additional_claims = {
        'role': user.role,
        'name': user.name,
        'email': user.email
    }
    new_access_token = create_access_token(identity=identity, additional_claims=additional_claims)
    return jsonify({'access_token': new_access_token}), 200

@auth_bp.route('/api/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json() or {}
    email = data.get('email')
    new_password = data.get('new_password')

    if not email or not new_password:
        return jsonify({'error': 'Email and new password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.set_password(new_password)
    db.session.commit()
    return jsonify({'message': 'Password reset successful'}), 200

@auth_bp.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_me():
    identity = get_jwt_identity()
    user = db.session.get(User, int(identity))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role,
            'phone': user.phone,
            'is_active': user.is_active,
            'is_blacklisted': user.is_blacklisted
        }
    }), 200



