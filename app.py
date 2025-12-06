from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from config import config
import os
from models import db, User
from routes import api_bp
from auth_routes import auth_bp
from email_service import mail
from scheduler import init_scheduler, shutdown_scheduler
import atexit

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page.'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    # Register blueprints
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Initialize scheduler
    init_scheduler(app)
    
    # Shutdown scheduler on exit
    atexit.register(shutdown_scheduler)
    
    # Routes
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """User login page"""
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        return render_template('login.html')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """User registration page"""
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        return render_template('register.html')
    
    @app.route('/logout')
    @login_required
    def logout():
        """User logout"""
        from flask_login import logout_user
        logout_user()
        flash('You have been logged out successfully.', 'success')
        return redirect(url_for('login'))
    
    @app.route('/')
    @login_required
    def index():
        """Dashboard page"""
        return render_template('index.html')
    
    @app.route('/checkout')
    @login_required
    def checkout():
        """Equipment checkout page"""
        return render_template('checkout.html')
    
    @app.route('/students')
    @login_required
    def students():
        """Student management page"""
        return render_template('students.html')
    
    @app.route('/equipment')
    @login_required
    def equipment():
        """Equipment management page"""
        return render_template('equipment.html')
    
    @app.route('/loans')
    @login_required
    def loans():
        """Loans management page"""
        return render_template('loans.html')
    
    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    # Non-deployment development server (localhost only, better for development)
    app.run(debug=True, host='127.0.0.1', port=5000)
