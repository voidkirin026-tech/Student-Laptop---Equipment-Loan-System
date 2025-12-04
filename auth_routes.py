"""Authentication routes for user login/register/logout"""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validation
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Username, email, and password required'}), 400
    
    if len(data.get('password', '')) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    # Check if user exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create user
    user = User(
        username=data['username'],
        email=data['email'],
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', ''),
        role=data.get('role', 'borrower')  # Default to borrower
    )
    user.set_password(data['password'])
    
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login_api():
    """API login endpoint"""
    data = request.get_json()
    
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    if user.status != 'active':
        return jsonify({'error': 'User account is not active'}), 403
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    login_user(user)
    
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict()
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout_api():
    """API logout endpoint"""
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/current-user', methods=['GET'])
def get_current_user():
    """Get current logged-in user"""
    if current_user.is_authenticated:
        return jsonify(current_user.to_dict()), 200
    return jsonify({'error': 'Not authenticated'}), 401

@auth_bp.route('/users', methods=['GET'])
@login_required
def get_users():
    """Get all users (admin only)"""
    if not current_user.is_admin():
        return jsonify({'error': 'Admin access required'}), 403
    
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@auth_bp.route('/users/<user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    """Get user details"""
    if user_id != current_user.id and not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200

@auth_bp.route('/users/<user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    """Update user details (admin or self)"""
    if user_id != current_user.id and not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    # Update allowed fields
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'email' in data and (data['email'] != user.email):
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already in use'}), 400
        user.email = data['email']
    
    # Admin only fields
    if current_user.is_admin():
        if 'role' in data:
            user.role = data['role']
        if 'status' in data:
            user.status = data['status']
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/users/<user_id>/change-password', methods=['PUT'])
@login_required
def change_password(user_id):
    """Change user password"""
    if user_id != current_user.id and not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    if not data.get('old_password') or not data.get('new_password'):
        return jsonify({'error': 'Old and new password required'}), 400
    
    if len(data.get('new_password', '')) < 6:
        return jsonify({'error': 'New password must be at least 6 characters'}), 400
    
    # Verify old password (unless admin changing another user's password)
    if user_id == current_user.id and not user.check_password(data['old_password']):
        return jsonify({'error': 'Current password is incorrect'}), 401
    
    user.set_password(data['new_password'])
    
    try:
        db.session.commit()
        return jsonify({'message': 'Password changed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/users/<user_id>/disable', methods=['PUT'])
@login_required
def disable_user(user_id):
    """Disable user account (admin only)"""
    if not current_user.is_admin():
        return jsonify({'error': 'Admin access required'}), 403
    
    if user_id == current_user.id:
        return jsonify({'error': 'Cannot disable your own account'}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user.status = 'disabled'
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'User disabled successfully',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
