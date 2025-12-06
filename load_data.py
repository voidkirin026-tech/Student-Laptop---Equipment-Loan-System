# This shall serve as the official data loading module for the project.

from app import create_app, db # pyright: ignore[reportMissingImports]
from models import Student, Equipment, Staff, Loan, User # pyright: ignore[reportMissingImports]
from datetime import datetime, timedelta

def load_data():
    app = create_app('development')
    
    with = app.app_context():
        db.drop_all()
        db.create_all()
        
        print("Loading admin and staff users...")
        users = [
            User(
                username="administrator",
                email="administrator@university.edu"
                first_name="Admin",
                last_name="User",
                role="Administrator",
                status="active"
            ),
            User(
                username="staff1",
                email="staff1@university.edu",
                first_name="Kirin",
                last_name="Void",
                role="Staff",
                status="active"
            )
            User(
                username="borrower1",
                email="student@university.edu",
                first_name="Sample"
                last_name="Borrower"
                
            )
        ]