# This shall serve as the official data loading module for the project.

from app import create_app, db # pyright: ignore[reportMissingImports]
from models import Student, Equipment, Staff, Loan, User # pyright: ignore[reportMissingImports]
from datetime import datetime, timedelta, timezone

def load_sample_data():
    """Load sample data into the database"""
    app = create_app('development')
    
    with app.app_context():
        # Clear existing data (optional)
        db.drop_all()
        db.create_all()
        
        print("Loading admin and staff users...")
        users = [
            User(
                username="administrator",
                email="administrator@gmail.com",
                first_name="Admin",
                last_name="User",
                role="Administrator",
                status="active"
            ),
            User(
                username="staff1",
                email="staff1@gmail.com",
                first_name="Kirin",
                last_name="Void",
                role="Staff",
                status="active"
            ),
            User(
                username="borrower1",
                email="student@gmail.com",
                first_name="Sample",
                last_name="Borrower",
                role="borrower",
                status="active"
            ),
        ]
        
        users[0].set_password("655321")
        users[1].set_password("655322")
        users[2].set_password("655323")
        
        for user in users:
            db.session.add(user)
        
        db.session.commit()
        print(f"✓ Added {len(users)} users")
        print("     - Admin: username=administrator, password=655321")
        print("     - Staff: username=staff1, password=655322")
        print("     - Borrower: username=borrower1, password=655323")
        
        # All emails listed below are examples only except for the first one
        # That is my email
        print("Loading sample students...")
        students = [
            Student(
                first_name="Josef Michael",
                last_name="Damaso",
                program="Information Technology",
                year_level=2,
                email="voidkirin026@gmail.com",
                status="active"
            ),
            Student(
                first_name="Khixter",
                last_name="Mosqueda",
                program="8th Grade",
                year_level=8,
                email="khixtermosqueda@gmail.com",
                status="active"
            ),
            Student(
                first_name="Jasmine",
                last_name="Camacho",
                program="Psychology",
                year_level=1,
                email="jasminecamacho@gmail.com",
                status="active"
            ),
            Student(
                first_name="Julianne Marie",
                last_name="Mosqueda",
                program="Accounting",
                year_level=1,
                email="juliannemosqueda@gmail.com",
                status="active"
            ),
            Student(
                first_name="Syiam",
                last_name="Fortunado",
                program="Computer Science",
                year_level=2,
                email="syiamfortunado@gmail.com",
                status="active"
            ),
            Student(
                first_name="John Anthony",
                last_name="Santiago",
                program="Computer Science",
                year_level=2,
                email="johnsantiago@gmail.com",
                status="active"
            ),
            Student(
                first_name="Ranie",
                last_name="Bandejas",
                program="Information Technology",
                year_level=2,
                email="raniebandejas@gmail.com",
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
                serial_number="MBP123456",
                condition="Excellent",
                availability_status="Available"
            ),
            Equipment(
                name="Dell XPS 13",
                model="Dell XPS 13 Plus",
                category="Laptop",
                serial_number="DELLXPS653",
                condition="Good",
                availability_status="Available"
            ),
            Equipment(
                name="iPad Pro 12.9",
                model="iPad Pro 12.9 6th Gen",
                category="Tablet",
                serial_number="IPADPRO789",
                condition="Excellent",
                availability_status="On Loan"
            ),
            Equipment(
                name="External Hard Drive",
                model="WD Blue 2TB",
                category="Storage",
                serial_number="WD2TB654128",
                condition="Fair",
                availability_status="On Loan"
            ),
            Equipment(
                name="Acer Wired Keyboard",
                model="SK-9626",
                category="Accessory",
                serial_number="DKUSB1B0CK",
                condition="Good",
                availability_status="Available"
            ),
            Equipment(
                name="Acer Wired Mouse",
                model="SM-9023",
                category="Accessory",
                serial_number="DC1121101C",
                condition="Excellent",
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
                name="Kirin Void",
                email="voidkirin026@gmail.com",
                role="IT Manager"
            ),
            Staff(
                name="Loner",
                email="lonemperor62@gmail.com",
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
                equipment_id=equipment[2].id,
                date_borrowed=datetime.now(timezone.utc).date() - timedelta(days=5),
                date_due=datetime.now(timezone.utc).date() + timedelta(days=10),
                status="Borrowed"
            ),
            Loan(
                student_id=students[2].id,
                equipment_id=equipment[3].id,
                date_borrowed=datetime.now(timezone.utc).date() - timedelta(days=30),
                date_due=datetime.now(timezone.utc).date() - timedelta(days=5),
                status="Borrowed"
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
