# 📦 Student Laptop/Equipment Loan System

A complete web-based information system for managing equipment checkouts, tracking loans, automating overdue notifications, and providing role-based access control with full multi-user support.

## 🎯 System Overview

This system implements **Scenario #7** from the final project requirements:

- ✅ Form for IT staff to log equipment checkouts (item, student, due date)
- ✅ Equipment database with status tracking ("Available" or "On Loan")
- ✅ Active loan logging and recording
- ✅ Automatic equipment status updates upon checkout
- ✅ Daily scheduled check for overdue items (past due date)
- ✅ Automatic email reminders for overdue items to students
- ✨ **NEW:** Complete user authentication system with password hashing
- ✨ **NEW:** Role-based access control (Admin, Staff, Borrower)
- ✨ **NEW:** Equipment edit and delete functionality
- ✨ **NEW:** Multi-user support with session management

## 🛠️ Technology Stack

- **Backend**: Python 3.13 with Flask 3.0+
- **Database**: PostgreSQL 18+
- **Authentication**: Flask-Login with Werkzeug password hashing
- **Task Scheduler**: APScheduler (daily automated tasks at 8 AM)
- **Email Service**: Flask-Mail (SMTP support)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **ORM**: SQLAlchemy 2.0+
- **Security**: PBKDF2 password hashing, CSRF protection, secure sessions

## Features

### Core Functionality

1. **Student Management**
   - ✅ Add and manage student database with comprehensive profiles
   - ✅ Track student program and year level
   - ✅ Email address validation and storage
   - ✅ Student status tracking (active/inactive)
   - ✅ View complete student roster
   - ✅ Form validation with user feedback
   - ✅ 50+ real-world university programs from 10 categories

2. **Equipment Management**
   - ✅ Add and track equipment inventory with category dropdown (Laptop, Tablet, Storage, etc.)
   - ✅ Custom category support for flexible classification
   - ✅ Track equipment status (Available/On Loan)
   - ✅ Modernized condition dropdown with 5 detailed options (Excellent, Good, Fair, Poor, Damaged)
   - ✅ Equipment model/brand tracking for detailed inventory
   - ✅ View equipment history and details

3. **Loan Management**
   - ✅ Log equipment checkouts with due dates
   - ✅ Form validation (prevents past dates, ensures all fields selected)
   - ✅ Track active and returned loans with filtering
   - ✅ Automatic status updates on checkout/return
   - ✅ View loan history with comprehensive details
   - ✅ Real-time loan status updates

4. **Automated Email Notifications**
   - ✅ Checkout confirmation emails
   - ✅ Return confirmation emails
   - ✅ Overdue reminder emails (daily at 8:00 AM)
   - ✅ Email delivery logging and tracking
   - ✅ Works with Gmail and other SMTP providers

5. **UI/UX Enhancements**
   - ✅ Modern dropdown styling for equipment conditions with color-coded indicators
   - ✅ Intuitive form layouts with grouped fields
   - ✅ Real-time table updates without page refresh
   - ✅ Status badges with visual indicators
   - ✅ Responsive design for all devices
   - ✅ Accessibility-friendly interface

6. **Scheduled Tasks**
   - ✅ Daily overdue check at 8:00 AM
   - ✅ Automatic email dispatch for overdue items
   - ✅ Proper app context handling for database access
   - ✅ Configurable scheduling

7. **Dashboard & Analytics**
   - ✅ Real-time statistics (Total, Available, Active, Overdue)
   - ✅ Overdue items monitoring with days overdue calculation
   - ✅ Active loans tracking
   - ✅ Equipment availability status
   - ✅ Auto-refresh every 30 seconds
   - ✅ Error handling and graceful fallbacks

8. **Audit Trail**
   - ✅ Log all system actions
   - ✅ Track equipment status changes
   - ✅ Email delivery history
   - ✅ Comprehensive action logging

### Quality & Reliability

- ✅ Form validation with user feedback
- ✅ API error handling with meaningful messages
- ✅ Defensive programming throughout
- ✅ Proper database relationships and constraints
- ✅ Safe null value handling
- ✅ Browser tab titles (no more "localhost:5000")

## 🚀 Quick Start (2 Minutes)

### Try It Immediately

```bash
# Install dependencies
pip install -r requirements.txt

# Load sample data (creates users & equipment)
python load_sample_data.py

# Start the server
python app.py
```

Then visit: <http://localhost:5000/login>

### Test Credentials

```bash
Admin:    username=admin    password=admin123
Staff:    username=staff1   password=staff123
Borrower: username=borrower1 password=borrower123
```

---

## 📖 Full Setup Guide

### 1. Prerequisites

```bash
# Python 3.13+
python --version

# PostgreSQL 18+ (or use SQLite for development)
psql --version
```

### 2. Installation

```bash
# Clone project
cd "Student Laptop & Equipment Loan System"

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Database

Edit `config.py` to set your database:

```python
# SQLite (development)
SQLALCHEMY_DATABASE_URI = 'sqlite:///equipment_loan.db'

# PostgreSQL (production)
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/equipment_loan'
```

### 4. Initialize System

```bash
# Load sample data (creates users, equipment, and sample loans)
python load_sample_data.py

# The script will:
# - Create all database tables
# - Create 3 test users (admin, staff, borrower)
# - Add 6 sample equipment items
# - Create 4 sample loans
# - Display credentials for testing
```

### 5. Run Application

```bash
# Start development server
python app.py

# Server starts at: http://localhost:5000
# Login page: http://localhost:5000/login
# Dashboard: http://localhost:5000/ (after login)
```

### 6. Optional: Configure Email

Edit `config.py`:

```python
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'your-email@gmail.com'
MAIL_PASSWORD = 'your-app-password'
```

---

## ✨ What's New (November 30, 2025)

### Authentication & Authorization

- ✅ Secure user login/registration system
- ✅ Password hashing with Werkzeug PBKDF2
- ✅ Three user roles with different permissions
- ✅ Session management
- ✅ Protected pages and API endpoints

### Equipment Management

- ✅ **Edit equipment** - Update name, model, condition
- ✅ **Delete equipment** - With safety checks (prevents deletion if on loan)
- ✅ Equipment action buttons in inventory table
- ✅ Audit logging for all changes

### User Experience

- ✅ Modern login/register pages
- ✅ User badge in navbar showing name and role
- ✅ Logout button (red) in navbar
- ✅ Permission-based UI elements
- ✅ Role restrictions explained in error messages

Visit: <http://localhost:5000>

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

### API Endpoints

### Students

- `GET /api/students` - List all students
- `POST /api/students` - Create new student (requires: first_name, last_name, email)
- `GET /api/students/<id>` - Get student details
- **Example POST:**

  ```json
  {
    "first_name": "Juan",
    "last_name": "Dela Cruz",
    "email": "juan@university.edu",
    "program": "Computer Science",
    "year_level": 2,
    "status": "active"
  }
  ```

### Equipment

- `GET /api/equipment` - List all equipment
- `POST /api/equipment` - Add new equipment
- `GET /api/equipment/available` - Get available equipment only
- `GET /api/equipment/<id>` - Get equipment details
- **Condition values:** Excellent, Good, Fair, Poor, Damaged

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

## University Programs

The system includes **50+ realistic university programs** organized into 10 categories:

### Engineering Programs

- Civil Engineering, Mechanical Engineering, Electrical Engineering
- Electronics Engineering, Chemical Engineering, Industrial Engineering

### Computer Science & IT

- Computer Science, Information Technology, Software Engineering
- Cybersecurity, Data Science, Artificial Intelligence

### Business & Commerce

- Business Administration, Accounting, Finance, Marketing
- Management, Economics, Business Analytics

### Health Sciences

- Medicine, Nursing, Pharmacy, Public Health
- Dentistry, Physical Therapy

### Natural Sciences

- Physics, Chemistry, Biology, Biochemistry
- Mathematics, Environmental Science

### Arts & Humanities

- English Literature, History, Philosophy, Psychology
- Sociology, Anthropology

### Social Sciences

- Law, Political Science, International Relations
- Communication, Journalism, Public Administration

### Creative & Design

- Graphic Design, Architecture, Fine Arts, Music
- Digital Media, Industrial Design

### Education & Teaching

- Elementary Education, Secondary Education, Higher Education
- Special Education

### Agriculture & Environment

- Agriculture, Forestry, Environmental Engineering, Veterinary Medicine

## Using the System

### Navigation Menu

- **Dashboard** - View system statistics and overdue items
- **Students** - Manage student database and profiles
- **Checkout** - Log equipment checkouts to students
- **Equipment** - Manage equipment inventory
- **Loans** - Track active and returned loans

### Adding a Student

1. Navigate to "Students"
2. Fill in the form:
   - First Name and Last Name (required)
   - Email Address (required, validated)
   - Program (optional dropdown)
   - Year Level (optional dropdown)
3. Click "Add Student"
4. Student appears in the table immediately

### Adding Equipment

1. Navigate to "Equipment"
2. Click "+ Add New Equipment"
3. Enter:
   - Equipment Name (required)
   - Model/Brand (optional but recommended)
   - Serial Number (required, must be unique)
   - Category (select from dropdown or custom)
   - Condition (select from 5-level scale: Excellent, Good, Fair, Poor, Damaged)
4. Submit - Equipment added to inventory

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

```text
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

```sql
DATABASE_URL=postgresql://user:password@localhost:5432/equipment_loan_db
```

## Loading Sample Data

```bash
python load_sample_data.py
```

This creates:

- **6 sample students** from diverse programs (Computer Science, Software Engineering, Mechanical Engineering, Business Administration, Electrical Engineering, Medicine)
- 6 equipment items with various brands and conditions
- 2 staff members
- 4 sample loans (including overdue items for testing)

## Testing

### Via Web Interface

1. Access <http://localhost:5000>
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

```text
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

```text
.
├── app.py                   # Main Flask application with routes
├── config.py               # Configuration (dev, test, prod)
├── models.py               # SQLAlchemy database models (7 tables)
├── routes.py               # REST API endpoints (20+ routes)
├── email_service.py        # Email handling and SMTP setup
├── scheduler.py            # Background task scheduling (APScheduler)
├── load_sample_data.py     # Sample data loader for testing
├── requirements.txt        # Python dependencies
├── Database Schema.sql     # SQL database schema
├── .env.example           # Environment variables template
├── SETUP_GUIDE.md         # Detailed setup instructions
├── README.md              # This file
├── templates/             # HTML templates (Jinja2)
│   ├── base.html          # Base layout and navigation
│   ├── index.html         # Dashboard & statistics
│   ├── students.html      # Student management (NEW)
│   ├── checkout.html      # Equipment checkout form
│   ├── equipment.html     # Equipment inventory management
│   └── loans.html         # Active/returned loans tracking
└── static/                # Static files
    ├── css/
    │   └── style.css      # Modern styling (updated condition colors)
    └── js/
        ├── dashboard.js   # Dashboard auto-refresh
        ├── checkout.js    # Checkout form handler
        ├── equipment.js   # Equipment CRUD operations
        ├── students.js    # Student CRUD operations (NEW)
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
| Equipment database | PostgreSQL equipment table with model field | ✅ |
| Log active loans | loans table with tracking | ✅ |
| Auto-update status | Automatic on checkout/return | ✅ |
| Daily scheduler | APScheduler at 8 AM | ✅ |
| Overdue checking | Query date_due < today | ✅ |
| Email reminders | Flask-Mail notifications | ✅ |
| Email logging | email_logs table | ✅ |
| Audit trail | audit_logs table | ✅ |
| Student Management | students.html page (NEW) | ✅ |
| Modern UI/UX | Condition dropdown with 5 levels (NEW) | ✅ |
| Equipment Model Field | Track brand/model details (NEW) | ✅ |

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
- Flask documentation: <https://flask.palletsprojects.com/>
- SQLAlchemy docs: <https://docs.sqlalchemy.org/>

## License

This is an educational project for a school assignment.

## Recent Updates (November 2025)

- ✅ Added Student Management page with full CRUD functionality
- ✅ Modernized Equipment Condition dropdown (5 levels: Excellent, Good, Fair, Poor, Damaged)
- ✅ Added Equipment Model/Brand field to track manufacturer details
- ✅ Enhanced UI with color-coded condition indicators
- ✅ Improved form validation and user feedback
- ✅ Updated navigation menu with Students link
- ✅ Enhanced CSS styling for better visual hierarchy

---

## UI/UX Design System

### Modern Color Palette

- **Primary**: Teal (#0f766e) with gradients
- **Success**: Green (#10b981) for available/active
- **Warning**: Amber (#f59e0b) for pending/fair
- **Danger**: Red (#ef4444) for overdue/errors

### Design Features

- Gradient backgrounds and buttons
- Smooth transitions and hover effects
- Status badges with visual indicators
- 4-level shadow system for depth
- Sticky navigation with backdrop blur
- Responsive grid layouts
- Modern border radius and spacing

---

## Documentation Index

- [Full Documentation Index](FULL_DOCUMENTATION_INDEX.md)

---

**Last Updated**: November 29, 2025
**Version**: 2.0 (CSS Modernized)
**Python**: 3.8+
**Database**: PostgreSQL 12+
**Status**: Production Ready ✅
