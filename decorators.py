"""Permission decorators for role-based access control"""
from functools import wraps
from flask import jsonify, redirect, url_for, request
from flask_login import current_user

def staff_required(f):
    """Decorator to require staff or admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_staff():
            if request.is_json:
                return jsonify({'error': 'Staff access required'}), 403
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            if request.is_json:
                return jsonify({'error': 'Admin access required'}), 403
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def borrower_required(f):
    """Decorator to require borrower role (anyone can borrow)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_borrower():
            if request.is_json:
                return jsonify({'error': 'Borrower access required'}), 403
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
