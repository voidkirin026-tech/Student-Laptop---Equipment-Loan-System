from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from config import config
import os
from models import db
from routes import api_bp
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
    
    # Register blueprints
    app.register_blueprint(api_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Initialize scheduler
    init_scheduler(app)
    
    # Shutdown scheduler on exit
    atexit.register(shutdown_scheduler)
    
    # Routes
    @app.route('/')
    def index():
        """Dashboard page"""
        return render_template('index.html')
    
    @app.route('/checkout')
    def checkout():
        """Equipment checkout page"""
        return render_template('checkout.html')
    
    @app.route('/equipment')
    def equipment():
        """Equipment management page"""
        return render_template('equipment.html')
    
    @app.route('/loans')
    def loans():
        """Loans management page"""
        return render_template('loans.html')
    
    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    app.run(debug=True, host='0.0.0.0', port=5000)
