"""
Sample Data Loader for Equipment Loan System
Run this script to populate the database with sample data for testing
"""

from app import create_app, db
from models import Student, Equipment, Staff, Loan
from datetime import datetime, timedelta

def load_sample_data():
    """Load sample data into the database"""
    app = create_app('development')
    
    with app.app_context():
        # Clear existing data (optional)
        db.drop_all()
        db.create_all()
        
        print("Loading sample students...")
        students = [
            Student(
                first_name="Juan",
                last_name="Dela Cruz",
                program="Computer Science",
                year_level=2,
                email="juan.delacruz@university.edu",
                status="active"
            ),
            Student(
                first_name="Maria",
                last_name="Santos",
                program="Information Technology",
                year_level=3,
                email="maria.santos@university.edu",
                status="active"
            ),
            Student(
                first_name="Carlos",
                last_name="Reyes",
                program="Computer Science",
                year_level=1,
                email="carlos.reyes@university.edu",
                status="active"
            ),
            Student(
                first_name="Ana",
                last_name="Garcia",
                program="Software Engineering",
                year_level=4,
                email="ana.garcia@university.edu",
                status="active"
            ),
        ]
        
        for student in students:
            db.session.add(student)
        
        db.session.commit()
        print(f"✓ Added {len(students)} students")
        
        print("Loading sample equipment...")
        equipment = [
            Equipment(
                name="MacBook Pro 16",
                model="MacBook Pro 16 2023 M3",
                category="Laptop",
                serial_number="MLB123456",
                condition="Good",
                availability_status="Available"
            ),
            Equipment(
                name="Dell XPS 13",
                model="Dell XPS 13 Plus",
                category="Laptop",
                serial_number="DELL987654",
                condition="Good",
                availability_status="Available"
            ),
            Equipment(
                name="iPad Pro 12.9",
                model="iPad Pro 12.9 6th Gen",
                category="Tablet",
                serial_number="IPAD111222",
                condition="Good",
                availability_status="On Loan"
            ),
            Equipment(
                name="External Hard Drive",
                model="WD Blue 2TB",
                category="Storage",
                serial_number="WD2TB333444",
                condition="Good",
                availability_status="Available"
            ),
            Equipment(
                name="USB-C Hub",
                model="Anker 7-in-1",
                category="Accessory",
                serial_number="HUB555666",
                condition="Fair",
                availability_status="Available"
            ),
            Equipment(
                name="Wireless Mouse",
                model="Logitech MX Master 3S",
                category="Accessory",
                serial_number="MOUSE777888",
                condition="Good",
                availability_status="Available"
            ),
        ]
        
        for item in equipment:
            db.session.add(item)
        
        db.session.commit()
        print(f"✓ Added {len(equipment)} equipment items")
        
        print("Loading sample staff...")
        staff = [
            Staff(
                name="John Smith",
                email="john.smith@university.edu",
                role="IT Manager"
            ),
            Staff(
                name="Sarah Johnson",
                email="sarah.johnson@university.edu",
                role="IT Technician"
            ),
        ]
        
        for member in staff:
            db.session.add(member)
        
        db.session.commit()
        print(f"✓ Added {len(staff)} staff members")
        
        print("Loading sample loans...")
        loans = [
            Loan(
                student_id=students[0].id,
                equipment_id=equipment[2].id,  # iPad (On Loan)
                date_borrowed=datetime.utcnow().date() - timedelta(days=5),
                date_due=datetime.utcnow().date() + timedelta(days=10),
                status="Borrowed"
            ),
            Loan(
                student_id=students[1].id,
                equipment_id=equipment[0].id,  # MacBook
                date_borrowed=datetime.utcnow().date() - timedelta(days=1),
                date_due=datetime.utcnow().date() + timedelta(days=14),
                status="Borrowed"
            ),
            Loan(
                student_id=students[2].id,
                equipment_id=equipment[3].id,  # External HD
                date_borrowed=datetime.utcnow().date() - timedelta(days=30),
                date_due=datetime.utcnow().date() - timedelta(days=5),  # Overdue!
                status="Borrowed"
            ),
            Loan(
                student_id=students[3].id,
                equipment_id=equipment[1].id,  # Dell XPS
                date_borrowed=datetime.utcnow().date() - timedelta(days=20),
                date_due=datetime.utcnow().date() - timedelta(days=10),
                date_returned=datetime.utcnow().date() - timedelta(days=5),
                status="Returned"
            ),
        ]
        
        for loan in loans:
            db.session.add(loan)
        
        db.session.commit()
        print(f"✓ Added {len(loans)} sample loans")
        
        print("\n✅ Sample data loaded successfully!")
        print("\nSample Data Summary:")
        print(f"  - {len(students)} Students")
        print(f"  - {len(equipment)} Equipment items")
        print(f"  - {len(staff)} Staff members")
        print(f"  - {len(loans)} Loans (including overdue items)")
        print("\nYou can now log in and test the system!")

if __name__ == "__main__":
    load_sample_data()
