# Student Laptop/Equipment Loan System

A complete web-based information system for managing equipment checkouts, tracking loans, and automating overdue notifications.

## System Overview

This system implements **Scenario #7** from the final project requirements:
- ✅ Form for IT staff to log equipment checkouts (item, student, due date)
- ✅ Equipment database with status tracking ("Available" or "On Loan")
- ✅ Active loan logging and recording
- ✅ Automatic equipment status updates upon checkout
- ✅ Daily scheduled check for overdue items (past due date)
- ✅ Automatic email reminders for overdue items to students

## Technology Stack

- **Backend**: Python 3.8+ with Flask
- **Database**: PostgreSQL 12+
- **Task Scheduler**: APScheduler (daily automated tasks)
- **Email Service**: Flask-Mail (SMTP support)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **ORM**: SQLAlchemy

## Features

### Core Functionality
1. **Equipment Management**
   - Add and track equipment inventory
   - Track equipment status (Available/On Loan)
   - Monitor equipment condition
   - View equipment history

2. **Loan Management**
   - Log equipment checkouts with due dates
   - Track active and returned loans
   - Automatic status updates
   - View loan history

3. **Student Management**
   - Maintain student database
   - Track student program and year level
   - Monitor borrowing history

4. **Automated Email Notifications**
   - Checkout confirmation emails
   - Return confirmation emails
   - Overdue reminder emails (daily)
   - Email delivery logging

5. **Scheduled Tasks**
   - Daily overdue check at 8:00 AM
   - Automatic email dispatch for overdue items
   - Configurable scheduling

6. **Dashboard & Analytics**
   - Real-time statistics
   - Overdue items monitoring
   - Active loans tracking
   - Equipment availability status

7. **Audit Trail**
   - Log all system actions
   - Track equipment status changes
   - Email delivery history

## Quick Start

### 1. Prerequisites
```bash
# Python 3.8+
python --version

# PostgreSQL 12+
psql --version
```

### 2. Setup
```bash
# Clone/Download project
cd "Student Laptop & Equipment Loan System"

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Database
```bash
# Create PostgreSQL database
createdb equipment_loan_db

# Copy and configure environment
cp .env.example .env
# Edit .env with your database URL and email settings
```

### 4. Initialize Database
```bash
# Run Python shell
python

# In Python:
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
exit()
```

### 5. Run the Application
```bash
python app.py
```

Visit: **http://localhost:5000**

## Database Schema

### Students Table
```sql
id, first_name, last_name, program, year_level, email, status, created_at
```

### Equipment Table
```sql
id, name, category, serial_number, condition, availability_status, created_at
```

### Loans Table
```sql
id, student_id, equipment_id, date_borrowed, date_due, date_returned, status, created_at
```

### Staff Table
```sql
id, name, email, role, created_at
```

### Email Logs Table
```sql
id, loan_id, recipient_email, email_type, sent_at, status
```

### Audit Logs Table
```sql
id, action, table_name, record_id, details, created_at
```

## API Endpoints

### Students
- `GET /api/students` - List all students
- `POST /api/students` - Create new student
- `GET /api/students/<id>` - Get student details

### Equipment
- `GET /api/equipment` - List all equipment
- `POST /api/equipment` - Add new equipment
- `GET /api/equipment/available` - Get available equipment only
- `GET /api/equipment/<id>` - Get equipment details

### Loans
- `POST /api/loans/checkout` - Checkout equipment
- `GET /api/loans` - List all loans
- `GET /api/loans/active` - List active loans only
- `GET /api/loans/overdue` - List overdue loans
- `POST /api/loans/<id>/return` - Return equipment
- `GET /api/loans/<id>` - Get loan details

### Staff
- `GET /api/staff` - List staff members
- `POST /api/staff` - Add staff member

### System
- `GET /api/health` - Health check
- `GET /api/audit-logs` - View audit trail (last 100)

## Using the System

### Adding Equipment
1. Navigate to "Manage Equipment"
2. Click "+ Add New Equipment"
3. Enter: Name, Category, Serial Number, Condition
4. Submit

### Checking Out Equipment
1. Go to "Checkout Equipment"
2. Select Student
3. Select Available Equipment
4. Set Due Date
5. Submit
   - ✓ Equipment status → "On Loan"
   - ✓ Checkout confirmation email sent to student
   - ✓ Loan recorded in database

### Returning Equipment
1. Go to "Loan Management" or "Dashboard"
2. Find active loan
3. Click "Return" button
   - ✓ Equipment status → "Available"
   - ✓ Return confirmation email sent
   - ✓ Loan marked as "Returned"

### Monitoring Overdue Items
1. Dashboard shows overdue count
2. Click "Overdue Items" button
3. View all overdue equipment with days overdue
4. System automatically emails students daily at 8 AM

## Configuration

### Email Setup (Gmail Example)
```
1. Enable 2-Factor Authentication in Gmail
2. Generate App Password (16 characters)
3. Add to .env:
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=xxxx xxxx xxxx xxxx
```

### Change Scheduled Task Time
Edit `scheduler.py`:
```python
scheduler.add_job(
    func=check_overdue_loans,
    trigger="cron",
    hour=8,      # 24-hour format (0-23)
    minute=0,
)
```

### Database Connection
Update in `.env`:
```
DATABASE_URL=postgresql://user:password@localhost:5432/equipment_loan_db
```

## Loading Sample Data

```bash
python load_sample_data.py
```

This creates:
- 4 sample students
- 6 equipment items
- 2 staff members
- 4 sample loans (including overdue items)

## Testing

### Via Web Interface
1. Access http://localhost:5000
2. Add equipment
3. Create students (can use API)
4. Checkout equipment
5. Check dashboard for statistics
6. Test return functionality

### Via API
```bash
# Get all equipment
curl http://localhost:5000/api/equipment

# Checkout equipment
curl -X POST http://localhost:5000/api/loans/checkout \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "uuid",
    "equipment_id": "uuid",
    "date_due": "2025-12-31"
  }'

# Get overdue loans
curl http://localhost:5000/api/loans/overdue
```

## System Architecture

```
┌─────────────────────────────────────────┐
│        Web Browser (Frontend)           │
│  Dashboard | Checkout | Inventory      │
└──────────────┬──────────────────────────┘
               │ HTTP/AJAX
┌──────────────▼──────────────────────────┐
│      Flask Web Application              │
│  ├─ Routes & Views                      │
│  ├─ Form Handlers                       │
│  └─ API Endpoints                       │
└──────┬─────────────────────────┬────────┘
       │                         │
       │ SQL                     │ Email
       │                         │ SMTP
┌──────▼──────────┐    ┌────────▼──────────┐
│  PostgreSQL DB  │    │   Email Service   │
│  ├─ Students    │    │   (Flask-Mail)    │
│  ├─ Equipment   │    └───────────────────┘
│  ├─ Loans       │
│  ├─ Email Logs  │
│  └─ Audit Logs  │
└─────────────────┘
       ▲
       │ Scheduled Task
       │
┌──────┴──────────────────────────────────┐
│      APScheduler (Daily 8 AM)           │
│  Check Overdue Items → Send Emails      │
└──────────────────────────────────────────┘
```

## Project Files

```
.
├── app.py                   # Main Flask application
├── config.py               # Configuration (dev, test, prod)
├── models.py               # SQLAlchemy database models
├── routes.py               # REST API endpoints
├── email_service.py        # Email handling
├── scheduler.py            # Background task scheduling
├── load_sample_data.py     # Sample data loader
├── requirements.txt        # Python dependencies
├── Database Schema.sql     # SQL database schema
├── .env.example           # Environment variables template
├── SETUP_GUIDE.md         # Detailed setup instructions
├── README.md              # This file
├── templates/             # HTML templates
│   ├── base.html          # Base layout
│   ├── index.html         # Dashboard
│   ├── checkout.html      # Checkout form
│   ├── equipment.html     # Equipment management
│   └── loans.html         # Loan management
└── static/                # Static files
    ├── css/
    │   └── style.css      # Styling
    └── js/
        ├── dashboard.js   # Dashboard functionality
        ├── checkout.js    # Checkout form
        ├── equipment.js   # Equipment management
        └── loans.js       # Loan management
```

## Troubleshooting

### Email Not Sending
- Verify SMTP settings in `.env`
- Check email credentials are correct
- Enable "Less secure app access" for Gmail
- Check console for error messages

### Database Connection Error
- Ensure PostgreSQL is running
- Verify DATABASE_URL format
- Check username/password
- Create database if it doesn't exist

### Scheduler Not Running
- Check logs for startup message
- Verify Python is in development mode
- Ensure APScheduler is installed
- Check timezone settings

### Port Already in Use
```bash
# Change port in app.py
app.run(port=5001)
```

## Features Implemented vs Requirements

| Requirement | Implementation | Status |
|-------------|-----------------|--------|
| Checkout form for IT staff | checkout.html with form | ✅ |
| Equipment database | PostgreSQL equipment table | ✅ |
| Log active loans | loans table with tracking | ✅ |
| Auto-update status | Automatic on checkout/return | ✅ |
| Daily scheduler | APScheduler at 8 AM | ✅ |
| Overdue checking | Query date_due < today | ✅ |
| Email reminders | Flask-Mail notifications | ✅ |
| Email logging | email_logs table | ✅ |
| Audit trail | audit_logs table | ✅ |

## Scalability & Future Enhancements

### Potential Additions
- User authentication and roles
- Equipment damage/loss tracking
- Fine calculation for late returns
- Batch loan operations
- Export to CSV/Excel
- Mobile app integration
- Real-time notifications (WebSockets)
- Equipment QR code scanning
- Integration with university email directory
- Analytics dashboard
- Reservation system (pre-booking)

## Security Considerations

- **Input Validation**: All API inputs validated
- **CSRF Protection**: Should add in production
- **SQL Injection**: Prevented by SQLAlchemy ORM
- **Email Security**: Uses SMTP TLS
- **Environment Variables**: Sensitive data in .env
- **Audit Trail**: All actions logged

## Performance Optimization

- Database indexes on foreign keys
- Efficient queries with lazy loading
- Scheduled tasks don't block requests
- Frontend pagination ready
- Static file caching

## Support & Documentation

- See `SETUP_GUIDE.md` for detailed installation
- Code comments throughout for clarity
- API endpoints documented above
- Flask documentation: https://flask.palletsprojects.com/
- SQLAlchemy docs: https://docs.sqlalchemy.org/

## License

This is an educational project for a school assignment.

---

**Last Updated**: November 2025
**Version**: 1.0
**Python**: 3.8+
**Database**: PostgreSQL 12+
