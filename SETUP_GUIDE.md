# Equipment Loan System - Setup Guide

## Overview
This is a complete Student Laptop/Equipment Loan System built with Python Flask, PostgreSQL, and a modern web interface.

## Features
✅ Equipment checkout form for IT staff
✅ Automatic status updates (Available → On Loan)
✅ Email notifications for checkout and returns
✅ Scheduled daily overdue checking
✅ Automatic overdue reminder emails
✅ Equipment inventory management
✅ Loan tracking and history
✅ Dashboard with statistics
✅ Audit logging

## Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

## Installation

### 1. Clone/Download the project
```bash
cd "c:\Users\Josef Michael\Desktop\Student Laptop & Equipment Loan System"
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup PostgreSQL Database
```sql
-- In PostgreSQL
CREATE DATABASE equipment_loan_db;
```

### 5. Create .env file
Copy `.env.example` to `.env` and update with your settings:
```
DATABASE_URL=postgresql://user:password@localhost:5432/equipment_loan_db
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### 6. Initialize Database
```bash
python
```
Then in Python shell:
```python
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
exit()
```

Or run the SQL schema:
```bash
psql -U user -d equipment_loan_db -f "Database Schema.sql"
```

### 7. Run the application
```bash
python app.py
```

The application will start at: http://localhost:5000

## Project Structure
```
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── models.py             # Database models
├── routes.py             # API endpoints
├── email_service.py      # Email handling
├── scheduler.py          # Background tasks (overdue checking)
├── requirements.txt      # Python dependencies
├── Database Schema.sql   # Database schema
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html       # Dashboard
│   ├── checkout.html    # Checkout form
│   ├── equipment.html   # Equipment management
│   └── loans.html       # Loan management
└── static/              # Static files
    ├── css/
    │   └── style.css
    └── js/
        ├── dashboard.js
        ├── checkout.js
        ├── equipment.js
        └── loans.js
```

## Key Components

### 1. Database Models (models.py)
- **Student**: Stores student information
- **Equipment**: Tracks equipment with status
- **Loan**: Records borrowing transactions
- **Staff**: IT staff members
- **EmailLog**: Email delivery tracking
- **AuditLog**: System action logging

### 2. API Endpoints (routes.py)
- `GET /api/students` - List all students
- `POST /api/students` - Create new student
- `GET /api/equipment` - List equipment
- `POST /api/equipment` - Add equipment
- `GET /api/equipment/available` - Available equipment only
- `POST /api/loans/checkout` - Checkout equipment
- `GET /api/loans` - List all loans
- `GET /api/loans/active` - Active loans only
- `GET /api/loans/overdue` - Overdue loans
- `POST /api/loans/{id}/return` - Return equipment

### 3. Email Service (email_service.py)
Automatically sends:
- Checkout confirmation emails
- Return confirmation emails
- Overdue reminder emails (daily)

### 4. Scheduler (scheduler.py)
- Runs daily at 8:00 AM
- Finds all overdue loans
- Sends reminder emails to students
- Logs all email activities

### 5. Frontend (templates + static)
- Dashboard: Real-time statistics and overdue items
- Checkout Form: Easy equipment checkout interface
- Equipment Management: Add and manage inventory
- Loan Management: Track all loans with filtering

## Usage

### Add Equipment
1. Go to "Manage Equipment"
2. Click "+ Add New Equipment"
3. Fill in details and submit

### Checkout Equipment
1. Go to "Checkout Equipment"
2. Select student and equipment
3. Set due date
4. Submit form
5. Student receives confirmation email

### Return Equipment
1. Go to "Loan Management"
2. Find the active loan
3. Click "Return" button
4. Equipment status automatically changes to "Available"
5. Student receives return confirmation

### Monitor Overdue Items
1. Dashboard shows overdue count
2. Click "Overdue" tab in Loan Management
3. System automatically emails students daily

## Email Setup (Gmail)

1. Enable 2FA in Gmail
2. Generate App Password
3. Use the App Password in `.env`

Example:
```
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=xxxx xxxx xxxx xxxx  # 16 character app password
```

## Configuration

### Scheduled Job Timing
Edit `scheduler.py` to change overdue check time:
```python
scheduler.add_job(
    func=check_overdue_loans,
    trigger="cron",
    hour=8,        # Change this (24-hour format)
    minute=0,      # Change this
    name="check_overdue_loans"
)
```

### Database Connection
Update in `.env`:
```
DATABASE_URL=postgresql://username:password@localhost:5432/equipment_loan_db
```

## Testing

### Manual API Testing
Use Postman or curl:

```bash
# Get all equipment
curl http://localhost:5000/api/equipment

# Create equipment
curl -X POST http://localhost:5000/api/equipment \
  -H "Content-Type: application/json" \
  -d '{"name":"MacBook Pro","category":"Laptop","serial_number":"ABC123"}'

# Checkout equipment
curl -X POST http://localhost:5000/api/loans/checkout \
  -H "Content-Type: application/json" \
  -d '{
    "student_id":"student-uuid",
    "equipment_id":"equipment-uuid",
    "date_due":"2025-12-15"
  }'
```

## Troubleshooting

### Email not sending?
- Check `.env` configuration
- Verify SMTP credentials
- Enable "Less secure app access" (Gmail)
- Check Flask-Mail logs in console

### Database connection error?
- Verify PostgreSQL is running
- Check DATABASE_URL format
- Run schema manually if needed

### Scheduler not running?
- Check Flask environment is development
- Verify APScheduler is installed
- Check console for scheduler start message

## Production Deployment

For production:
1. Change `FLASK_ENV` to `production`
2. Use strong `SECRET_KEY`
3. Configure proper email service
4. Use PostgreSQL with backups
5. Deploy with gunicorn: `gunicorn app:create_app()`
6. Use nginx as reverse proxy
7. Set up SSL/TLS

## Support
For issues or questions about implementation, refer to the code comments and Flask/SQLAlchemy documentation.
